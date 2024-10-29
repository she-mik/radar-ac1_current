import serial
import json
import logging
import csv
import os

# CSV file setup
csv_file_path = 'data.csv'

# Check if the file exists and prepare to write data
file_exists = os.path.isfile(csv_file_path)

# Open the CSV file in append mode
with open(csv_file_path, mode='w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write header
    csv_writer.writerow(['idx', 'ac_current_1', 'ac_current_2', 'ac_current_3', 'ac_current_4', 'ac_current_5', 'ac_current_6'])  # Add headers based on your JSON structure

    # Open the serial port
    with serial.Serial('COM3', 115200, timeout=1) as ser:
        count = -1
        while count != 1:
            line = ser.readline()  # Read a line from the serial port
            try:
                if line:  # Check if the line is not empty
                    decoded_line = line.decode(
                        'utf-8').strip()  # Decode the byte string and strip any whitespace/newlines

                    # Find and extract the JSON part of the line
                    start_index = decoded_line.find('{')  # Locate the beginning of the JSON object
                    end_index = decoded_line.rfind('}')  # Locate the end of the JSON object

                    # Check if valid JSON exists in the line
                    if start_index != -1 and end_index != -1 and start_index < end_index:
                        json_data = decoded_line[start_index:end_index + 1]  # Extract the JSON part
                        parsed_json = json.loads(json_data)  # Parse the JSON string into a Python dictionary

                        if "ac_current" in parsed_json:
                            idx_value = parsed_json["ac_current"]["idx"]  # Extract the idx value
                            ac_1_value = parsed_json["ac_current"]["ac1"] # Extract ac_current value
                            ac_2_value = parsed_json["ac_current"]["ac2"]
                            ac_3_value = parsed_json["ac_current"]["ac3"]
                            ac_4_value = parsed_json["ac_current"]["ac4"]  # Extract ac_current value
                            ac_5_value = parsed_json["ac_current"]["ac5"]
                            ac_6_value = parsed_json["ac_current"]["ac6"]

                            offset_1 = 2048 #Correction offset AC_1
                            offset_2 = 2048 #Correction offset AC_2
                            offset_3 = 2048 #Correction offset AC_3

                            if idx_value == 0:
                                count += 1

                            # Print the parsed JSON data for debugging
                            print(json.dumps(parsed_json, indent=4))

                            # Write the extracted data to CSV
                            csv_writer.writerow([idx_value, ac_1_value-offset_1, ac_2_value-offset_2, ac_3_value-offset_3, ac_4_value-offset_1, ac_5_value-offset_2, ac_6_value-offset_3])  # Write a new row to the CSV
                            logging.info(f"Data written to CSV: idx={idx_value}, ac_1={ac_1_value}, ac_2={ac_2_value}, ac_3={ac_3_value}, ac_4={ac_1_value}, ac_5={ac_2_value}, ac_6={ac_3_value}")

            except json.JSONDecodeError as e:
                logging.error(f"Failed to decode JSON: {e}")
            except Exception as e:
                logging.error(f"An error occurred: {e}")