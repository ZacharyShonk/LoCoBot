from WidowX_Arm_Module import WidowX200Arm
import time

ROBOT_SPEED = 0.2

arm = WidowX200Arm(dev_port="/dev/ttyUSB1", baud_rate=1000000)

WORKSPACE_LIMITS = arm.WORKSPACE_LIMITS
JOINT_LIMITS = arm.JOINT_LIMITS

def MoveArm(x, y, z, pitch, roll, speed):
    perc_x = x
    perc_y = y
    perc_z = z

    target_x = WORKSPACE_LIMITS['x'][0] + (perc_x / 100.0) * (WORKSPACE_LIMITS['x'][1] - WORKSPACE_LIMITS['x'][0])
    target_y = WORKSPACE_LIMITS['y'][0] + (perc_y / 100.0) * (WORKSPACE_LIMITS['y'][1] - WORKSPACE_LIMITS['y'][0])
    target_z = WORKSPACE_LIMITS['z'][0] + (perc_z / 100.0) * (WORKSPACE_LIMITS['z'][1] - WORKSPACE_LIMITS['z'][0])

    print(f"Computed target coordinates: x={target_x:.3f}, y={target_y:.3f}, z={target_z:.3f}")

    ik_solution = arm.inverse_kinematics(target_x, target_y, target_z, pitch, roll)

    if ik_solution is None:
        print("No valid IK solution for the given target.")
    else:
        print("Computed joint angles (degrees):")
        for joint, angle in zip(["waist", "shoulder", "elbow", "wrist_angle", "wrist_rotate"], ik_solution):
            print(f"  {joint}: {angle:.2f}")

        for joint, angle in zip(["waist", "shoulder", "elbow", "wrist_angle", "wrist_rotate"], ik_solution):
            arm.move_joint(joint, angle, speed)

def Gripper(Position):
    if Position >= JOINT_LIMITS["gripper"][1]:
        Position = JOINT_LIMITS["gripper"][1]
    elif Position <= JOINT_LIMITS["gripper"][0]:
        Position = JOINT_LIMITS["gripper"][0]
    else:
        Position = Position
    arm.move_joint("gripper", Position, 800)

time.sleep(2)

arm.Zero()

time.sleep(1)

MoveArm(100, 50, 100, 0, 0, 500)
time.sleep(0.2)
MoveArm(80, 100, 50, 30, 0, 1000)
time.sleep(0.4)
MoveArm(90, 100, 40, 30, 0, 1000)
time.sleep(0.3)
MoveArm(100, 50, 100, 0, 0, 500)
time.sleep(0.4)
MoveArm(100, 50, 100, 0, 0, 500)
time.sleep(0.4)
MoveArm(100, 0, 100, 0, 0, 500)
time.sleep(0.2)
MoveArm(80, 100, 50, 30, 0, 1000)
time.sleep(0.4)
MoveArm(90, 50, 40, 30, 0, 1000)


