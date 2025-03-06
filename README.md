# LoCoBot
A project to get LoCoBot running in 2025 via modified scripts and setup.

## RealSense Stream Viewer
- **`realsense_stream_viewer.py`**: A Flask-based Python server that interfaces with the RealSense camera, handles streaming of RGB, depth, and overlay images, and provides a control interface for users via a web browser.
  - It uses `pyrealsense2` to interface with the RealSense camera.
  - A simple web server built with Flask streams the video feed from the camera.
  - Control options via the web UI allow users to switch between RGB, depth, and overlay streams, as well as adjust the depth-overlay mix.
  
- **Web Interface**: The script serves an HTML interface to allow easy control over the camera stream, including options to adjust the depth-overlay mix. This interface is displayed through a web browser.

### Usage
1. Run the `realsense_stream_viewer.py` script to start the Flask server.
2. Open a web browser and navigate to `http://<your-robot-ip>:5000` to access the RealSense video stream controls.
3. Use the buttons and slider to change the stream type (RGB, Depth, or Overlay) and adjust the overlay mix.

## Koboki
This is the "Roomba" part of the robot. I have been able to read the basic data over serial but not control it yet.
Needs to be finished [Kobuki - User Guide](docs/Kobuki%20-%20User%20Guide.pdf).
More information on the protocol found at [Appendix Protocol Specification](https://yujinrobot.github.io/kobuki/enAppendixProtocolSpecification.html)

### Usage
1. Run the `koboki.py` script to start the serial connection.
2. View the sensor data.