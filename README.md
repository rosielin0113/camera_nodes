# Camera Node

This repository contains prototype perception scripts for the UAV side of the Raytheon Autonomous Vehicle Competition project.

The current code includes:

- a basic camera test using OpenCV
- a YOLO-based obstacle detection test using a live camera feed

These scripts are intended for early development and testing before full ROS2 integration.

---

## Files

### `camera_test.py`
Opens the default camera using OpenCV and displays the live video stream.

### `yolo_test.py`
Opens the default camera, runs YOLO object detection on each frame, draws bounding boxes around detected objects, and prints possible obstacle information in the terminal.

---

## Requirements

- Python 3.9+
- OpenCV
- Ultralytics YOLO

---

## Installation

Install dependencies with:

```bash
pip install opencv-python ultralytics
