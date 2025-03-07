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
            packet_handler.write1ByteTxRx(port_handler, servo_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    else:
        packet_handler.write1ByteTxRx(port_handler, ids, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
print("Arm joints are enabled.")

# -------------------- MOTOR CONTROL FUNCTIONS --------------------

def degrees_to_position(degrees):
    return int((degrees + 180) * DEGREE_TO_POSITION)

def position_to_degrees(position):
    return (position * POSITION_TO_DEGREE) - 180

def move_joint(joint, degrees, speed=100):
    """Move a joint to the specified position in degrees if it's within the allowed range."""
    if joint in JOINT_LIMITS:
        min_deg, max_deg = JOINT_LIMITS[joint]
        if min_deg <= degrees <= max_deg:
            position = degrees_to_position(degrees)
            if isinstance(JOINT_IDS[joint], tuple):  # Handle shoulder (dual servo)
                mirror_position = DYNAMIXEL_MAX - position
                packet_handler.write4ByteTxRx(port_handler, JOINT_IDS[joint][0], ADDR_GOAL_POSITION, position)
                packet_handler.write4ByteTxRx(port_handler, JOINT_IDS[joint][1], ADDR_GOAL_POSITION, mirror_position)
            else:
                packet_handler.write4ByteTxRx(port_handler, JOINT_IDS[joint], ADDR_GOAL_POSITION, position)
            print(f"Joint {joint} moving to {degrees} degrees.")
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
    """Cycle a joint's position fluidly between min_deg and max_deg 20 times with a speed ramp."""
    for cycle in range(cycles):
        # Gradually increase speed
        current_speed = start_speed + ((end_speed - start_speed) * (cycle / (cycles - 1)))
        move_joint(joint, min_deg, current_speed)
        time.sleep(1)  # Optional delay to let it move to the start position
        move_joint(joint, max_deg, current_speed)
        time.sleep(1)  # Wait for the joint to reach the max position
        move_joint(joint, min_deg, current_speed)  # Reverse to the start position

# -------------------- EXECUTION --------------------

if __name__ == "__main__":
    while True:
        print("\nOptions:")
        print("1. Read joint position")
        print("2. Set joint position")
        print("3. Exit")
        print("4. Get array of angles")
        print("5. Random")
        print("6. Cycle Joint")
        choice = input("Select an option: ")
        
        if choice == "1":
            joint = input("Enter joint name: ")
            if joint in JOINT_IDS:
                print(f"Joint {joint} position: {read_joint_position(joint)} degrees")
            else:
                print("Invalid joint name.")
        elif choice == "2":
            joint = input("Enter joint name: ")
            if joint in JOINT_IDS:
                degrees = int(input("Enter position in degrees: "))
                move_joint(joint, degrees)
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
                random_value = random.uniform(joint_range[0], joint_range[1])

                print(f"Joint: {joint_name}")
                print(f"Random value: {random_value:.2f}")

                move_joint(joint_name, random_value)
                time.sleep(0.3)
        elif choice == "6":
            joint = input("Enter joint name to cycle: ")
            if joint in JOINT_IDS:
                min_deg = int(input("Enter minimum degree: "))
                max_deg = int(input("Enter maximum degree: "))
                start_speed = int(input("Enter starting speed (0-1023): "))
                end_speed = int(input("Enter ending speed (0-1023): "))
                cycle_joint(joint, min_deg, max_deg, start_speed, end_speed)
            else:
                print("Invalid joint name.")

        else:
            print("Invalid choice, try again.")

# Close Serial Connection
port_handler.closePort()
print("Serial port closed.")
