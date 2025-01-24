import serial
import time
import numpy as np
from datetime import datetime

# Load the interpolation data (volume-to-grams calibration data) from the .npy file
interpolation_data = np.load('interpolation_data.npy', allow_pickle=True)
interpolator = interpolation_data.item()  # Assuming it's stored as a dictionary

# Extract the slope and intercept from the saved model
slope = interpolator['slope']
intercept = interpolator['intercept']

serial_port = 'COM4' # OR -- use this for raspberry pi comm '/dev/ttyACM0' 
baud_rate = 57600
file_path = 'arduino_log.txt'  # Update path as needed

# Variable to store the tare value (initial sensor value)
tare_value = None

def interpolate_to_volume(sensor_value):
    """ Interpolate individual sensor value to volume (mL) using linear model. """
    try:
        volume_mL = (sensor_value - intercept) / slope
        return volume_mL
    except Exception as e:
        print(f"Error during interpolation: {e}")
        return None

def convert_to_grams(volume_mL):
    """ Convert volume in mL to grams (assuming 1mL = 1g). """
    if volume_mL is not None:
        return volume_mL  # Assuming 1 mL = 1 gram for water, adjust for different densities.
    else:
        return None

def Tare_scale():
    """ Calibrate the scale by setting tare and performing interpolation. """
    global tare_value
    print("Starting taring...")
    ser = serial.Serial(serial_port, baud_rate, timeout=10)
    
    line = ser.readline().decode('utf-8').strip()
    time.sleep(5)  # Optional: Add a small delay to ensure the data is ready
    if line:
        try:
            # Parse the line to extract sensor values for each loadcell
            if "Loadcell" in line:
                sensor_values = []
                # Split the line by '|' and extract values
                for part in line.split('|'):
                    parts = part.strip().split(":")
                    if len(parts) == 2:
                        sensor_value = float(parts[1].strip())  # Convert the reading to float
                        sensor_values.append(sensor_value)
                # If the tare value is set, subtract it from the current sensor value
                # Perform interpolation for each loadcell
                if sensor_values:
                    tare_values = [interpolate_to_volume(value) for value in sensor_values]
                    print(f"Tare values set: {tare_values}")
                    
            else:
                print(f"Line format is incorrect: {line}")
                
        except Exception as e:
            print(f"Error parsing sensor value: {e}")

    else:
        print("No data available")  # Debugging info: No data available
    
    # Interpolation will happen based on this tare value
    print("Scale calibrated! You can now proceed with continuous data collection.\n")


def data_collection():
    """ Collect data continuously and log it to a file. """
    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=10)

        with open(file_path, 'w') as file:
            num_sensors = 5

            header = "Timestamp(s)"
            for i in range(1, num_sensors + 1):
                header += f"\tLoadcell {i} Value (raw)\tLoadcell {i} Volume (mL)\tLoadcell {i} Grams(g)"
            header += "\n"
            file.write(header)
            file.flush()  # Ensure data is written to the file immediately
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        # Print the raw line for debugging
                        print(f"Raw line: {line}")
                        
                        # Extract the sensor values from the line
                        try:
                            if "Loadcell" in line:
                                sensor_values = []
                                # Split the line by '|' and extract values
                                for part in line.split('|'):
                                    parts = part.strip().split(":")
                                    if len(parts) == 2:
                                        sensor_value = float(parts[1].strip())  # Convert the reading to float
                                        sensor_values.append(sensor_value)
                                
                                # If tare value is set, subtract it from the current sensor value
                                if tare_value is not None and sensor_values:

                                    volume_mL = [interpolate_to_volume(value) for value in sensor_values]  # Get all loadcell
                                    grams = [a-b for a,b in zip(volume_mL , tare_value)]  # Calculate grams as difference
                                    
                                    # Print the converted values for debugging, formatted to 1 decimal place
                                    print(f"Interpolated grams: {grams:.1f} grams")                                   
                                    
                                    # Write the data to the file, formatted to 1 decimal place
                                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    file.write(
                                        f"{timestamp}\t"
                                        + "\t".join([f"{value:.1f}" for value in sensor_values])
                                        + "\t"
                                        + "\t".join([f"{v:.1f}" for v in volume_mL])
                                        + "\t"
                                        + "\t".join([f"{g:.1f}" for g in grams])
                                        + "\n"
                                    )
                                    file.flush()  # Ensure data is written to the file immediately
                            else:
                                print(f"Line format is incorrect: {line}")
                        except Exception as e:
                            print(f"Error with generating sensor value: {e}")
                    
                else:
                    print("No data available")  # Debugging info: No data available
                
                time.sleep(5)  # Optional: Add a small sleep to reduce CPU usage

    except serial.SerialException as e:
        print(f"Serial Error: {e}")
    except IOError as e:
        print(f"File I/O Error: {e}")

def main():
    while True:
        """ Main function to offer user options. """
        print("\nWelcome to the scale calibration and data collection program.")
        print("1. Tare the scale")
        print("2. Start continuous data collection")

        option = input("Enter the number of your choice: ").strip()
        
        if option == "1":
            Tare_scale()
        elif option == "2":
            data_collection()
        else:
            print("Invalid option. Please choose 1 or 2")

if __name__ == '__main__':
    main()
