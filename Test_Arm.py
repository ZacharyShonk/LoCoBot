from WidowX_Arm_Module import WidowX200Arm
import time

# Startup the arm (default device: "/dev/ttyUSB1")
arm = WidowX200Arm(dev_port="/dev/ttyUSB1", baud_rate=1000000)

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