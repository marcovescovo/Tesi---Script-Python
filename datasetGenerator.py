import csv
import requests
from urllib.parse import urlencode, urljoin
import os
from datetime import datetime

# Fixed URL
base_url = "https://spider.cs.ucr.edu/cgi/generator.py?"

# Function to make an HTTP GET request with given parameters and save the response as a file
def make_get_request_and_save(url, params, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
        
        # Save the response content (file) to the current directory
        with open(output_file, 'wb') as file:
            file.write(response.content)
        
        return f"File saved as: {output_file}"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


# Main function to read CSV and make GET requests
def main(csv_file):
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        
        # Read the parameter names from the first row
        parameter_names = next(csv_reader)
        
        for row in csv_reader:
            print(row)

            # Create a dictionary of parameters using the parameter names
            params = {parameter_names[i]: row[i] for i in range(len(parameter_names))}
            
            # Extract and remove the 'sampleQuantity' parameter
            sample_quantity = params.pop('sampleQuantity', None)

            if len(sample_quantity) <= 0:
                continue
            
            # Filter out parameters with a length of 0 or less
            params = {k: v for k, v in params.items() if v and len(v) > 0}
            
            # Make multiple requests based on sampleQuantity
            for i in range(int(sample_quantity)):
        
                # Determine the file format based on the 'format' parameter (default to 'csv')
                file_format = params.get('format', 'csv')
                if len(file_format) <= 0:
                    file_format = 'csv'  # Default to 'csv' if 'format' is not valid
                    
                current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
                output_file = f"output_file{current_datetime}.{file_format}"
                
                full_url = urljoin(base_url, "?" + urlencode(params))
                response = make_get_request_and_save(full_url, params, output_file)
                print(f"Request URL: {full_url}\nParameters: {params}\n{response}\n")

                # Increment the 'seed' parameter value by 1 at each iteration
                seed_value = int(params.get('seed', 0)) + 1
                params['seed'] = str(seed_value)

if __name__ == "__main__":
    csv_file = "/home/vboxuser/Documents/user_inputs.csv"  # Replace with your CSV file name
    main(csv_file)
