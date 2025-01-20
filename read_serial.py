import serial
import time
from datetime import datetime

serial_port = '/dev/ttyACM0'  # Update this to your actual port
baud_rate = 38400
file_path = 'arduino_log.txt'  # Update path as needed

def main():
    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        #time.sleep(1)  # Allow time for Arduino to reset

        with open(file_path, 'w') as file:
            file.write("Timestamp(s)\tCount\tAnalog Value\tVoltage(V)\t Pressure(psid)\n")
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"{timestamp} - {line}")  # Print with timestamp
                        file.write(f"{timestamp}\t{line}\n")  # Write with timestamp
                        file.flush()  # Ensure data is written to the file immediately
                else:
                    print("No data available")  # Debugging info: No data available
                
                # Optional: Add a small sleep to reduce CPU usage
                time.sleep(1)

    except serial.SerialException as e:
        print(f"Serial Error: {e}")
    except IOError as e:
        print(f"File I/O Error: {e}")

if __name__ == '__main__':
    main()
