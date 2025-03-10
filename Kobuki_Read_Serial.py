import serial
import struct
import os

# Configure the serial port
PORT = "/dev/ttyUSB0"  # Adjust based on your setup
BAUDRATE = 115200

def compute_checksum(data):
    """Compute XOR checksum excluding headers (first 2 bytes)."""
    cs = 0
    for byte in data[2:]:  # XOR from index 2 (length + payload)
        cs ^= byte
    return cs

def parse_packet(packet):
    """Parse an incoming packet."""
    if len(packet) < 4:  # Minimum size: headers (2) + length (1) + checksum (1)
        return None

    if packet[0] != 0xAA or packet[1] != 0x55:
        print("Invalid header")
        return None

    length = packet[2]
    payload = packet[3:-1]
    checksum = packet[-1]

    if compute_checksum(packet) != 0:
        print("Checksum mismatch!")
        return None

    print(f"Valid Packet Received: Payload Length={length}, Payload={payload.hex()}")
    return payload

def decode_payload(payload):
    # Unpack the payload based on the specified format
    header, length, timestamp, bumper, wheel_drop, cliff, left_encoder, right_encoder, left_pwm, right_pwm, button, charger, battery, overcurrent_flags = struct.unpack(
        '<B B H B B B H H b b B B B B', payload[:17]
    )

    # Create a dictionary for the decoded values
    sensor_data = {
        "header": header,
        "length": length,
        "timestamp": timestamp,
        "bumper": bumper,
        "wheel_drop": wheel_drop,
        "cliff": cliff,
        "left_encoder": left_encoder,
        "right_encoder": right_encoder,
        "left_pwm": left_pwm,
        "right_pwm": right_pwm,
        "button": button,
        "charger": charger,
        "battery": battery,
        "overcurrent_flags": overcurrent_flags
    }

    # Descriptions for each sensor
    descriptions = {
        "header": "Feedback Identifier (Fixed)",
        "length": "Size of data field (Fixed)",
        "timestamp": "Timestamp generated internally in milliseconds",
        "bumper": "Flag set when bumper is pressed: 0x01 for right, 0x02 for central, 0x04 for left",
        "wheel_drop": "Flag set when wheel is dropped: 0x01 for right, 0x02 for left",
        "cliff": "Flag set when cliff is detected: 0x01 for right, 0x02 for central, 0x04 for left",
        "left_encoder": "Accumulated encoder data for left wheel",
        "right_encoder": "Accumulated encoder data for right wheel",
        "left_pwm": "PWM value for left wheel motor (signed type for direction)",
        "right_pwm": "PWM value for right wheel motor (signed type for direction)",
        "button": "Flag set when button is pressed: 0x01 for Button 0, 0x02 for Button 1, 0x04 for Button 2",
        "charger": "Charger state: 0 for DISCHARGING, 2 for DOCKING_CHARGED, 6 for DOCKING_CHARGING, etc.",
        "battery": "Battery voltage in 0.1 V",
        "overcurrent_flags": "Flag set when overcurrent is detected: 0x01 for left wheel, 0x02 for right wheel",
    }

    # Function to clear the screen
    def clear_screen():
        if os.name == 'nt':  # For Windows
            os.system('cls')
        else:  # For Unix-like systems
            os.system('clear')

    # Function to parse and display sensor data with descriptions
    clear_screen()  # Clear the screen once before displaying data

    def parse_sensor_data(data):
        for key, value in data.items():
            if value == 0:
                continue

            if key in ["bumper", "wheel_drop", "cliff", "button", "overcurrent_flags"]:
                flags = {
                    "bumper": ["Right", "Central", "Left"],
                    "wheel_drop": ["Right", "Left"],
                    "cliff": ["Right", "Central", "Left"],
                    "button": ["Button 0", "Button 1", "Button 2"],
                    "overcurrent_flags": ["Left", "Right"]
                }
                active_flags = [desc for i, desc in enumerate(flags[key]) if value & (1 << i)]
                print(f"{key.capitalize()}: {', '.join(active_flags)} ({descriptions.get(key, 'No description available.')})")
            else:
                print(f"{key.capitalize()}: {value} ({descriptions.get(key, 'No description available.')})")

    # Check if motors are powered (PWM non-zero means powered)
    def check_motor_power(left_pwm, right_pwm):
        if left_pwm != 0 or right_pwm != 0:
            print("Motors are powered!")
        else:
            print("Motors are not powered.")

    # Call the function to parse and display sensor data
    parse_sensor_data(sensor_data)

    # Check if motors are powered
    check_motor_power(left_pwm, right_pwm)

def read_serial():
    """Read and process serial data."""
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    
    while True:
        data = ser.read(256)  # Read up to 256 bytes
        if not data:
            continue

        # Find header position
        header_pos = data.find(b'\xAA\x55')
        if header_pos == -1:
            continue

        # Extract packet
        packet = data[header_pos:]
        if len(packet) < 4:  # Ensure it has minimum necessary fields
            continue

        length = packet[2]
        expected_size = 3 + length + 1  # headers(2) + length(1) + payload + checksum(1)

        if len(packet) >= expected_size:
            payload = parse_packet(packet[:expected_size])
            if payload:
                # Here we process the motion command
                if len(payload) == 4:  # Motion command with 2 bytes for linear and 2 bytes for angular velocity
                    linear_velocity = struct.unpack('<h', payload[:2])[0] / 1000.0  # Convert back from scaled value
                    angular_velocity = struct.unpack('<h', payload[2:])[0] / 1000.0  # Convert back from scaled value

                    print(f"Motion Command Received:")
                    print(f"Linear Velocity: {linear_velocity:.2f} m/s")
                    print(f"Angular Velocity: {angular_velocity:.2f} rad/s")
                decode_payload(payload)

if __name__ == "__main__":
    read_serial()
