def Tare_scale():
    """ Calibrate the scale by setting tare and performing interpolation. """
    global tare_value
    print("Starting taring...")
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    
    line = ser.readline().decode('utf-8').strip()
    
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
                # Perform interpolation to get volume (mL)
                if sensor_values:
                    volume_mL = interpolate_to_volume(sensor_values[0])  # Assuming Loadcell 1 is used for tare
                    tare_value = volume_mL
                    print(f"Tare value set: {tare_value}")
                    
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
        ser = serial.Serial(serial_port, baud_rate, timeout=1)

        with open(file_path, 'w') as file:
            file.write("Timestamp(s)\tSensor 1 Value (raw)\tSensor 2 Value (raw)\tSensor 3 Value (raw)\tSensor 4 Value (raw)\tSensor 5 Value (raw)\tVolume (mL)\tGrams\n")

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
                                    volume_mL = interpolate_to_volume(sensor_values[0])  # Assuming Loadcell 1 is used for volume
                                    grams = volume_mL - tare_value  # Calculate grams as difference
                                    
                                    # Print the converted values for debugging, formatted to 1 decimal place
                                    print(f"Interpolated grams: {grams:.1f} grams")                                   
                                    
                                    # Write the data to the file, formatted to 1 decimal place
                                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    file.write(f"{timestamp}\t" + "\t".join([f"{value:.1f}" for value in sensor_values]) + f"\t{volume_mL:.1f}\t{grams:.1f}\n")
                                    file.flush()  # Ensure data is written to the file immediately
                            else:
                                print(f"Line format is incorrect: {line}")
                        except Exception as e:
                            print(f"Error with generating sensor value: {e}")
                    
                else:
                    print("No data available")  # Debugging info: No data available
                
                time.sleep(2)  # Optional: Add a small sleep to reduce CPU usage

    except serial.SerialException as e:
        print(f"Serial Error: {e}")
    except IOError as e:
        print(f"File I/O Error: {e}")