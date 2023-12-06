import numpy as np
import scipy.stats as stats

def estrai_coordinate_da_stringa(polygon_string):    # Cerca tutte le coppie di coordinate all'interno della stringa POLYGON
    coordinate_matches = re.findall(r'([-+]?\d*\.\d+\s[-+]?\d*\.\d+)', polygon_string)
    # Divide le coordinate in coppie    coordinate_coppie = [coordinate.split() for coordinate in coordinate_matches]
    # Converti le coordinate in tuple di float
    coordinate_tuple = [(float(x), float(y)) for x, y in coordinate_coppie]
    return coordinate_tuple

def calcola_centroide(vertici):
    num_vertici = len(vertici)
    if num_vertici < 3:
        raise ValueError("Il poligono deve avere almeno 3 vertici")

    somma_x = 0
    somma_y = 0

    for x, y in vertici:
        somma_x += x
        somma_y += y

    centroide_x = somma_x / num_vertici
    centroide_y = somma_y / num_vertici

    return (centroide_x, centroide_y)

def gaussian_value_at_point(center_param, point):
    # Ensure the center_param is within the range [0, 1]
    center_param = max(0, min(1, center_param))
    
    # Calculate the standard deviation to constrain values between 0 and 1
    std_deviation = min(center_param, 1 - center_param)
    
    # Create a normal distribution with the specified mean and standard deviation
    norm_dist = stats.norm(loc=center_param, scale=std_deviation)
    
    # Calculate the PDF (probability density function) value at the specified point
    pdf_value = norm_dist.pdf(point)
    
    return pdf_value

# Example usage with a center parameter of 0.5 and a specific point
center_param_x = 0.5
center_param_y = 0.5
specific_point_x = 0.50
specific_point_y = 0.50
pdf_value = (gaussian_value_at_point(center_param_x, specific_point_x) + gaussian_value_at_point(center_param_y, specific_point_y)) / 2

print(f"Z value at xy coordinates {specific_point_x} {specific_point_y}:", pdf_value)
