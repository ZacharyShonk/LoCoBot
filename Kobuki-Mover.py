import serial
import time
import struct
import Kobuki_Read_Serial

class KobukiController:
    def __init__(self, port="/dev/ttyUSB1", baudrate=115200):
        """Initialize the connection to the Kobuki robot."""
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Allow time for the connection to establish
            print("Connected to Kobuki robot.")
        except serial.SerialException as e:
            print(f"Error connecting to Kobuki: {e}")
            exit(1)

    def send_command(self, speed, turn):
        """Send movement commands to Kobuki robot with speed and turn rate."""
        # Command Header
        header = [0xAA, 0x55]  # Start of command sequence
        payload_length = 0x06   # Number of data bytes in the payload
        command_id = 0x01       # Command for controlling movement (speed & turn)

        # Pack speed and turn rate as 2-byte signed integers (little-endian)
        speed_bytes = struct.pack('<h', speed)
        turn_bytes = struct.pack('<h', turn)

        # Payload consists of the command length, ID, speed, and turn
        payload = [payload_length, command_id] + list(speed_bytes) + list(turn_bytes)

        # Compute checksum by XOR'ing all payload bytes
        checksum = 0
        for byte in payload:
            checksum ^= byte

        # Final command including header, payload, and checksum
        command = bytearray(header + payload + [checksum])

        # Output command in hex for debugging
        print(f"Sending movement command: {command.hex()}")

        # Send command to Kobuki robot
        self.ser.writelines(command)  # Write the entire command in one go
        self.ser.flush()  # Make sure all data is transmitted



    def enable_motors(self):
        command = b'\xAA\x55\x02\x03\xFA'  # Motor power enable command
        self.ser.write(command)
        time.sleep(0.1)  # Short delay
        print("Sent motor enable command.")


    def request_motor_status(self):
        """Request the status of the motors (whether they are enabled)."""
        header = [0xAA, 0x55]
        payload_length = 0x03
        command_id = 0x10  # Command ID to request motor status

        # Build the payload for the motor status request
        payload = [payload_length, command_id]

        # Compute checksum
        checksum = 0
        for byte in payload:
            checksum ^= byte

        # Final command to request motor status
        command = bytearray(header + payload + [checksum])

        # Output command in hex for debugging
        print(f"Requesting motor status: {command.hex()}")

        # Send request to Kobuki
        self.ser.write(command)

    def move_forward(self, speed=200, duration=1):
        """Move the Kobuki forward at a given speed (mm/s) for a set duration (seconds)."""
        self.send_command(speed, 0)  # No turning, only moving forward
        time.sleep(duration)
        self.stop()

    def move_backward(self, speed=200, duration=1):
        """Move the Kobuki backward at a given speed for a set duration."""
        self.send_command(-speed, 0)  # Negative speed for backward movement
        time.sleep(duration)
        self.stop()

    def turn_left(self, speed=50, duration=1):
        """Turn the Kobuki left at a given speed (degrees/second) for a set duration."""
        self.send_command(0, speed)  # Turning to the left
        time.sleep(duration)
        self.stop()


    def reset_kobuki(self):
        command = b'\xAA\x55\x02\x0B\xF2'  # Reset command
        self.ser.write(command)
        time.sleep(1)
        print("Sent reset command.")

    def simulate_button_press(self):
        command = b'\xAA\x55\x02\x01\xFE'  # Fake button press command
        self.ser.write(command)
        time.sleep(0.1)
        print("Simulated B0 button press.")

    def unlock_kobuki(self):
        reset_command = b'\xAA\x55\x02\x0B\xF2'  # Reset command
        motor_enable_command = b'\xAA\x55\x02\x03\xFA'  # Enable motors
        
        self.ser.write(reset_command)
        time.sleep(0.5)  # Short delay
        self.ser.write(motor_enable_command)
        time.sleep(0.1)  # Ensure the command is processed

        print("Attempted to unlock Kobuki. Check if motors are now enabled.")


    def turn_right(self, speed=50, duration=1):
        """Turn the Kobuki right at a given speed for a set duration."""
        self.send_command(0, -speed)  # Negative turn speed for right turn
        time.sleep(duration)
        self.stop()

    def send_hardcoded_move(self):
        """Send a pre-configured movement command to move forward."""
        command = bytearray([0xAA, 0x55, 0x06, 0x01, 0xC8, 0x00, 0x00, 0x00, 0xCF])
        print(f"Sending hardcoded move command: {command.hex()}")
        self.ser.write(command)

    def stop(self):
        """Stop the Kobuki robot."""
        self.send_command(0, 0)  # Speed and turn rate set to 0

if __name__ == "__main__":
    # Create KobukiController instance with the default serial port
    kobuki = KobukiController(port="/dev/ttyUSB0")  # Change port if needed

    kobuki.send_hardcoded_move()

    Kobuki_Read_Serial.read_serial()

    # try:
    #     # Enter user commands to control the robot
    #     while True:
    #         command = input("Enter command (w/a/s/d for movement, q to quit): ").strip().lower()
    #         if command == 'w':
    #             kobuki.move_forward(200, 1)
    #         elif command == 's':
    #             kobuki.move_backward(200, 1)
    #         elif command == 'a':
    #             kobuki.turn_left(100, 1)
    #         elif command == 'd':
    #             kobuki.turn_right(100, 1)
    #         elif command == 'q':
    #             kobuki.stop()
    #             break
    #         else:
    #             print("Invalid command. Use w/a/s/d or q to quit.")
    # except KeyboardInterrupt:
    #     kobuki.stop()
    #     print("\nStopped.")
