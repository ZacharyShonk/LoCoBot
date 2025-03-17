# WidowX 200 Arm Module:
## Overview
This is a module built to allow for movement of the arm.

## Usage
After setting up the robot you can use the module as follows:

```python
from WidowX_Arm_Module import WidowX200Arm
import time

# Startup the arm (default device: "/dev/ttyUSB1")
arm = WidowX200Arm(dev_port="/dev/ttyUSB1", baud_rate=1000000)

#Turns on the Arm Servos
arm.enable()

# Set the speed of all the motors - wont effect commands the change the speed
# Higher number - slower (0, 1023)
arm.set_all_speed(800)

# Tucks the arm under the camera
arm.Tuck() 

time.sleep(1)

# Uses % of max position to move the arm in X(Forwards/Backwards), Y(Base Turn Left/Right)
#Z(Up/Down), Pitch(Gripper Up/Down), Roll (Gripper Roll), Speed(0, 1023 Higher - slower)
arm.MoveArm(True, 100,50, 30, 0, 0, 800)

time.sleep(1)

# Zeros the arm to all of the servos default values
arm.Zero()

time.sleep(0.5)

arm.MoveArm(False, 0.3,80, 0.3, 0, 0, 800) 

time.sleep(1)

# Moves the joint to position 0, based on joint name
arm.move_joint("waist", 0, 500)

# Sets the gripper to a position stated or clamps to limit if passed limit
arm.Gripper(-41)

time.sleep(0.3)

arm.Tuck()

time.sleep(0.5)

# Shutsdown the arm
arm.shutdown()
```

## API Reference

### `WidowX_Arm_Module.WidowX200Arm`
#### Constructor
```python
variable = WidowX200Arm(dev_port="/dev/ttyUSB1", baud_rate=1000000)
```
Initializes a connection to the Arm.
- `dev_port`: Path to the serial port where the robot is connected (default: `"/dev/ttyUSB1"`).

#### Methods

```python
variable.enable()
```
Turns on the arms servos

```python
variable.MoveArm(use_percent: bool,x: float,y: float, z: float, pitch: int, roll: int, speed: int)
```
Commands the arm to move with specified velocities and positions.
- `use_percent`: Determines whether you want to use position in meters or percent of max
- `x`: Position in % of max or meters
- `y`: Position in % of max 
- `z`: Position in % of max or meters
- `pitch`: Position of pitch (gripper up/down)
- `roll`: Position of pitch (gripper roll)

```python
variable.Tuck()
```
Causes the arm to reset to the joints default positions

```python
variable.set_all_speed(speed: int)
```
Sets the speed of all joints
- `speed`: an number in between 0 and 1023 with the higher number being slower

```python
variable.move_joint(joint_name: str, position: float, speed: int)
```
Moves a specific joint, using its name to a determined position
- `joint_name`: Name of the joint (found in the module)
- `position`: the position or degree of determined motor to be moved to (limits found in module)
- `speed`: an number in between 0 and 1023 with the higher number being slower

```python
variable.Gripper(position: float)
```
Moves the gripper inwards and outwards based on position given
- `position`: the position of the gripper to be moved to (limits found in module)

```python
variable.shutdown()
```
Turns off the servos on the arm (only do this when it is in a safe position, or it can risk damaging the arm.)
