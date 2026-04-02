#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

import cv2
from ultralytics import YOLO

from std_msgs.msg import String
import json


class YoloDetectionNode(Node):

    def __init__(self):
        super().__init__('yolo_detection_node')

        self.get_logger().info("YOLO Detection Node started")

        # Parameters
        self.camera_index = 0
        self.conf_threshold = 0.4

        # Load YOLO model
        self.model = YOLO("yolov8n.pt")

        # Open camera
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            self.get_logger().error("Failed to open camera")

        # Publisher 
        self.publisher_ = self.create_publisher(String, 'detections', 10)

        # Timer
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().error("Failed to read frame")
            return

        results = self.model(frame, verbose=False)

        detected_objects = []

        for result in results:
            boxes = result.boxes
            names = result.names

            if boxes is None:
                continue

            for box in boxes:
                conf = float(box.conf[0].item())
                if conf < self.conf_threshold:
                    continue

                cls_id = int(box.cls[0].item())
                class_name = names[cls_id]

                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                detected_objects.append({
                    "class": class_name,
                    "confidence": round(conf, 2),
                    "center": (center_x, center_y)
                })


        if detected_objects:
            msg = String()
            msg.data = json.dumps(detected_objects)

            self.publisher_.publish(msg)

            self.get_logger().info(f"Published {len(detected_objects)} detections")

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = YoloDetectionNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
