import time
import numpy as np
import pyrealsense2 as rs
import pykobuki
from camera_server import pipeline, align, start_camera_server

# Define any obstacle avoidance specific constants and functions here
ROBOT_SPEED = 0.01

# Initialize your robot
robot = pykobuki.Kobuki("/dev/kobuki")

def obstacle_avoidance():
    global ROBOT_SPEED
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        depth_data = np.asanyarray(depth_frame.get_data()) / 1000.0  # Convert mm to meters
        height, width = depth_data.shape

        print(height,width)

        left_region = depth_data[:, int(width * 0.2):int(width * 0.4)]
        right_region = depth_data[:, int(width * 0.6):int(width * 0.8)]
        center_region = depth_data[:, int(width * 0.4):int(width * 0.6)]

        def get_filtered_distance(region):
            valid_values = region[region > 0]
            if valid_values.size == 0:
                return float('inf')
            return np.percentile(valid_values, 10)

        left_dist = get_filtered_distance(left_region)
        right_dist = get_filtered_distance(right_region)
        center_dist = get_filtered_distance(center_region)
        print(f"Left: {left_dist:.2f} m, Right: {right_dist:.2f} m, Center: {center_dist:.2f} m")

        # Write algo here

        time.sleep(0.1)

if __name__ == '__main__':
    start_camera_server()
    
    try:
        obstacle_avoidance()
    except KeyboardInterrupt:
        pass
