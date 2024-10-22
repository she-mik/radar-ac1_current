import json
import csv
import os

# Specify the input and output file paths
no_move_file_path = 'ac_current2.txt'  # Path to your no move text file
output_directory = 'data_chunks'  # Directory to save the output CSV files

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)


# Function to read and process the JSON file by row count
def read_json_file_by_row(file_path):
    data_list = []  # List to store the data in order
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):  # Use line number for sequential indexing
            line = line.strip()
            offset = 0
            if line:
                try:
                    json_data = json.loads(line)
                    data_list.append({
                        "row_num": json_data.get("idx", 0),  # Store row number as key
                        "nmac1": json_data.get("ac1", 0) - offset,
                        "nmac2": json_data.get("ac2", 0) - offset,
                        "nmac3": json_data.get("ac3", 0) - offset,
                        "nmac4": json_data.get("ac4", 0) - offset,
                        "nmac5": json_data.get("ac5", 0) - offset,
                        "nmac6": json_data.get("ac6", 0) - offset,
                    })
                except json.JSONDecodeError:
                    print(f"Error decoding JSON on line {line_num}: {line}")
    return data_list


# Read data from the input file
no_move_data = read_json_file_by_row(no_move_file_path)

# Check if there's data to write
if no_move_data:
    # Chunk size
    chunk_size = 1024

    # Calculate the number of chunks
    num_chunks = (len(no_move_data) + chunk_size - 1) // chunk_size  # This ensures we round up

    # Write each chunk to a separate CSV file
    for chunk_index in range(num_chunks):
        # Calculate start and end indices for the chunk
        start_index = chunk_index * chunk_size
        end_index = min(start_index + chunk_size, len(no_move_data))

        # Get the current chunk of data
        chunk_data = no_move_data[start_index:end_index]

        # Define output file name
        output_file_path = os.path.join(output_directory, f'data_chunk_{chunk_index + 1}.csv')

        # Define the CSV headers based on the chunk data
        headers = chunk_data[0].keys()

        # Write the chunk data to the CSV file
        with open(output_file_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=';')  # Use semicolon as delimiter
            writer.writeheader()
            writer.writerows(chunk_data)

        print(f"Chunk {chunk_index + 1} has been written to {output_file_path}.")
else:
    print("No data available to write.")