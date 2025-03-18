import pykobuki
import time

# Initialize the robot
kobuki = pykobuki.Kobuki()

# Set forward speed and rotation speed
linear_speed = 0.2
angular_speed = 0.0

while True:
    # Read sensor data
    sensors = kobuki.read_sensor_data()

    # If a bumper is pressed, reverse and rotate
    if sensors['bumper_left'] or sensors['bumper_center'] or sensors['bumper_right']:
        print("Bumper pressed! Reversing and rotating.")
        kobuki.move(-linear_speed, 3.14 / 1.8)  # Reverse and rotate
        time.sleep(2)

    # If a cliff is detected, stop and reverse
    elif sensors['cliff_left'] or sensors['cliff_center'] or sensors['cliff_right']:
        print("Cliff detected! Reversing.")
        kobuki.move(-linear_speed, 0.0)  # Reverse without rotation
        time.sleep(1)

    # Continue moving forward
    else:
        kobuki.move(linear_speed, angular_speed)
    time.sleep(0.1)
