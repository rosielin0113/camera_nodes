#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

import cv2
import cv2.aruco as aruco
import numpy as np
import json

from std_msgs.msg import String


class ArucoNode(Node):

    def __init__(self):
        super().__init__('aruco_node')

        self.get_logger().info("Aruco Node started")

        # Camera
        self.cap = cv2.VideoCapture(0)

        # ArUco detector
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.parameters = aruco.DetectorParameters()

        # Publisher
        self.publisher_ = self.create_publisher(String, 'aruco_detections', 10)

        # Timer
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().error("Failed to read frame")
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners_list, ids, _ = aruco.detectMarkers(
            gray,
            self.aruco_dict,
            parameters=self.parameters,
        )

        detections = []

        if ids is not None:
            h, w = frame.shape[:2]
            cx_img, cy_img = w / 2.0, h / 2.0

            for i, corners in enumerate(corners_list):
                c = corners[0]
                center = c.mean(axis=0)
                cx, cy = center

                dx = (cx - cx_img) / cx_img
                dy = (cy - cy_img) / cy_img

                detections.append({
                    "id": int(ids[i]),
                    "center": [float(cx), float(cy)],
                    "offset_norm": [float(dx), float(dy)]
                })

        # Publisher
        if detections:
            msg = String()
            msg.data = json.dumps(detections)

            self.publisher_.publish(msg)

            self.get_logger().info(f"Published {len(detections)} markers")

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = ArucoNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
