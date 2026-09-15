#!/usr/bin/env python3
"""Automated repository checks for Lab 4: Python ROS 2 Nodes.

Run with: pytest test_lab_4.py -v

These checks establish that the required work left usable repository artifacts.
Course staff use the Gradescope PDF to grade node behavior, screenshot content,
and discussion answers.
"""

from __future__ import annotations

import ast
import struct
import subprocess
import warnings
import zlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent

PACKAGE_ROOT = Path("ros2_ws/src/lab04_pub_sub")
PYTHON_PACKAGE = PACKAGE_ROOT / "lab04_pub_sub"
REQUIRED_NODE_FILES = ("node_a.py", "node_b.py", "node_c.py")
REQUIRED_SCREENSHOTS = (
    "colcon_build.png",
    "nodes_running.png",
    "rqt_graph.png",
)
EXPECTED_ENTRY_POINT_TARGETS = {
    "lab04_pub_sub.node_a:main",
    "lab04_pub_sub.node_b:main",
    "lab04_pub_sub.node_c:main",
}
README_STARTER_FINGERPRINT = "Update this README"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
IMAGE_SIGNATURES = (
    b"\xff\xd8\xff",
    b"GIF87a",
    b"GIF89a",
    b"BM",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _png_dimensions(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None

    position = 8
    dimensions: tuple[int, int] | None = None
    compressed = bytearray()
    saw_end = False
    while position + 12 <= len(data):
        length = struct.unpack(">I", data[position:position + 4])[0]
        chunk_end = position + 12 + length
        if chunk_end > len(data):
            return None
        kind = data[position + 4:position + 8]
        payload = data[position + 8:position + 8 + length]
        expected_crc = struct.unpack(">I", data[position + 8 + length:chunk_end])[0]
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != expected_crc:
            return None
        if kind == b"IHDR":
            if dimensions is not None or length != 13:
                return None
            dimensions = struct.unpack(">II", payload[:8])
        elif kind == b"IDAT":
            compressed.extend(payload)
        elif kind == b"IEND":
            if length != 0 or chunk_end != len(data):
                return None
            saw_end = True
            break
        position = chunk_end

    if dimensions is None or not compressed or not saw_end:
        return None
    try:
        zlib.decompress(compressed)
    except zlib.error:
        return None
    return dimensions


def _is_image(path: Path) -> bool:
    head = path.read_bytes()[:12]
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return _png_dimensions(path) is not None
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return True
    return any(head.startswith(signature) for signature in IMAGE_SIGNATURES)


def _literal(node: ast.AST, assignments: dict[str, object]) -> object:
    if isinstance(node, ast.Name) and node.id in assignments:
        return assignments[node.id]
    return ast.literal_eval(node)


def _console_scripts(setup_path: Path) -> tuple[dict[str, str], str | None]:
    try:
        tree = ast.parse(_read_text(setup_path), filename=str(setup_path))
    except SyntaxError as exc:
        return {}, (
            "setup.py could not be read because it has invalid Python syntax: "
            f"{exc.msg} on line {exc.lineno}. Fix that line, then rerun pytest."
        )

    assignments: dict[str, object] = {}
    for statement in tree.body:
        if not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
            continue
        target = statement.targets[0]
        if not isinstance(target, ast.Name):
            continue
        try:
            assignments[target.id] = ast.literal_eval(statement.value)
        except (ValueError, TypeError):
            continue

    entry_points_node: ast.AST | None = None
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function_name = None
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
        if function_name != "setup":
            continue
        for keyword in node.keywords:
            if keyword.arg == "entry_points":
                entry_points_node = keyword.value
                break
        if entry_points_node is not None:
            break

    if entry_points_node is None:
        return {}, (
            "setup.py does not pass entry_points to setup(). Add a console_scripts "
            "entry for each node, then rerun pytest."
        )

    try:
        entry_points = _literal(entry_points_node, assignments)
    except (ValueError, TypeError):
        return {}, (
            "The grader could not read setup.py entry_points. Use the standard "
            "entry_points={'console_scripts': [...]} form shown in the manual."
        )
    if not isinstance(entry_points, dict):
        return {}, "setup.py entry_points must be a dictionary containing console_scripts."

    raw_scripts = entry_points.get("console_scripts")
    if not isinstance(raw_scripts, (list, tuple)):
        return {}, "setup.py entry_points needs a console_scripts list for the three nodes."

    scripts: dict[str, str] = {}
    for item in raw_scripts:
        if not isinstance(item, str) or "=" not in item:
            continue
        executable, target = item.split("=", 1)
        scripts[executable.strip()] = target.strip()
    return scripts, None


def check_required_files(repo: Path) -> list[str]:
    errors: list[str] = []

    required_files = (
        Path("README.md"),
        PACKAGE_ROOT / "package.xml",
        PACKAGE_ROOT / "setup.py",
        PYTHON_PACKAGE / "__init__.py",
        *(PYTHON_PACKAGE / name for name in REQUIRED_NODE_FILES),
    )
    for relative in required_files:
        path = repo / relative
        if not path.is_file():
            errors.append(f"Add the missing required file: {relative.as_posix()}")
        elif path.stat().st_size == 0 and relative.name != "__init__.py":
            errors.append(f"Add your work to the empty file: {relative.as_posix()}")

    readme = repo / "README.md"
    if readme.is_file() and README_STARTER_FINGERPRINT in _read_text(readme):
        errors.append(
            "README.md still says 'Update this README'. Replace that sentence "
            "with your name, NetID, and a 1-3 line summary."
        )

    docs = repo / "docs"
    if not docs.is_dir():
        errors.append("Add a docs/ directory containing the three screenshots from the lab.")
    else:
        candidates = [
            path for path in docs.iterdir()
            if path.is_file() and path.suffix.casefold() in IMAGE_EXTENSIONS
        ]
        valid_images = [path for path in candidates if _is_image(path)]
        if len(valid_images) < 3:
            errors.append(
                "Add three readable screenshot images to docs/. "
                f"The grader found {len(valid_images)}. PNG, JPEG, GIF, BMP, and WebP "
                "files are accepted; course staff judge their content from the PDF."
            )
        expected = set(REQUIRED_SCREENSHOTS)
        present_names = {path.name for path in valid_images}
        missing_names = sorted(expected - present_names)
        if missing_names and len(valid_images) >= 3:
            warnings.warn(
                "The three screenshots are present, but these recommended filenames "
                f"were not found: {', '.join(missing_names)}"
            )

    setup_path = repo / PACKAGE_ROOT / "setup.py"
    if setup_path.is_file():
        scripts, parse_error = _console_scripts(setup_path)
        if parse_error:
            errors.append(parse_error)
        else:
            actual_targets = set(scripts.values())
            for target in sorted(EXPECTED_ENTRY_POINT_TARGETS):
                if target not in actual_targets:
                    errors.append(
                        "Add a setup.py console_scripts entry targeting "
                        f"'{target}'. The executable name to the left of '=' may be your choice."
                    )

    return errors


def check_repository_hygiene(repo: Path) -> list[str]:
    if not (repo / ".git").exists():
        return [
            "Run pytest from the root of your cloned Lab 4 repository. "
            "The grader could not find its .git directory."
        ]

    result = _run_git(repo, "ls-files")
    if result.returncode != 0:
        return [
            "The grader could not inspect tracked files with 'git ls-files'. "
            "Run 'git status' and resolve the reported Git problem first."
        ]

    forbidden_directories = {"build", "install", "log"}
    tracked = [Path(line) for line in result.stdout.splitlines() if line]
    prohibited = [
        path.as_posix()
        for path in tracked
        if ({part.casefold() for part in path.parts[:-1]} & forbidden_directories)
    ]
    if prohibited:
        shown = prohibited[:8]
        remainder = len(prohibited) - len(shown)
        summary = ", ".join(shown)
        if remainder:
            summary += f", and {remainder} more"
        return [
            "Remove generated build/, install/, and log/ files from Git tracking, "
            "then commit and push again. The files may remain on your VM if .gitignore "
            f"excludes them. Tracked generated files: {summary}"
        ]
    return []


def _assert_no_errors(errors: list[str]) -> None:
    assert not errors, "\n- " + "\n- ".join(errors)


def test_repository_evidence() -> None:
    _assert_no_errors(check_required_files(REPO_ROOT))
    for notice in check_repository_hygiene(REPO_ROOT):
        warnings.warn("No points lost: " + notice)
