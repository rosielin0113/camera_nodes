import cv2
from ultralytics import YOLO

def main():
    camera_index = 0
    confidence_threshold = 0.4

    # Load YOLO model
    model = YOLO("yolov8n.pt")

    # Open camera
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}")
        return

    print("YOLO obstacle detection started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame from camera.")
            break

        # Run YOLO on current frame
        results = model(frame, verbose=False)

        detected_objects = []

        for result in results:
            boxes = result.boxes
            names = result.names

            if boxes is None:
                continue

            for box in boxes:
                conf = float(box.conf[0].item())
                if conf < confidence_threshold:
                    continue

                cls_id = int(box.cls[0].item())
                class_name = names[cls_id]

                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                width = x2 - x1
                height = y2 - y1
                center_x = x1 + width // 2
                center_y = y1 + height // 2

                detected_objects.append({
                    "class": class_name,
                    "confidence": round(conf, 2),
                    "bbox": (x1, y1, x2, y2),
                    "center": (center_x, center_y)
                })

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Draw label
                label = f"{class_name} {conf:.2f}"
                cv2.putText(
                    frame,
                    label,
                    (x1, max(y1 - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

                # Draw center point
                cv2.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)

        # Print detections for this frame
        if detected_objects:
            print("Detected possible obstacles:")
            for obj in detected_objects:
                print(
                    f"  class={obj['class']}, "
                    f"confidence={obj['confidence']}, "
                    f"center={obj['center']}, "
                    f"bbox={obj['bbox']}"
                )

        # Show result
        cv2.imshow("YOLO Obstacle Detection", frame)

        # Quit on q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
