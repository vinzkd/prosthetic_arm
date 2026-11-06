import socket
import time
import sys
import pygame

PI_IP = "192.168.50.211" 
PI_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize Pygame Controller API
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Error: No controller detected. Run inside Steam OS Desktop mode.")
    sys.exit(1)

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Connected to: {joystick.get_name()}")
print(f"Streaming analog positions to {PI_IP}:{PI_PORT}...")

try:
    while True:
        pygame.event.pump()
        
        # Read Right Trigger (Axis 5) -> Value ranges from -1.0 (unpressed) to 1.0 (fully pressed)
        trigger_raw = joystick.get_axis(5)
        # Convert -1.0..1.0 to 0°..180° angle
        index_angle = round(((trigger_raw + 1.0) / 2.0) * 180.0, 1)

        # Read Right Joystick Y-Axis (Axis 3) -> Value ranges from -1.0 (up) to 1.0 (down)
        stick_raw = joystick.get_axis(3)
        # Convert -1.0..1.0 to 0°..180° angle
        thumb_angle = round(((stick_raw + 1.0) / 2.0) * 180.0, 1)

        # Format command string: "INDEX_ANGLE,THUMB_ANGLE"
        payload = f"{index_angle},{thumb_angle}"
        
        # Transmit UDP packet
        sock.sendto(payload.encode('utf-8'), (PI_IP, PI_PORT))
        
        # Run at 50Hz (20ms interval)
        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nExiting sender script...")
