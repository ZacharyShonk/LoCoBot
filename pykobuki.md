# PyKobuki: Python Wrapper for the Kobuki Robot

## Overview
PyKobuki is a Python wrapper to use Kobuki base.

## Usage
After building and installing the module, you can use `pykobuki` in your Python scripts as follows:

```python
import pykobuki

# Initialize the robot (default device: "/dev/kobuki")
kobuki = pykobuki.Kobuki()

# Move forward at 0.1 m/s with no rotation
kobuki.move(0.1, 0.0)

# Sleep for 2 seconds
kobuki.sleep(2)

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
sleep(seconds: float)
```
Causes the program to pause for the specified duration.
- `seconds`: Duration to sleep (in seconds)

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