# Lab 4: Python ROS 2 Nodes (Publisher, Relay, Subscriber): [Your Name]

ECE 383 / ME 555: Introduction to Robotics and Automation (Fall 2026)

Update this README with your name, NetID, and a 1–3 line summary of your work.

## Contents

- `node_scaffolds/`: incomplete starting files for Nodes A, B, and C
- `docs/`: build, running-node, and ROS graph screenshots
- `test_lab_4.py`: automated repository checks
- `pytest.ini`: limits `pytest` to `test_lab_4.py` so it skips the ROS 2 workspace

Create `ros2_ws/src/lab04_pub_sub/` by following the lab manual. Keep the
original files in `node_scaffolds/` and copy each one into the Python package
before completing its TODOs.

## Run the grading checks

From the repository root on the VM:

```bash
pytest -v
```

The checks confirm that the repository contains your package, three node files,
three readable images, an updated README, and entry points for the nodes. They
also flag tracked ROS 2 build output. Screenshot filenames and console-script
executable names are recommendations, so reasonable alternatives still pass.

Passing the repository checks does not mean the full lab has been graded.
Course staff use your Gradescope PDF to evaluate node behavior, the evidence
shown in each screenshot, and your discussion answers.

Failures are expected while the lab is incomplete. Fix every failure before
the final push and confirm that Classroom 50 reports a passing result.
