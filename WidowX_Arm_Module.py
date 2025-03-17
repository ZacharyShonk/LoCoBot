import time
import math
from dynamixel_sdk import *  # Dynamixel SDK

class WidowX200Arm:
    def __init__(self, dev_port="/dev/ttyUSB1", baud_rate=1000000, protocol_version=2.0):
        # Configuration Constants
        self.DEV_PORT = dev_port
        self.BAUD_RATE = baud_rate
        self.PROTOCOL_VERSION = protocol_version

        # Joint IDs Mapping
        self.JOINT_IDS = {
            "waist": 1,
            "shoulder": (2, 3),  # Shoulder joint consists of two servos (mirror configuration)
            "elbow": 4,
            "wrist_angle": 5,
            "wrist_rotate": 6,
            "gripper": 7,
            "Camera_Waist": 8,
            "Camera_Wrist": 9,
        }

        # Addresses for Dynamixel protocol
        self.ADDR_TORQUE_ENABLE = 64
        self.ADDR_GOAL_VELOCITY = 112
        self.ADDR_GOAL_POSITION = 116
        self.ADDR_PRESENT_POSITION = 132
        self.TORQUE_ENABLE = 1
        self.TORQUE_DISABLE = 0

        # Conversion Constants
        self.DYNAMIXEL_MIN = 0
        self.DYNAMIXEL_MAX = 4095
        self.DEGREE_TO_POSITION = self.DYNAMIXEL_MAX / 360.0
        self.POSITION_TO_DEGREE = 360.0 / self.DYNAMIXEL_MAX

        # Define position limits for each joint in degrees
        self.WORKSPACE_LIMITS = {
            'x': (0.0, 0.3491386428374851),
            'y': (-0.3, 0.3),
            'z': (0.1, 0.26922206196312054)
        }

        self.JOINT_LIMITS = {
            "waist": (-100, 100),
            "shoulder": (-108, 113),
            "elbow": (-90, 90),
            "wrist_angle": (-100, 123),
            "wrist_rotate": (-180, 180),
            "gripper": (-40, 55),  # Gripper in mm
            "Camera_Waist": (-90, 90),
            "Camera_Wrist": (-90, 45),
        }

        self.port_handler = PortHandler(self.DEV_PORT)
        self.packet_handler = PacketHandler(self.PROTOCOL_VERSION)

        if not self.port_handler.openPort():
            print("Error: Failed to open serial port!")
            exit()
        if not self.port_handler.setBaudRate(self.BAUD_RATE):
            print("Error: Failed to set baud rate!")
            exit()
        print(f"Serial port opened at {self.BAUD_RATE} bps.")

    def degrees_to_position(self, degrees):
        return int((degrees + 180) * self.DEGREE_TO_POSITION)

    def position_to_degrees(self, position):
        return (position * self.POSITION_TO_DEGREE) - 180

    def set_all_speed(self, speed):
        for joint_name, joint_id in self.JOINT_IDS.items():
            if isinstance(joint_id, tuple):  
                for id in joint_id:
                    self.packet_handler.write4ByteTxRx(
                        self.port_handler, id, self.ADDR_GOAL_VELOCITY, int(speed)
                    )
            else:
                self.packet_handler.write4ByteTxRx(
                    self.port_handler, joint_id, self.ADDR_GOAL_VELOCITY, int(speed)
                )

    def set_speed(self, servo_id, speed):
        self.packet_handler.write4ByteTxRx(self.port_handler, servo_id, self.ADDR_GOAL_VELOCITY, int(speed))

    def set_position(self, servo_id, position):
        self.packet_handler.write4ByteTxRx(self.port_handler, servo_id, self.ADDR_GOAL_POSITION, position)

    def move_joint(self, joint, degrees, speed):
        if joint in self.JOINT_LIMITS:
            min_deg, max_deg = self.JOINT_LIMITS[joint]

            if degrees < min_deg:
                degrees = min_deg
                print(f"Warning: Clamped {joint} to {min_deg}° (out of range).")
            elif degrees > max_deg:
                degrees = max_deg
                print(f"Warning: Clamped {joint} to {max_deg}° (out of range).")

            position = self.degrees_to_position(degrees)
            speed = max(0, min(speed, 1023))

            if isinstance(self.JOINT_IDS[joint], tuple):
                mirror_position = self.DYNAMIXEL_MAX - position
                for servo_id in self.JOINT_IDS[joint]:
                    self.set_speed(servo_id, speed)
                    if servo_id == self.JOINT_IDS[joint][0]:
                        self.set_position(servo_id, position)
                    else:
                        self.set_position(servo_id, mirror_position)
            else:
                servo_id = self.JOINT_IDS[joint]
                self.set_speed(servo_id, speed)
                self.set_position(servo_id, position)

            print(f"Joint {joint} moving to {degrees}° at speed {speed}.")
        else:
            print(f"Error: No limits defined for joint {joint}.")

    def read_joint_position(self, joint):
        if isinstance(self.JOINT_IDS[joint], tuple):
            position, _, _ = self.packet_handler.read2ByteTxRx(self.port_handler, self.JOINT_IDS[joint][0], self.ADDR_PRESENT_POSITION)
        else:
            position, _, _ = self.packet_handler.read2ByteTxRx(self.port_handler, self.JOINT_IDS[joint], self.ADDR_PRESENT_POSITION)
        return self.position_to_degrees(position)
    
    def read_all_joint_positions(self):
        for joint_name, joint_id in self.JOINT_IDS.items():
            if isinstance(joint_id, tuple):  
                for id in joint_id:
                    position = self.read_joint_position(joint_name)
                    print(f"{joint_name} (ID: {id}): {position} degrees")
            else:
                position = self.read_joint_position(joint_name)
                print(f"{joint_name}: {position} degrees")

    def Zero(self):
        for joint in ["waist", "shoulder", "elbow", "wrist_angle", "wrist_rotate"]:
            self.move_joint(joint, 0, 1000)

    def inverse_kinematics(self, x, y, z, pitch_deg, roll_deg=0):
        pitch = math.radians(pitch_deg)
        roll  = math.radians(roll_deg)
        
        q1 = math.atan2(y, x)
        r = math.sqrt(x**2 + y**2)
        
        d5 = 0.05  # End-effector offset in meters
        L1 = 0.2   # Shoulder-to-elbow length (meters)
        L2 = 0.2   # Elbow-to-wrist center length (meters)
        
        wrist_r = r - d5 * math.cos(pitch)
        wrist_z = z - d5 * math.sin(pitch)
        D = math.sqrt(wrist_r**2 + wrist_z**2)
        
        min_D = abs(L1 - L2)
        max_D = L1 + L2
        
        if D > max_D or D < min_D:
            if D > max_D:
                ratio = max_D / D
            else:
                ratio = min_D / D
            wrist_r *= ratio
            wrist_z *= ratio
            D = math.sqrt(wrist_r**2 + wrist_z**2)
        
        cos_angle = (wrist_r**2 + wrist_z**2 - L1**2 - L2**2) / (2 * L1 * L2)
        cos_angle = max(min(cos_angle, 1), -1)
        q3 = math.acos(cos_angle)
        
        q2 = math.atan2(wrist_z, wrist_r) - math.atan2(L2 * math.sin(q3), L1 + L2 * math.cos(q3))
        
        q4 = pitch - (q2 + q3)
        
        q5 = roll

        q1_deg = math.degrees(q1)
        q2_deg = math.degrees(q2)
        q3_deg = math.degrees(q3)
        q4_deg = math.degrees(q4)
        q5_deg = math.degrees(q5)

        print(f"Inverse Kinematics Solution: q1={q1_deg}, q2={q2_deg}, q3={q3_deg}, q4={q4_deg}, q5={q5_deg}")
        return q1_deg, q2_deg, q3_deg, q4_deg, q5_deg
    
    def MoveArm(self, use_percent, x, y, z, pitch, roll, speed):


        if use_percent:
            target_x = self.WORKSPACE_LIMITS['x'][0] + (x / 100.0) * (self.WORKSPACE_LIMITS['x'][1] - self.WORKSPACE_LIMITS['x'][0])
            target_y = self.WORKSPACE_LIMITS['y'][0] + (y / 100.0) * (self.WORKSPACE_LIMITS['y'][1] - self.WORKSPACE_LIMITS['y'][0])
            target_z = self.WORKSPACE_LIMITS['z'][0] + (z / 100.0) * (self.WORKSPACE_LIMITS['z'][1] - self.WORKSPACE_LIMITS['z'][0])
        else:
            target_x = x
            target_y = self.WORKSPACE_LIMITS['y'][0] + (y / 100.0) * (self.WORKSPACE_LIMITS['y'][1] - self.WORKSPACE_LIMITS['y'][0])
            target_z = z

        print(f"Computed target coordinates: x={target_x:.3f}, y={target_y:.3f}, z={target_z:.3f}")

        ik_solution = self.inverse_kinematics(target_x, target_y, target_z, pitch, roll)

        if ik_solution is None:
            print("No valid IK solution for the given target.")
        else:
            print("Computed joint angles (degrees):")
            for joint, angle in zip(["waist", "shoulder", "elbow", "wrist_angle", "wrist_rotate"], ik_solution):
                print(f"  {joint}: {angle:.2f}")

            for joint, angle in zip(["waist", "shoulder", "elbow", "wrist_angle", "wrist_rotate"], ik_solution):
                self.move_joint(joint, angle, speed)

    def Gripper(self, Position):
        if Position >= self.JOINT_LIMITS["gripper"][1]:
            Position = self.JOINT_LIMITS["gripper"][1]
        elif Position <= self.JOINT_LIMITS["gripper"][0]:
            Position = self.JOINT_LIMITS["gripper"][0]
        else:
            Position = Position
        self.move_joint("gripper", Position, 800)

    def Tuck(self):
        self.Zero()
        time.sleep(2)

        self.move_joint("waist", -1.8021978021977816, 1000)
        time.sleep(0.6)
        self.move_joint("shoulder", -76.7032967032967, 1000)
        self.move_joint("elbow", 96.74725274725279, 1000)
        self.move_joint("wrist_angle", 30.373626373626394, 1000)
        self.move_joint("wrist_rotate", 0, 1000)

    def shutdown(self):
        for joint, ids in self.JOINT_IDS.items():
            if isinstance(ids, tuple):
                for servo_id in ids:
                    if servo_id == 3:
                        self.packet_handler.write1ByteTxRx(self.port_handler, servo_id, self.ADDR_TORQUE_ENABLE, self.TORQUE_DISABLE)
                    else:
                        self.packet_handler.write1ByteTxRx(self.port_handler, servo_id, self.ADDR_TORQUE_ENABLE, self.TORQUE_DISABLE)
            else:
                self.packet_handler.write1ByteTxRx(self.port_handler, ids, self.ADDR_TORQUE_ENABLE, self.TORQUE_DISABLE)

    def enable(self):
        for joint, ids in self.JOINT_IDS.items():
            if isinstance(ids, tuple):
                for servo_id in ids:
                    if servo_id == 3:
                        self.packet_handler.write1ByteTxRx(self.port_handler, servo_id, self.ADDR_TORQUE_ENABLE, self.TORQUE_DISABLE)
                    else:
                        self.packet_handler.write1ByteTxRx(self.port_handler, servo_id, self.ADDR_TORQUE_ENABLE, self.TORQUE_ENABLE)
            else:
                self.packet_handler.write1ByteTxRx(self.port_handler, ids, self.ADDR_TORQUE_ENABLE, self.TORQUE_ENABLE)
