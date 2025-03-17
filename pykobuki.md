
# PyKobuki: Python Wrapper for the Kobuki Robot

## Overview
PyKobuki is a Python wrapper to use Kobuki base.

## Usage
After building and installing the module, you can use `pykobuki` in your Python scripts as follows:

```python
import pykobuki
import time

# Initialize the robot (default device: "/dev/kobuki")
kobuki = pykobuki.Kobuki()

# Move forward at 0.1 m/s with no rotation
kobuki.move(0.1, 0.0)

# Sleep for 2 seconds
time.sleep(2)

# Read sensor data
sensors = kobuki.read_sensor_data()
print(sensors)

# Shutdown the robot
kobuki.shutdown()
```

## API Reference

### `pykobuki.Kobuki`
#### Constructor
```python
Kobuki(device: str = "/dev/kobuki")
```
Initializes a connection to the Kobuki robot.
- `device`: Path to the serial port where the robot is connected (default: `"/dev/kobuki"`).

#### Methods

```python
move(linear: float, angular: float)
```
Commands the robot to move with specified velocities.
- `linear`: Linear velocity (m/s)
- `angular`: Angular velocity (rad/s)

```python
read_sensor_data() -> dict
```
Retrieves sensor data from the robot and returns it as a dictionary containing:
- `time_stamp`: Timestamp of the data
- `bumper`: Bumper sensor status
- `wheel_drop`: Wheel drop sensor status
- `cliff`: Cliff sensor status
- `left_encoder`, `right_encoder`: Wheel encoders
- `left_pwm`, `right_pwm`: Motor PWM values
- `buttons`: Button press states
- `charger`: Charging status
- `battery`: Battery voltage (formatted to two decimal places)
- `over_current`: Overcurrent status

```python
shutdown()
```
Stops the robot and disables it.

## Advanced Examples

### Example 1: **Dynamic Path Following with Bumper and Cliff Sensors**

This example demonstrates how the robot can follow a dynamic path while avoiding obstacles using bumper and cliff sensors. If the robot detects an obstacle or a cliff, it will take corrective actions, such as rotating or reversing.

```python
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
```

### Example 2: **Battery Voltage Logging and Shutdown on Low Battery**

This example continuously monitors the robot’s battery voltage and logs it. If the voltage falls below a certain threshold, the robot will shut down.

```python
import pykobuki
import time

# Initialize the robot
kobuki = pykobuki.Kobuki()

# Set a low battery threshold (e.g., 14.0V)
low_battery_threshold = 14.0

# Open a file to log battery status
with open("battery_log.txt", "w") as log_file:
    while True:
        # Read sensor data
        sensors = kobuki.read_sensor_data()
        
        # Log battery voltage
        battery_voltage = float(sensors['battery_voltage'])
        log_file.write(f"Battery voltage: {battery_voltage}V")
        
        # Print the battery status
        print(f"Battery voltage: {battery_voltage}V")

        # If battery voltage is below the threshold, shut down the robot
        if battery_voltage < low_battery_threshold:
            print("Low battery! Shutting down.")
            kobuki.shutdown()
            break
        
        # Sleep for a while before checking again
        time.sleep(5)
```

### Example 3: **Continuous Movement with Obstacle Avoidance**

In this example, the robot will continuously move forward at a set speed while avoiding obstacles. When an obstacle is detected, the robot will back up and rotate, then resume its forward motion.

```python
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

    # If any bumper is pressed, reverse and rotate
    if sensors['bumper_left'] or sensors['bumper_center'] or sensors['bumper_right']:
        print("Bumper pressed! Reversing and rotating.")
        kobuki.move(-linear_speed, 3.14 / 1.8)  # Reverse and rotate
        time.sleep(2)

    # If a cliff is detected, stop and reverse
    elif sensors['cliff_left'] or sensors['cliff_center'] or sensors['cliff_right']:
        print("Cliff detected! Reversing.")
        kobuki.move(-linear_speed, 0.0)  # Reverse without rotation
        time.sleep(1)

    # Continue moving forward if no obstacle is detected
    else:
        kobuki.move(linear_speed, angular_speed)
    
    # Pause for a short time to allow sensor data to update
    time.sleep(0.1)
```

### Example 4: **Random Movement with Obstacle Avoidance**

This example demonstrates the robot moving randomly in different directions while avoiding obstacles and cliffs. The robot will stop momentarily, choose a new random direction, and proceed.

```python
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
```

### Example 5: **Timed Rotation with Bumper Check**

This example rotates the robot for a specific time and checks for bumpers during the rotation. If a bumper is pressed, the robot will stop and reverse, then resume the rotation.

```python
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
```

