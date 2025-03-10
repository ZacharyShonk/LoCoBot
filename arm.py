import time
from dynamixel_sdk import *  # Dynamixel SDK
import random

# -------------------- CONFIGURATION --------------------

# WidowX 200 Serial Port (Change if necessary)
DEV_PORT = "/dev/ttyUSB1"  # Change for Windows: "COMX"
BAUD_RATE = 1000000  # XL-320 operates at 1 Mbps by default

# Dynamixel Protocol Version (XL-320 uses v2.0)
PROTOCOL_VERSION = 2.0

# Joint IDs Mapping
JOINT_IDS = {
    "waist": 1,
    "shoulder": (2, 3),  # Shoulder joint consists of two servos
    "elbow": 4,
    "wrist_angle": 5,
    "wrist_rotate": 6,
    "gripper": 7,
}

ADDR_TORQUE_ENABLE = 64       # Torque Enable address for Protocol 2.0
ADDR_GOAL_VELOCITY = 112      # Goal Velocity (speed control) register (4 bytes)
ADDR_GOAL_POSITION = 116      # Goal Position (4 bytes)
ADDR_PRESENT_POSITION = 132   # Present Position (4 bytes)
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

# Conversion Constants
DYNAMIXEL_MIN = 0
DYNAMIXEL_MAX = 4095
DEGREE_TO_POSITION = DYNAMIXEL_MAX / 360.0
POSITION_TO_DEGREE = 360.0 / DYNAMIXEL_MAX

# Define position limits for each joint in degrees
JOINT_LIMITS = {
    "waist": (-180, 180),
    "shoulder": (-108, 113),
    "elbow": (-108, 93),
    "wrist_angle": (-100, 123),
    "wrist_rotate": (-180, 180),
    "gripper": (-40, 55),  # Gripper in mm
}

# -------------------- INITIALIZATION --------------------

# Initialize Port Handler & Packet Handler
port_handler = PortHandler(DEV_PORT)
packet_handler = PacketHandler(PROTOCOL_VERSION)

# Open Serial Port
if not port_handler.openPort():
    print("Error: Failed to open serial port!")
    exit()
if not port_handler.setBaudRate(BAUD_RATE):
    print("Error: Failed to set baud rate!")
    exit()
print(f"Serial port opened at {BAUD_RATE} bps.")

