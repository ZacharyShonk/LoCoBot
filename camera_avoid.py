import pyrealsense2 as rs
import numpy as np
import time

# Initialize RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # Depth stream setup
pipeline.start(config)

# Define threshold distance (in meters) to detect obstacles
LEFT_THRESHOLD = 0.7  # meters
RIGHT_THRESHOLD = 0.7  # meters
CENTER_THRESHOLD = 0.5  # meters

def get_depth_frame():
    frames = pipeline.wait_for_frames()  # Get frames from the camera
    depth_frame = frames.get_depth_frame()  # Get depth frame
    return np.asanyarray(depth_frame.get_data())  # Convert to numpy array for processing

def analyze_obstacle_distance(depth_data):
    # Divide the image into left, center, and right regions
    height, width = depth_data.shape
    left_region = depth_data[:, :width // 3]  # Left third of the frame
    right_region = depth_data[:, 2 * width // 3:]  # Right third of the frame
    center_region = depth_data[:, width // 3:2 * width // 3]  # Center third of the frame

    # Convert the depth data from millimeters to meters
    left_region = left_region / 1000.0
    right_region = right_region / 1000.0
    center_region = center_region / 1000.0

    # Calculate the average depth in each region
    left_avg_depth = np.mean(left_region[left_region > 0])  # Ignore 0 values (invalid depth)
    right_avg_depth = np.mean(right_region[right_region > 0])
    center_avg_depth = np.mean(center_region[center_region > 0])

    return left_avg_depth, right_avg_depth, center_avg_depth

def obstacle_avoidance():
    while True:
        depth_data = get_depth_frame()  # Get current depth frame
        left, right, center = analyze_obstacle_distance(depth_data)  # Analyze obstacle distances
        
        print(f"Left: {left:.2f} m, Right: {right:.2f} m, Center: {center:.2f} m")

        # Decision Making
        if center < CENTER_THRESHOLD:
            print("Obstacle in front, stop!")
            # Stop the robot
        elif left < LEFT_THRESHOLD:
            print("Obstacle on left, turn right!")
            # Turn right
        elif right < RIGHT_THRESHOLD:
            print("Obstacle on right, turn left!")
            # Turn left
        else:
            print("Path clear, move forward!")

        time.sleep(0.1)  # Small delay to simulate real-time processing

if __name__ == "__main__":
    try:
        obstacle_avoidance()  # Start obstacle avoidance
    finally:
        pipeline.stop()  # Stop the RealSense pipeline
