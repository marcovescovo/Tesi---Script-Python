import csv

# Specify the CSV file path
csv_file_path = '/home/marco/Documents/user_inputs.csv'

# Check if the CSV file already exists
csv_file_exists = False
try:
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        if any(row for row in csvreader):
            csv_file_exists = True
except FileNotFoundError:
    pass

# List of parameter names
parameters = [
    "cardinality", "distribution", "percentage", "buffer", "probability",
    "digits", "split_range", "dither", "seed", "geometry", "width",
    "height", "size", "line_seg", "format", "affinematrix", "dimensions",
    "sampleQuantity"
]

if not csv_file_exists:
    # Create the CSV file and write the parameter names as the first row
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(parameters)

while True:
    # Create a list to store parameter values for the current row
    parameter_values = []

    # Ask the user for input for each parameter and store them in the list
    for parameter in parameters:
        user_input = input(f"Enter value for {parameter}: ")
        parameter_values.append(user_input)

    # Write the parameter values to the CSV file
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(parameter_values)

    print(f'User inputs have been added to {csv_file_path}.')

    # Ask the user if they want to add more rows
    add_more = input('Do you want to add more rows? (y/n): ').strip().lower()
    if add_more != 'y':
        break

print('Exiting the program.')