# Enable torque for each joint
for joint, ids in JOINT_IDS.items():
    if isinstance(ids, tuple):
        for servo_id in ids:
            if servo_id == 3:
                packet_handler.write1ByteTxRx(port_handler, servo_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
            else:
                packet_handler.write1ByteTxRx(port_handler, servo_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    else:
        packet_handler.write1ByteTxRx(port_handler, ids, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
print("Arm joints are enabled.")

# -------------------- MOTOR CONTROL FUNCTIONS --------------------

def degrees_to_position(degrees):
    return int((degrees + 180) * DEGREE_TO_POSITION)

def position_to_degrees(position):
    return (position * POSITION_TO_DEGREE) - 180

def set_speed(servo_id, speed):
    print(f"Set servo speed for {servo_id} to {speed}")
    packet_handler.write4ByteTxRx(port_handler, servo_id, ADDR_GOAL_VELOCITY, int(speed))

def set_position(servo_id, position):
    print(f"Set servo location for {servo_id} to {position}")
    packet_handler.write4ByteTxRx(port_handler, servo_id, ADDR_GOAL_POSITION, position)

def move_joint(joint, degrees, speed=500):
    """Move a joint to the specified position in degrees if it's within the allowed range."""
    if joint in JOINT_LIMITS:
        min_deg, max_deg = JOINT_LIMITS[joint]
        if min_deg <= degrees <= max_deg:
            position = degrees_to_position(degrees)
            speed = max(0, min(speed, 1023))  # Ensure speed is within range

            if isinstance(JOINT_IDS[joint], tuple):  # Handle shoulder (dual servo)
                mirror_position = DYNAMIXEL_MAX - position
                for servo_id in JOINT_IDS[joint]:
                    set_speed(servo_id, speed)
                    set_position(servo_id, position if servo_id == JOINT_IDS[joint][0] else mirror_position)
            else:
                servo_id = JOINT_IDS[joint]
                set_speed(servo_id, speed)
                set_position(servo_id, position)

            print(f"Joint {joint} moving to {degrees} degrees at speed {speed}.")
        else:
            print(f"Error: Joint {joint} position {degrees} out of range ({min_deg}-{max_deg}).")
    else:
        print(f"Error: No limits defined for joint {joint}.")

def read_joint_position(joint):
    """Reads and returns the current position of a joint in degrees."""
    if isinstance(JOINT_IDS[joint], tuple):  # Handle shoulder (dual servo)
        position, _, _ = packet_handler.read2ByteTxRx(port_handler, JOINT_IDS[joint][0], ADDR_PRESENT_POSITION)
    else:
        position, _, _ = packet_handler.read2ByteTxRx(port_handler, JOINT_IDS[joint], ADDR_PRESENT_POSITION)
    return position_to_degrees(position)

def cycle_joint(joint, min_deg, max_deg, start_speed=100, end_speed=1023, cycles=20):
    """Cycle a joint between min_deg and max_deg dynamically, waiting for movement completion."""
    for cycle in range(cycles):
        current_speed = int(start_speed + ((end_speed - start_speed) * (cycle / (cycles - 1))))
        min_pos = degrees_to_position(min_deg)
        max_pos = degrees_to_position(max_deg)

        servo_ids = JOINT_IDS[joint]
        if isinstance(servo_ids, tuple):  # Handle shoulder (dual servo)
            for servo_id in servo_ids:
                packet_handler.write4ByteTxRx(port_handler, servo_id, ADDR_GOAL_VELOCITY, current_speed)
            packet_handler.write4ByteTxRx(port_handler, servo_ids[0], ADDR_GOAL_POSITION, min_pos)
            packet_handler.write4ByteTxRx(port_handler, servo_ids[1], ADDR_GOAL_POSITION, DYNAMIXEL_MAX - min_pos)
            wait_for_movement(servo_ids[0], min_pos)
        else:
            packet_handler.write4ByteTxRx(port_handler, servo_ids, ADDR_GOAL_VELOCITY, current_speed)
            packet_handler.write4ByteTxRx(port_handler, servo_ids, ADDR_GOAL_POSITION, min_pos)
            wait_for_movement(servo_ids, min_pos)

        packet_handler.write4ByteTxRx(port_handler, servo_ids, ADDR_GOAL_POSITION, max_pos)
        wait_for_movement(servo_ids, max_pos)

def wait_for_movement(servo_id, target_position, tolerance=10):
    """Waits until the servo reaches the target position within a tolerance."""
    while True:
        current_position, _, _ = packet_handler.read4ByteTxRx(port_handler, servo_id, ADDR_PRESENT_POSITION)
        if abs(current_position - target_position) <= tolerance:
            break
        time.sleep(0.1)  # Check every 50ms
        
# -------------------- EXECUTION --------------------

if __name__ == "__main__":
    while True:
        for servo_id in range(1, 10):  # Adjust range if necessary
            if True:
                dxl_model_number, dxl_comm_result, dxl_error = packet_handler.ping(port_handler, servo_id)
                if dxl_comm_result == COMM_SUCCESS:
                    print(f"Servo ID {servo_id} is active. Model Number: {dxl_model_number}")


        print("\nOptions:")
        print("1. Read joint position")
        print("2. Set joint position")
        print("3. Exit")
        print("4. Get array of angles")
        print("5. Random")
        print("6. Cycle Joint")
        print("7. Zero robot")
        choice = input("Select an option: ")
        
        if choice == "1":
            joint = input("Enter joint name (waist, shoulder, elbow, wrist_angle, wrist_rotate): ")
            if joint in JOINT_IDS:
                print(f"Joint {joint} position: {read_joint_position(joint)} degrees")
            else:
                print("Invalid joint name.")
        elif choice == "2":
            joint = input("Enter joint name (waist, shoulder, elbow, wrist_angle, wrist_rotate): ")
            if joint in JOINT_IDS:
                degrees = int(input("Enter position in degrees: "))
                speed = int(input("Speed (0-1023) >> "))
                move_joint(joint, degrees, speed=speed)
            else:
                print("Invalid joint name.")
        elif choice == "3":
            break
        elif choice == "4":
            joints = ["waist", "shoulder", "elbow", "wrist_angle", "wrist_rotate"]

            joint_angles = []
            for joint in joints:
                joint_angles.append(read_joint_position(joint))
            print(joint_angles)
        elif choice == "5":
            while True:
                random_joint_limits = {
                    "waist": (-90, 90),
                    "shoulder": (-30, 30),
                    "elbow": (-20, 20),
                    "wrist_angle": (0, 123),
                    "wrist_rotate": (-180, 180),
                    # "gripper": (-40, 55),  # Gripper in mm
                }

                joint_name = random.choice(list(random_joint_limits.keys()))
                joint_range = random_joint_limits[joint_name]
                random_angle = int(random.uniform(joint_range[0], joint_range[1]))
                random_speed = int(random.uniform(0, 1023))

                print(f"Joint: {joint_name}")
                print(f"Random Angle: {random_angle:.2f}")
                print(f"Random value: {random_speed:.2f}")

                move_joint(joint_name, random_angle, speed=random_speed)
                time.sleep(1)
        elif choice == "6":
            joint = input("Enter joint name to cycle (waist, shoulder, elbow, wrist_angle, wrist_rotate): ")
            if joint in JOINT_IDS:
                min_deg = int(input("Enter minimum degree: "))
                max_deg = int(input("Enter maximum degree: "))
                start_speed = int(input("Enter starting speed (0-1023): "))
                end_speed = int(input("Enter ending speed (0-1023): "))
                cycle_joint(joint, min_deg, max_deg, start_speed, end_speed)
            else:
                print("Invalid joint name.")
        elif choice == "7":
            joints = ["waist", "shoulder", "elbow", "wrist_angle", "wrist_rotate"]

            for joint in joints:
                move_joint(joint, 0)
        else:
            print("Invalid choice, try again.")

# Close Serial Connection
port_handler.closePort()
print("Serial port closed.")
