import os
import pandas as pd
import plotly.graph_objects as go

# Specify the directory containing the CSV files
output_directory = 'data_chunks'  # Directory where the chunk CSV files are saved

# Initialize a list to collect all nmac3 values
all_nmac3_values = []

# Initialize a counter for the files
file_count = 0

# Loop through each CSV file in the specified directory
for csv_file in os.listdir(output_directory):
    if csv_file.endswith('.csv'):
        csv_file_path = os.path.join(output_directory, csv_file)

        # Read the CSV file with semicolon as the delimiter
        data = pd.read_csv(csv_file_path, delimiter=';')

        # Check if required columns exist
        required_columns = {'row_num', 'nmac3', 'nmac5'}
        if not required_columns.issubset(data.columns):
            print(f"Skipping {csv_file}: missing required columns.")
            continue

        # Increment file count
        file_count += 1

        # Only process every 10th file
        if file_count % 10 != 0:
            continue

        # Append the nmac3 values to the list
        all_nmac3_values.extend(data['nmac3'].tolist())

# Check if we have any nmac3 values to plot
if all_nmac3_values:
    # Create a figure for the histogram
    fig_histogram = go.Figure()

    # Add histogram data to the histogram figure
    fig_histogram.add_trace(go.Histogram(
        x=all_nmac3_values,
        name='Combined Histogram',
        opacity=1,
        histnorm='probability density',  # Normalizing histogram
        marker=dict(line=dict(width=1, color='black')),
        showlegend=True
    ))

    # Update layout with title and axis labels for the histogram figure
    fig_histogram.update_layout(
        title='Combined Histogram of nmac3 Values',
        xaxis_title='nmac3 Values',
        yaxis_title='Probability Density',
        legend_title='Legend',
        showlegend=True,
    )

    # Show grid for histogram
    fig_histogram.update_xaxes(showgrid=True)
    fig_histogram.update_yaxes(showgrid=True)

    # Adjust layout for histogram
    fig_histogram.update_layout(margin=dict(l=40, r=40, t=40, b=40))

    # Show the combined histogram plot
    fig_histogram.show()
else:
    print("No nmac3 values found in the selected files.")
