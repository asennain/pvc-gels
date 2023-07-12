import serial
import time

ser = serial.Serial('COM4', 250000)  # Replace 'COM3' with your printer's serial port
print(f"COM Port: {ser.name}")
time.sleep(2)  # Allow time for the connection to stabilize

ser.write("G91\n".encode())

for _ in range(2):
    ser.write("G1 Z.1\n".encode())
    time.sleep(2)

time.sleep(1)  # Wait for 1 second

ser.close()
