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

        # Select rows for processing (optional, you can use full data)
        base_point = 0  # Starting point, location of idx 0
        limited_data = data.iloc[base_point:base_point + 1024]  # Get rows

        # Extract the relevant column for AC current
        y_data_nm_ac3 = limited_data['nmac3']  # Dependent variable for AC current 3

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
                         name='Amplitude per Chunk (Max - Median)', line=dict(color='blue', width=2),
                         marker=dict(size=6, color='red')))

# Update layout with title and axis labels
fig.update_layout(
    title='Amplitude (Max - Median) of nmac3 in Each Chunk',
    xaxis_title='Chunk Number',
    yaxis_title='Amplitude (Max - Median)',
    legend_title='Legend',
    showlegend=True,
)

# Show grid (optional in plotly; you can customize gridlines)
fig.update_xaxes(showgrid=True)
fig.update_yaxes(showgrid=True)

# Adjust layout (optional, but helps in some cases)
fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))

# Show the plot
fig.show()

