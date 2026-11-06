import socket
import serial
import time

# Update with your Arduino's serial port (e.g., '/dev/ttyACM0' or '/dev/ttyUSB0')
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

# UDP Socket configuration (receives data from Steam Deck)
UDP_IP = "0.0.0.0"
UDP_PORT = 5005

# Initialize Serial link to Arduino
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait 2 seconds for Arduino to reset upon connection
    print(f"Connected to Arduino on {SERIAL_PORT}")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Setup UDP Server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Pi Bridge listening for Deck commands on UDP port {UDP_PORT}...")

try:
    while True:
        # Receive packet from Steam Deck (e.g., "180,90")
        data, addr = sock.recvfrom(1024)
        message = data.decode('utf-8').strip() + "\n"
        
        # Forward command string directly over Serial to Arduino
        arduino.write(message.encode('utf-8'))

except KeyboardInterrupt:
    print("\nShutting down bridge...")
    arduino.close()
