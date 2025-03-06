import pyrealsense2 as rs
import numpy as np
import cv2
from flask import Flask, Response, render_template_string
import threading

app = Flask(__name__)

# Initialize RealSense pipeline
pipe = rs.pipeline()
cfg = rs.config()

# Enable RGB and Depth at max resolution
cfg.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
cfg.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

pipe.start(cfg)

# Align depth frame to color frame
align = rs.align(rs.stream.color)

# To store the current stream type (default is RGB)
current_stream = 'rgb'

# Default mix value for the overlay (0.0 to 1.0)
mix_value = 0.3  # Default mix value for depth overlay

# Function to get RGB stream (with JPEG compression)
def get_rgb():
    frames = pipe.wait_for_frames()
    color_frame = frames.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())

    # Compress using JPEG (quality set to 50 for faster compression)
    _, rgb_encoded = cv2.imencode('.jpg', color_image, [cv2.IMWRITE_JPEG_QUALITY, 50])
    return rgb_encoded

# Function to get aligned Depth stream (with JPEG compression)
def get_depth():
    frames = pipe.wait_for_frames()
    aligned_frames = align.process(frames)  # Align depth to RGB
    depth_frame = aligned_frames.get_depth_frame()

    depth_image = np.asanyarray(depth_frame.get_data())
    depth_colored = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    # Compress depth with JPEG
    _, depth_encoded = cv2.imencode('.jpg', depth_colored, [cv2.IMWRITE_JPEG_QUALITY, 50])
    return depth_encoded

# Function to get Overlay (aligned RGB + Depth, with JPEG compression)
def get_overlay():
    frames = pipe.wait_for_frames()
    aligned_frames = align.process(frames)  # Align depth to RGB

    color_frame = aligned_frames.get_color_frame()
    depth_frame = aligned_frames.get_depth_frame()

    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    # Convert depth to color map
    depth_colored = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    # Resize depth to match RGB size
    depth_resized = cv2.resize(depth_colored, (color_image.shape[1], color_image.shape[0]))

    # Overlay aligned depth on RGB with dynamic mixing
    overlay = cv2.addWeighted(color_image, 1 - mix_value, depth_resized, mix_value, 0)

    # Compress overlay with JPEG
    _, overlay_encoded = cv2.imencode('.jpg', overlay, [cv2.IMWRITE_JPEG_QUALITY, 50])
    return overlay_encoded

# Route to change the camera view
@app.route('/change_stream/<stream_type>')
def change_stream(stream_type):
    global current_stream
    if stream_type in ['rgb', 'depth', 'overlay']:
        current_stream = stream_type
        return f"Stream changed to {stream_type}."
    return "Invalid stream type. Use 'rgb', 'depth', or 'overlay'."

# Route to change the overlay mix value
@app.route('/set_mix_value/<float:value>')
def set_mix_value(value):
    global mix_value
    if 0.0 <= value <= 1.0:
        mix_value = value
        return f"Overlay mix value set to {value}."
    else:
        return "Invalid value. Must be between 0.0 and 1.0."

# Function to stream the selected camera mode to the browser
def stream_video():
    while True:
        if current_stream == 'rgb':
            encoded_image = get_rgb()
        elif current_stream == 'depth':
            encoded_image = get_depth()
        elif current_stream == 'overlay':
            encoded_image = get_overlay()

        frame = encoded_image.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Route for the video feed
@app.route('/video_feed')
def video_feed():
    return Response(stream_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Embed HTML as a string inside Python
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RealSense Stream Viewer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
        }
        #video {
            max-width: 100%;
            border: 1px solid #ccc;
            margin-bottom: 20px;
        }
        .controls {
            margin-top: 20px;
        }
        .controls button, .controls input {
            margin: 5px;
        }
    </style>
</head>
<body>

<h1>RealSense Video Stream</h1>

<!-- Video Feed -->
<img id="video" src="{{ url_for('video_feed') }}" alt="Video Stream">

<div class="controls">
    <h3>Stream Controls</h3>
    
    <button onclick="changeStream('rgb')">RGB</button>
    <button onclick="changeStream('depth')">Depth</button>
    <button onclick="changeStream('overlay')">Overlay</button>

    <h3>Overlay Mix Control (0.0 to 1.0)</h3>
    <input type="range" id="mixSlider" min="0" max="1" step="0.01" value="0.3" onchange="setMixValue(this.value)">
    <span id="mixValueLabel">0.3</span>
</div>

<script>
    // Update overlay mix value when slider changes
    function setMixValue(value) {
        document.getElementById('mixValueLabel').textContent = value;
        fetch(`/set_mix_value/${value}`);
    }

    // Change the stream type (rgb, depth, overlay)
    function changeStream(streamType) {
        fetch(`/change_stream/${streamType}`);
    }
</script>

</body>
</html>
"""

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template_string(html_code)

# Start Flask server in a separate thread to handle web requests
def start_flask():
    app.run(host='0.0.0.0', port=5000, threaded=True)

# Start the Flask server in a new thread
flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()

# Keep the main thread alive while the Flask server runs
while True:
    pass
