import csv

# Specify the CSV file path
csv_file_path = '/home/vboxuser/Documents/user_inputs.csv'

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
    "compress", "polysize", "maxseg", "sampleQuantity"
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
        if len(user_input) <= 0:
            match parameter:
                case 'cardinality':
                    user_input = '10000'
                case 'distribution':
                    user_input = 'uniform'
                case 'percentage':
                    user_input = ''
                case 'buffer':
                    user_input = ''
                case 'probability':
                    user_input = ''
                case 'digits':
                    user_input = ''
                case 'split_range':
                    user_input = ''
                case 'seed':
                    user_input = '1'
                case 'geometry':
                    user_input = 'point'
                case 'width':
                    user_input = ''
                case 'height':
                    user_input = ''
                case 'size':
                    user_input = ''
                case 'line_seg':
                    user_input = ''
                case 'format':
                    user_input = 'csv'
                case 'affinematrix':
                    user_input = '1,0,0,0,1,0'
                case 'dimensions':
                    user_input = '2'
                case 'maxseg':
                    user_input = '3'
                case 'polysize':
                    user_input = '0.01'
                case 'compress':
                    user_input = 'bz2'
                case 'sampleQuantity':
                    user_input = '1'
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
