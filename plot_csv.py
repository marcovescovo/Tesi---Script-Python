import matplotlib.pyplot as plt
import numpy as np
import csv

# Function to sort the CSV rows by the "attrib" column
def sort_csv_by_attrib(input_file, output_file):
    with open(input_file, mode='r', newline='') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        rows = sorted(reader, key=lambda row: row['attrib'])

    with open(output_file, mode='w', newline='') as outfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

# Function to read a CSV file with a custom separator and store columns in lists
def read_csv_file(filename, delimiter=';'):
    # Initialize empty lists to store columns
    columns = {}

    try:
        # Open the CSV file for reading with the custom delimiter
        with open(filename, mode='r') as csv_file:
            # Create a CSV reader object with the specified delimiter
            csv_reader = csv.reader(csv_file, delimiter=delimiter)

            # Read the header row to get column names
            header = next(csv_reader)

            # Initialize lists for each column
            for column_name in header:
                columns[column_name] = []

            # Read the data rows and append values to respective lists
            for row in csv_reader:
                for i, value in enumerate(row):
                    columns[header[i]].append(float(value))

        return columns

    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the CSV file name
csv_filename = "/home/marco/Documents/file_di_output/sample.csv"
csv_filename_out = "/home/marco/Documents/file_di_output/sample_sorted.csv"

sort_csv_by_attrib(csv_filename, csv_filename_out)

# Call the function to read the CSV file and store columns in lists
column_data = read_csv_file(csv_filename_out)

fig, ax = plt.subplots()
x, y = column_data['GEOM_X'], column_data['GEOM_Y']
scale = column_data['attrib']

"""

scale_blue   = []
x_blue       = []
y_blue       = []
scale_green  = []
x_green      = []
y_green      = []
scale_orange = []
x_orange     = []
y_orange     = []

idx = 0

maximum = len(scale)

factor = 10 ** 3

blue_idx  = maximum // 4
green_idx = (maximum * 3) // 4

blue_threshold  = scale[blue_idx]
green_threshold = scale[green_idx]

for val in scale:

    if idx >= green_idx :
        scale_orange.append(100)#(val * factor)
        x_orange.append(x[idx])
        y_orange.append(y[idx])
    elif idx >= blue_idx :
        scale_green.append(100)#(val * factor)
        x_green.append(x[idx])
        y_green.append(y[idx])
    else:
        scale_blue.append(100)#(val * factor)
        x_blue.append(x[idx])
        y_blue.append(y[idx])
        
    idx = idx + 1

ax.scatter(x_orange, y_orange, c='tab:orange', s=scale_orange, label=f'>= {green_threshold}', alpha=0.5, edgecolors='none')
ax.scatter(x_green,  y_green,  c='tab:green',  s=scale_green,  label=f'< {green_threshold}',  alpha=0.5, edgecolors='none')
ax.scatter(x_blue,   y_blue,   c='tab:blue',   s=scale_blue,   label=f'< {blue_threshold}',   alpha=0.5, edgecolors='none')
"""
ax.scatter(x, y, c=scale, s=100, alpha=0.5, edgecolors='black')

ax.grid(True)

plt.show()
