# THIS IS BEING HEAVILY REWRITTEN CURRENTLY

import time
from dynamixel_sdk import *  # Dynamixel SDK
import random

# -------------------- CONFIGURATION --------------------

# WidowX 200 Serial Port (Change if necessary)
DEV_PORT = "/dev/ttyUSB1"  # Change for Windows: "COMX"
BAUD_RATE = 1000000  # XL-320 operates at 1 Mbps by default

# Dynamixel Protocol Version (XL-320 uses v2.0)
PROTOCOL_VERSION = 2.0

# Dynamixel Motor IDs (Change according to your setup)
DXL_IDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # Adjust if needed

ADDR_TORQUE_ENABLE = 64       # Torque Enable address for Protocol 2.0
ADDR_GOAL_VELOCITY = 112      # New: Goal Velocity (speed control) register (4 bytes)
ADDR_GOAL_POSITION = 116      # Goal Position (4 bytes)
ADDR_PRESENT_POSITION = 132   # Present Position (4 bytes)
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

# New global speed setting (can be updated at runtime)
DEFAULT_SPEED = 100  # Adjust as needed

# Define position limits for each servo to prevent overextension
SERVO_LIMITS = {
    0: (0, 4096),
    1: (685, 3325),
    2: (1700, 3357), # 735
    3: (739, 3360),  # Servo 3 mirrors Servo 2
    4: (939, 3275),
    5: (622, 3234),
    6: (2081-600, 2081+600),
    7: (2068, 2953),
    8: (0, 4096),
    9: (0, 4096),
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

# Enable torque for each motor
for dxl_id in DXL_IDS:
    dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(
        port_handler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Error enabling torque for Motor {dxl_id}: {packet_handler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error:
        print(f"Motor {dxl_id} Error: {packet_handler.getRxPacketError(dxl_error)}")

print("Arm motors are enabled.")

# -------------------- MOTOR CONTROL FUNCTIONS --------------------

def move_motor(dxl_id, position, speed=None):
    """Move the motor to the specified position at the given speed if it's within its allowed range."""
    if speed is None:
        speed = DEFAULT_SPEED
    if dxl_id in SERVO_LIMITS:
        min_pos, max_pos = SERVO_LIMITS[dxl_id]
        if min_pos <= position <= max_pos:
            # Set motor speed first
            dxl_comm_result, dxl_error = packet_handler.write4ByteTxRx(
                port_handler, dxl_id, ADDR_GOAL_VELOCITY, speed)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Motor {dxl_id} Speed Error: {packet_handler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error:
                print(f"Motor {dxl_id} Speed Error: {packet_handler.getRxPacketError(dxl_error)}")
            else:
                print(f"Motor {dxl_id} set to speed {speed}.")
            # Now move to the desired position
            dxl_comm_result, dxl_error = packet_handler.write4ByteTxRx(
                port_handler, dxl_id, ADDR_GOAL_POSITION, position)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Motor {dxl_id} Position Error: {packet_handler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error:
                print(f"Motor {dxl_id} Position Error: {packet_handler.getRxPacketError(dxl_error)}")
            else:
                print(f"Motor {dxl_id} moving to position {position}.")
        else:
            print(f"Motor {dxl_id} Error: Position {position} out of range ({min_pos}-{max_pos}).")
    else:
        print(f"Motor {dxl_id} Error: No limits defined.")

def read_motor_position(dxl_id):
    """Reads and returns the current position of a Dynamixel motor."""
    position, result, error = packet_handler.read2ByteTxRx(port_handler, dxl_id, ADDR_PRESENT_POSITION)
    if result != COMM_SUCCESS:
        print(f"Motor {dxl_id}: {packet_handler.getTxRxResult(result)}")
    elif error:
        print(f"Motor {dxl_id}: {packet_handler.getRxPacketError(error)}")
    return position

def set_servos(servo_status=TORQUE_DISABLE):
    """Enable or disable torque for all servos."""
    for dxl_id in DXL_IDS:
        packet_handler.write1ByteTxRx(port_handler, dxl_id, ADDR_TORQUE_ENABLE, servo_status)
        print(f"Motor {dxl_id} torque {'enabled' if servo_status == TORQUE_ENABLE else 'disabled'}.")

def replayer():
    """Record and replay motor positions."""
    set_servos(TORQUE_DISABLE)
    time.sleep(5)
    
    saved_position = []
    for DXL_ID in DXL_IDS:
        saved_position.append(read_motor_position(DXL_ID))

    print("Position Saved:", saved_position)
    time.sleep(5)
    
    set_servos(TORQUE_ENABLE)

    for i, pos in enumerate(saved_position):
        move_motor(DXL_IDS[i], pos)

def create_sequence(movements):
    """Execute a sequence of movements for multiple servos."""
    for movement in movements:
        for motor_id, position in movement.items():
            move_motor(motor_id, position)
        time.sleep(1)  # Delay between steps

def set_servos_to_middle():
    """Move all servos to the middle of their allowed range, ensuring correct math for servo 2 & 3."""
    for dxl_id, (min_pos, max_pos) in SERVO_LIMITS.items():
        middle_pos = (min_pos + max_pos) // 2  # Calculate middle position
        
        if dxl_id == 2:
            mirror_pos = 4095 - middle_pos  # Servo 3 mirrors Servo 2
            move_motor(2, middle_pos)
            move_motor(3, mirror_pos)
            print(f"Servo 2 set to {middle_pos}, Servo 3 set to {mirror_pos}")
        elif dxl_id != 3:  # Avoid setting Servo 3 separately
            move_motor(dxl_id, middle_pos)
            print(f"Motor {dxl_id} set to middle position: {middle_pos}")

def move_servos_randomly(step_delay=0.5, steps=10):
    """Slowly move servos 0-6 to random positions within their range, ensuring correct math for servos 2 & 3."""
    for _ in range(steps):
        for dxl_id in range(7):  # Only servos 0-6
            min_pos, max_pos = SERVO_LIMITS[dxl_id]
            if dxl_id == 2:
                random_pos = random.randint(min_pos, max_pos)
                mirror_pos = 4095 - random_pos
                move_motor(2, random_pos)
                move_motor(3, mirror_pos)
                print(f"Servo 2 moving to {random_pos}, Servo 3 moving to {mirror_pos}")
            else:
                random_pos = random.randint(min_pos, max_pos)
                move_motor(dxl_id, random_pos)
                print(f"Motor {dxl_id} moving to random position: {random_pos}")
        time.sleep(step_delay)  # Wait before next movement

def move_motor_safe(dxl_id, position, speed=None):
    """Move a motor to a safe position considering axis constraints."""
    if speed is None:
        speed = DEFAULT_SPEED
    # Ensure the motor has defined limits
    if dxl_id in SERVO_LIMITS:
        min_pos, max_pos = SERVO_LIMITS[dxl_id]
        # Special handling for axis-dependent servos
        if dxl_id == 2:  
            # Servo 2 & 3 move opposite each other
            if min_pos <= position <= max_pos:
                mirror_pos = 4095 - position  # Mirror movement for servo 3
                if SERVO_LIMITS[3][0] <= mirror_pos <= SERVO_LIMITS[3][1]:
                    move_motor(2, position, speed)
                    move_motor(3, mirror_pos, speed)
                    print(f"Servo 2 set to {position}, Servo 3 set to {mirror_pos}")
                else:
                    print(f"Error: Mirrored position {mirror_pos} out of range for Servo 3.")
            else:
                print(f"Error: Position {position} out of range for Servo 2.")
        
        elif dxl_id == 4:
            # Servo 4 is constrained with other servos
            safe_range = (SERVO_LIMITS[4][0], SERVO_LIMITS[4][1])  
            if safe_range[0] <= position <= safe_range[1]:
                move_motor(4, position, speed)
                print(f"Servo 4 set to {position}")
            else:
                print(f"Error: Position {position} out of range for Servo 4.")

        else:
            # Normal movement for all other servos
            if min_pos <= position <= max_pos:
                move_motor(dxl_id, position, speed)
                print(f"Motor {dxl_id} set to {position}")
            else:
                print(f"Error: Position {position} out of range for Motor {dxl_id}.")
    else:
        print(f"Motor {dxl_id} Error: No limits defined.")

def set_speed_setting():
    """Prompt the user to update the default motor speed setting."""
    global DEFAULT_SPEED
    try:
        new_speed = int(input("Enter new speed value: "))
        DEFAULT_SPEED = new_speed
        print(f"Default speed updated to {DEFAULT_SPEED}.")
    except ValueError:
        print("Invalid speed value.")

# -------------------- EXECUTION --------------------

if __name__ == "__main__":
    while True:
        print("\nOptions:")
        print("1. Read servo position")
        print("2. Set servo position")
        print("3. Create and run sequence")
        print("4. Run replayer")
        print("5. Exit")
        print("6. Set servos to middle")
        print("7. Random")
        print("8. Set speed")
        choice = input("Select an option: ")
        
        if choice == "1":
            motor_id = int(input("Enter motor ID: "))
            print(f"Motor {motor_id} position: {read_motor_position(motor_id)}")
        elif choice == "2":
            motor_id = int(input("Enter motor ID: "))
            if motor_id == 2 or motor_id == 3:
                print("Setting servo 2 & 3")
                position = int(input("Enter position for servo 2: "))
                position2 = 4095 - position
                print(f"Calculated position for servo 3: {position2}")
                move_motor(2, position)
                move_motor(3, position2)
            else:
                position = int(input("Enter position: "))
                move_motor(motor_id, position)
        elif choice == "3":
            movements = []
            steps = int(input("Enter number of steps in sequence: "))
            for _ in range(steps):
                step = {}
                for motor_id in DXL_IDS:
                    position = int(input(f"Enter position for motor {motor_id}: "))
                    step[motor_id] = position
                movements.append(step)
            create_sequence(movements)
        elif choice == "4":
            replayer()
        elif choice == "5":
            break
        elif choice == "6":
            set_servos_to_middle()
        elif choice == "7":
            move_servos_randomly(step_delay=5)
        elif choice == "8":
            set_speed_setting()
        else:
            print("Invalid choice, try again.")

# Close Serial Connection
port_handler.closePort()
print("Serial port closed.")
