import pykobuki
import time
import random

# Initialize the robot
kobuki = pykobuki.Kobuki()

# Set the movement parameters
linear_speed = 0.2
angular_speed = 3.14 / 2  # 90-degree turn speed

while True:
    # Read sensor data
    sensors = kobuki.read_sensor_data()

    # If any bumper is pressed or cliff is detected, avoid and change direction
    if sensors['bumper_left'] or sensors['bumper_center'] or sensors['bumper_right']:
        print("Obstacle detected! Changing direction.")
        kobuki.move(-linear_speed, 0)  # Reverse
        time.sleep(1)
        kobuki.move(0, random.choice([-angular_speed, angular_speed]))  # Rotate randomly
        time.sleep(1)

    elif sensors['cliff_left'] or sensors['cliff_center'] or sensors['cliff_right']:
        print("Cliff detected! Changing direction.")
        kobuki.move(-linear_speed, 0)  # Reverse
        time.sleep(1)
        kobuki.move(0, random.choice([-angular_speed, angular_speed]))  # Rotate randomly
        time.sleep(1)

    # Continue moving in a random direction
    else:
        direction = random.choice([0, 1])  # 0 for forward, 1 for reverse
        if direction == 0:
            kobuki.move(linear_speed, 0)  # Move forward
        else:
            kobuki.move(-linear_speed, 0)  # Move backward
        time.sleep(2)  # Move for 2 seconds before changing direction
