import pykobuki
import time

# Initialize the robot
kobuki = pykobuki.Kobuki()

# Set the rotation speed and duration
angular_speed = 3.14 / 2  # 90-degree turn speed
rotation_time = 3  # Rotate for 3 seconds

start_time = time.time()
while True:
    # Check if rotation time has passed
    if time.time() - start_time < rotation_time:
        # Rotate the robot
        kobuki.move(0, angular_speed)
    else:
        # Stop rotating after the specified time
        kobuki.move(0, 0)
        break

    # Check if any bumper is pressed during the rotation
    sensors = kobuki.read_sensor_data()
    if sensors['bumper_left'] or sensors['bumper_center'] or sensors['bumper_right']:
        print("Bumper pressed! Reversing.")
        kobuki.move(-0.2, 0)  # Reverse for 1 second
        time.sleep(1)

    time.sleep(0.1)  # Small delay to allow sensor data to update
