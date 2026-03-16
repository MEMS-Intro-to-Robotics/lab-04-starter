#!/usr/bin/env python3
"""
Autograding validation for Lab 4: ROS 2 Python Publisher/Subscriber Pipeline.
Run with: pytest test_lab_4.py -v
"""

import ast
import os
import warnings

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
GITIGNORE_EXPECTED = {"build/", "install/", "log/", "build", "install", "log"}
README_STARTER_FINGERPRINT = "Update this README"

PKG_DIR = os.path.join("ros2_ws", "src", "lab04_pub_sub")
NODE_FILES = ["node_a.py", "node_b.py", "node_c.py"]
EXPECTED_ENTRY_POINTS = {"node_a", "node_b", "node_c"}


def _find_in_package(name):
    """Search for a file in the package directory tree."""
    for root, dirs, files in os.walk(PKG_DIR):
        if name in files:
            return os.path.join(root, name)
    return os.path.join(PKG_DIR, name)


def _get_images(docs_dir="docs"):
    if not os.path.isdir(docs_dir):
        return []
    return [
        f for f in os.listdir(docs_dir)
        if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
    ]


def _check_syntax(path):
    with open(path, "r", errors="replace") as f:
        source = f.read()
    ast.parse(source, filename=path)


# ── Required files (hard fail) ──────────────────────────────


def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md not found"


def test_readme_not_empty():
    assert os.path.getsize("README.md") > 0, "README.md is empty"


def test_readme_updated():
    with open("README.md", "r", errors="replace") as f:
        content = f.read()
    assert README_STARTER_FINGERPRINT not in content, (
        "README.md still contains the starter template text. "
        "Please update it with your name, NetID, and instructions for running your code."
    )


def test_docs_directory_exists():
    assert os.path.isdir("docs"), "docs/ directory not found"


def test_package_directory_exists():
    assert os.path.isdir(PKG_DIR), f"ROS 2 package not found at {PKG_DIR}"


def test_setup_py_exists():
    assert os.path.isfile(os.path.join(PKG_DIR, "setup.py")), "setup.py not found"


def test_package_xml_exists():
    assert os.path.isfile(os.path.join(PKG_DIR, "package.xml")), "package.xml not found"


def test_node_a_exists():
    path = _find_in_package("node_a.py")
    assert os.path.isfile(path), "node_a.py not found in package"


def test_node_b_exists():
    path = _find_in_package("node_b.py")
    assert os.path.isfile(path), "node_b.py not found in package"


def test_node_c_exists():
    path = _find_in_package("node_c.py")
    assert os.path.isfile(path), "node_c.py not found in package"


# ── Python syntax (hard fail) ───────────────────────────────


def test_node_a_syntax():
    _check_syntax(_find_in_package("node_a.py"))


def test_node_b_syntax():
    _check_syntax(_find_in_package("node_b.py"))


def test_node_c_syntax():
    _check_syntax(_find_in_package("node_c.py"))


# ── Entry points (warnings) ─────────────────────────────────


def test_setup_entry_points():
    setup_path = os.path.join(PKG_DIR, "setup.py")
    if not os.path.isfile(setup_path):
        return
    with open(setup_path, "r", errors="replace") as f:
        content = f.read()
    missing = {ep for ep in EXPECTED_ENTRY_POINTS if ep not in content}
    if missing:
        warnings.warn(f"Entry points not found in setup.py: {', '.join(sorted(missing))}")


# ── Screenshots (warnings) ──────────────────────────────────


def test_screenshot_count():
    images = _get_images()
    print(f"\nFound {len(images)} image(s) in docs/:")
    for img in sorted(images):
        print(f"  - {img}")
    if len(images) < 3:
        warnings.warn(f"Expected at least 3 screenshots, found {len(images)}")


# ── Git hygiene (warnings) ──────────────────────────────────


def test_gitignore_exists():
    if not os.path.isfile(".gitignore"):
        warnings.warn(".gitignore not found — build/, install/, log/ should be excluded")


def test_no_build_artifacts():
    for d in ["build", "install", "log"]:
        for base in [".", "ros2_ws"]:
            path = os.path.join(base, d)
            if os.path.isdir(path):
                warnings.warn(f"'{path}' is committed — should be in .gitignore")
