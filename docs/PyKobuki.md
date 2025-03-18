
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
 - `bumper_left`, `bumper_center`, `bumper_right`: Individual bumper sensor statuses
 - `wheel_drop_left`, `wheel_drop_right`: Wheel drop sensor statuses
 - `cliff_left`, `cliff_center`, `cliff_right`: Cliff sensor statuses
 - `left_encoder`, `right_encoder`: Wheel encoders (counts)
 - `left_pwm`, `right_pwm`: Motor PWM values
 - `button0`, `button1`, `button2`: Button press states
 - `charger_state`: Charging status (integer, 0 = not charging, 1 = charging)
 - `battery_voltage`: Battery voltage (formatted to two decimal places)
 - `overcurrent_left`, `overcurrent_right`: Overcurrent statuses for left and right motors

```python
shutdown()
```
Stops the robot and disables it.

## **Advanced Examples**
Explore the following examples to get started with Kobuki:

- **Dynamic Path Following with Bumper and Cliff Sensors**: Implement dynamic path following while avoiding obstacles using bumper and cliff sensors.
   - [View Python Script](/examples/pykobuki/dynamic_path_following_with_bumper_and_cliff_sensors.py)
   - [Read Explanation](/examples/pykobuki/dynamic_path_following_with_bumper_and_cliff_sensors.md)

- **Continuous Movement with Obstacle Avoidance**: Move continuously while avoiding obstacles using sensor data.
   - [View Python Script](/examples/pykobuki/continuous_movement_with_obstacle_avoidance.py)
   - [Read Explanation](/examples/pykobuki/continuous_movement_with_obstacle_avoidance.md)

- **Random Movement with Obstacle Avoidance**: Perform random movement while avoiding obstacles and cliffs.
   - [View Python Script](/examples/pykobuki/random_movement_with_obstacle_avoidance.py)
   - [Read Explanation](/examples/pykobuki/random_movement_with_obstacle_avoidance.md)

- **Timed Rotation with Bumper Check**: Perform a timed rotation while checking for bumpers and reacting accordingly.
   - [View Python Script](/examples/pykobuki/timed_rotation_with_bumper_check.py)
   - [Read Explanation](/examples/pykobuki/timed_rotation_with_bumper_check.md)
