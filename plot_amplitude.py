import os
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Specify the directory containing the CSV files
output_directory = 'data_chunks'  # Directory where the chunk CSV files are saved

# Initialize lists to store chunk numbers and amplitudes (max - median)
chunk_numbers = []
amplitudes = []

# Initialize a counter for the files
file_count = 0

# Loop through each CSV file in the specified directory
for csv_file in os.listdir(output_directory):
    if csv_file.endswith('.csv'):
        csv_file_path = os.path.join(output_directory, csv_file)

        # Read the CSV file with semicolon as the delimiter
        data = pd.read_csv(csv_file_path, delimiter=';')

        # Check if required columns exist
        required_columns = {'row_num', 'nmac3'}
        if not required_columns.issubset(data.columns):
            print(f"Skipping {csv_file}: missing required columns.")
            continue

        # Increment file count (this will act as the chunk number)
        file_count += 1

        # Process only every 10th file
        if file_count % 10 != 0:
            continue

        # Select rows for processing (optional, you can use full data)
        base_point = 0  # Starting point, location of idx 0
        limited_data = data.iloc[base_point:base_point + 1024]  # Get rows

        # Extract the relevant column for AC current
        y_data_nm_ac3 = limited_data['nmac6']  # Dependent variable for AC current 3

        # Calculate the maximum and median values for this chunk
        max_value = np.max(y_data_nm_ac3)
        median_value = np.median(y_data_nm_ac3)

        # Calculate the amplitude (max - median)
        amplitude = max_value - median_value

        # Append the chunk number and its amplitude to the lists
        chunk_numbers.append(file_count)
        amplitudes.append(amplitude)

# Create a scatter plot for chunk numbers vs. amplitudes
fig = go.Figure()

# Add trace for the amplitudes
fig.add_trace(go.Scatter(x=chunk_numbers, y=amplitudes, mode='lines+markers',
                         name='Amplitude per Chunk (Max - Median)', line=dict(color='purple', width=4),
                         marker=dict(size=6, color='red')))

# Update layout with larger title and axis labels
fig.update_layout(
    title={'text': 'Amplitude (Max - Median) of nmac6 in Every 10th Chunk', 'font': {'size': 24}},  # Larger title
    xaxis_title={'text': 'Chunk Number', 'font': {'size': 18}},  # Larger x-axis label
    yaxis_title={'text': 'Amplitude (Max - Median)', 'font': {'size': 18}},  # Larger y-axis label
    legend_title={'text': 'Legend', 'font': {'size': 16}},  # Larger legend title
    font=dict(size=26),  # General font size for labels, tick labels, etc.
    showlegend=True,
)

# Increase marker size and line width for better visibility
fig.update_traces(marker=dict(size=8, color='red'), line=dict(width=5))

# Show the plot
fig.show()