import pyrealsense2 as rs
import numpy as np
import cv2
import time
from flask import Flask, Response, render_template_string
import threading
import pykobuki
import os

app = Flask(__name__)

# Initialize RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
pipeline.start(config)

# Align depth to color
align = rs.align(rs.stream.color)

# Load YOLO model
net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load COCO class labels
with open("coco.names", "r") as f:
    classes = f.read().strip().split("\n")

# Detection & Obstacle Avoidance Parameters
confidence_threshold = 0.5
nms_threshold = 0.4
LEFT_THRESHOLD = 1
RIGHT_THRESHOLD = 1
CENTER_THRESHOLD = 0.7

ROBOT_SPEED = 1/4

# Movement control toggle (default OFF)
movement_enabled = False  

def get_rgb():
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    color_frame = aligned_frames.get_color_frame()
    depth_frame = aligned_frames.get_depth_frame()

    color_image = np.asanyarray(color_frame.get_data())

    # YOLO Detection
    blob = cv2.dnn.blobFromImage(color_image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids, confidences, boxes = [], [], []
    height, width, _ = color_image.shape

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]

            # Get object distance
            center_x = x + w // 2
            center_y = y + h // 2
            depth_value = depth_frame.get_distance(center_x, center_y)  # Meters
            distance_cm = depth_value * 100  # Convert to cm

            cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(color_image, f"{label} {confidence:.2f} | {distance_cm:.1f} cm", 
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    _, rgb_encoded = cv2.imencode('.jpg', color_image, [cv2.IMWRITE_JPEG_QUALITY, 50])
    return rgb_encoded

def get_depth():
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    depth_frame = aligned_frames.get_depth_frame()
    depth_image = np.asanyarray(depth_frame.get_data())
    depth_colored = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    _, depth_encoded = cv2.imencode('.jpg', depth_colored, [cv2.IMWRITE_JPEG_QUALITY, 50])
    return depth_encoded

def obstacle_avoidance():
    global movement_enabled
    while True:
        if not movement_enabled:
            robot.move(0, 0)
            time.sleep(0.1)
            continue

        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        depth_data = np.asanyarray(depth_frame.get_data()) / 1000.0  # Convert mm to meters

        height, width = depth_data.shape
        left_region = depth_data[:, :width // 3]
        right_region = depth_data[:, 2 * width // 3:]
        center_region = depth_data[:, width // 3:2 * width // 3]

        def get_filtered_distance(region):
            valid_values = region[region > 0]  # Remove invalid (zero) depth readings
            if valid_values.size == 0:
                return float('inf')  # No valid depth, assume no obstacle
            return np.percentile(valid_values, 10)  # Use 10th percentile to reduce noise

        left_dist = get_filtered_distance(left_region)
        right_dist = get_filtered_distance(right_region)
        center_dist = get_filtered_distance(center_region)

        print(f"Left: {left_dist:.2f} m, Right: {right_dist:.2f} m, Center: {center_dist:.2f} m")

        if center_dist < CENTER_THRESHOLD:
            print("Obstacle ahead! Stopping!")
            robot.move(0, 0)
        elif left_dist < LEFT_THRESHOLD:
            print("Obstacle on left! Turning right!")
            robot.move(ROBOT_SPEED, -1)
        elif right_dist < RIGHT_THRESHOLD:
            print("Obstacle on right! Turning left!")
            robot.move(ROBOT_SPEED, 1)
        else:
            print("Path clear! Moving forward!")
            robot.move(ROBOT_SPEED, 0)

        time.sleep(0.1)

@app.route('/toggle_movement')
def toggle_movement():
    global movement_enabled
    movement_enabled = not movement_enabled
    return f"Obstacle avoidance {'enabled' if movement_enabled else 'disabled'}."

@app.route('/video_feed')
def video_feed():
    def stream_video():
        while True:
            frame = get_rgb().tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return Response(stream_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>RealSense Stream</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        img { width: 80%; border: 2px solid black; }
        button { margin-top: 20px; padding: 10px 20px; font-size: 18px; }
    </style>
</head>
<body>
    <h1>RealSense Object Detection & Obstacle Avoidance</h1>
    <img src="{{ url_for('video_feed') }}" alt="Video Feed">
    <br>
    <button onclick="toggleMovement()">Toggle Obstacle Avoidance</button>
    <script>
        function toggleMovement() {
            fetch('/toggle_movement').then(response => response.text()).then(alert);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_code)

def start_flask():
    app.run(host='0.0.0.0', port=5000, threaded=True)

flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()

robot = pykobuki.Kobuki("/dev/kobuki")

obstacle_avoidance()
