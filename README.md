# UAV & UGV Perception System README

*(Camera Node + YOLO Detection Node + ArUco Detection Node)*

---

## 1. System Overview

This project implements a modular perception system for autonomous UAV/UGV platforms using ROS2.

The system is composed of three main nodes:

* **Camera Node** – Captures raw images from the camera
* **YOLO Detection Node** – Performs obstacle/object detection
* **ArUco Detection Node** – Detects fiducial markers for navigation and alignment

---

## 2. System Architecture

```
[Camera Node]
      ↓  /camera/image_raw
[YOLO Node] --------→ /detections
[ArUco Node] -------→ /aruco_detections
      ↓
[Control / Planning Node]
      ↓
[Robot (UGV / UAV)]
```

### Key Design Principles

* Modular (each function = one node)
* Interface-based (ROS2 topics)
* Scalable (can add SLAM, tracking, etc.)
* Testable (each node independently verified)

---

## 3. Camera Node

### Purpose

Captures real-time video frames and publishes them to the system.

### Functionality

* Opens camera device
* Captures frames at fixed rate
* Publishes images to ROS2 topic

### Output Topic

```
/camera/image_raw
```

### Key Features

* Event-driven (ROS2 timer instead of while loop)
* Compatible with downstream perception nodes
* Clean resource handling (camera release)

---

## 4. YOLO Detection Node

### Purpose

Detects objects (obstacles) using YOLOv8 model.

### Input

* Camera frames (direct or via topic)

### Output

```
/detections
```

### Output Format (JSON)

```json
[
  {
    "class": "person",
    "confidence": 0.87,
    "center": [320, 240]
  }
]
```

### Functionality

* Runs YOLO model on each frame
* Filters detections by confidence threshold
* Extracts:

  * class label
  * confidence
  * bounding box center

### System Role

* Provides obstacle awareness
* Used for:

  * collision avoidance
  * path planning

---

## 5. ArUco Detection Node

### Purpose

Detects ArUco markers for localization, alignment, and landing.

### Input

* Camera frames

### Output

```
/aruco_detections
```

### Output Format (JSON)

```json
[
  {
    "id": 3,
    "center": [315, 250],
    "offset_norm": [0.02, -0.05]
  }
]
```

---

## 6. ArUco Centering Concept (Critical)

Each detection computes:

```
dx = (cx - image_center_x) / image_center_x
dy = (cy - image_center_y) / image_center_y
```

### Interpretation

| Value  | Meaning                         |
| ------ | ------------------------------- |
| dx = 0 | perfectly centered horizontally |
| dx > 0 | marker is on the right          |
| dx < 0 | marker is on the left           |

| Value  | Meaning             |
| ------ | ------------------- |
| dy = 0 | vertically centered |
| dy > 0 | marker is below     |
| dy < 0 | marker is above     |

### Control Logic Example

```
if dx > 0 → turn right
if dx < 0 → turn left
if dx ≈ 0 → go forward
```

### System Meaning

ArUco centering is used to minimize visual alignment error and guide robot motion.

---

## 7. Integration Flow

### Perception → Control

```
YOLO → obstacle detection
ArUco → target alignment
```

Combined:

```
if obstacle detected:
    avoid
else:
    align to ArUco marker
```

---

## 8. Dependencies

* Python 3.x
* ROS2 (rclpy)
* OpenCV (`cv2`)
* OpenCV ArUco module
* Ultralytics YOLO (`ultralytics`)

Install example:

```
pip install opencv-python ultralytics
```

---

## 9. Future Improvements

* Replace JSON with custom ROS2 message types
* Add camera calibration (pose estimation with ArUco)
* Integrate depth estimation
* Add tracking (multi-frame object tracking)
* Connect to motion control node

---

## 10. System Engineering Perspective

This system follows the V-model and modular architecture:

* Level 1: Unit (Camera / YOLO / ArUco nodes)
* Level 2: Subsystem (Perception system)
* Level 3: Integration (Perception + Control)
* Level 4: System (Autonomous navigation)

---

## 11. Summary

This project demonstrates:

* Real-time perception pipeline
* AI-based detection (YOLO)
* Vision-based navigation (ArUco)
* ROS2 modular system architecture

It forms the foundation for autonomous UAV/UGV navigation and control.

