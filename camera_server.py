from flask import Flask, Response, render_template_string, request
import pyrealsense2 as rs
import numpy as np
import cv2
import threading
import time

# --- Initialization of RealSense and YOLO --- #
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
pipeline.start(config)
align = rs.align(rs.stream.color)

# Load YOLO model and class labels
net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
with open("coco.names", "r") as f:
    classes = f.read().strip().split("\n")

# Flask application setup
app = Flask(__name__)

# HTML template for the preview page
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>RealSense Stream</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        img { width: 80%; border: 2px solid black; }
    </style>
</head>
<body>
    <h1>RealSense Object Detection</h1>
    <img src="{{ url_for('video_feed_depth') }}" alt="Video Feed">
</body>
</html>
"""

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
            if confidence > 0.3:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            # Get object distance from depth
            center_x = x + w // 2
            center_y = y + h // 2
            depth_value = depth_frame.get_distance(center_x, center_y)
            distance_cm = depth_value * 100  # meters to cm

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

@app.route('/video_feed_depth')
def video_feed_depth():
    def stream_video():
        while True:
            frame = get_depth().tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return Response(stream_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_rgb')
def video_feed_rgb():
    def stream_video():
        while True:
            frame = get_rgb().tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return Response(stream_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template_string(html_code)

def run_server():
    app.run(host='0.0.0.0', port=5000, threaded=True)

def start_camera_server():
    """Start the Flask camera preview server in a new daemon thread."""
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    return server_thread

# Allow the module to be run directly for testing purposes.
if __name__ == '__main__':
    start_camera_server()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
