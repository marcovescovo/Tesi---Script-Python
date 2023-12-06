from pyspark.sql import SparkSession
import sys
import numpy as np
import scipy.stats as stats
from pyspark.sql.types import StructType, StructField, DoubleType  # Add this import
import re
import os
import random
import math
import datetime
import csv

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def estrai_nomi_file(directory_path):
    # Verifica se il percorso specificato è una directory
    if not os.path.isdir(directory_path):
        return None
    
    # Ottieni la lista dei nomi dei file nella directory
    file_names = os.listdir(directory_path)
    
    # Estrai i nomi dei file con estensione in una lista
    file_names_with_extension = [file for file in file_names if os.path.isfile(os.path.join(directory_path, file))]
    
    return file_names_with_extension

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def getEstensione(filePath):
    estensione = os.path.splitext(filePath)[-1]
    return estensione

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def estrai_coordinate_da_stringa(polygon_string):    # Cerca tutte le coppie di coordinate all'interno della stringa POLYGON
    coordinate_matches = re.findall(r'([-+]?\d*\.\d+\s[-+]?\d*\.\d+)', polygon_string)
    coord_list = []
    for element in coordinate_matches:
        coord_list.append(element.split(" "))
    # Divide le coordinate in coppie    coordinate_coppie = [coordinate.split() for coordinate in coordinate_matches]
    # Converti le coordinate in tuple di float
    coordinate_res = [[float(x), float(y)] for x, y in coord_list]
    return coordinate_res

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def calcola_centroide(vertici):
    num_vertici = len(vertici)
    if num_vertici < 3:
        raise ValueError("Il poligono deve avere almeno 3 vertici: " + str(len(vertici)))
    somma_x = 0
    somma_y = 0

    for x, y in vertici:
        somma_x += x
        somma_y += y

    centroide_x = somma_x / num_vertici
    centroide_y = somma_y / num_vertici

    return (centroide_x, centroide_y)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def gaussiana(x, mu=0.5, sigma=0.15):
    # Calcola il valore della gaussiana
    exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
    result = math.exp(exponent)

    # Normalizza il risultato tra 0 e 1
    max_value = math.exp(0)  # Quando x = mu
    normalized_result = result / max_value

    return normalized_result

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def doppiaGaussiana(P, POS1, POS2, NEG1, NEG2, mu=0.45):

    GSS = gaussiana(P, mu)
    # Calcola il valore della gaussiana principale nel punto P
    gaussiana_principal = GSS * (POS2-POS1) + POS1

    # Calibra la gaussiana secondaria in modo che sia inferiore ad A ma maggiore di 0
    GSS = gaussiana(P, 1-mu)
    gaussiana_secondaria = GSS * (NEG2-NEG1) + NEG1

    # Sottrai il valore della gaussiana secondaria
    risultato = gaussiana_principal - gaussiana_secondaria

    #while risultato < 0.001:
    #    risultato = risultato * 10

    return risultato

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def add_column(row):
    list_row = list(row)
    new_value = (doppiaGaussiana(list_row[0], AX1, AX2, BX1, BX2) + doppiaGaussiana(list_row[1], AY1, AY2, BY1, BY2)) / 2
    new_row = list_row + [float(new_value)]
    return tuple(new_row)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def add_column_wkt(row):
    list_row = list(row)
    centroide_x, centroide_y = calcola_centroide(estrai_coordinate_da_stringa(list_row[0]))
    new_value = (doppiaGaussiana(centroide_x, AX1, AX2, BX1, BX2) + doppiaGaussiana(centroide_y, AY1, AY2, BY1, BY2)) / 2
    new_row = list_row + [float(new_value)]
    #new_row = list_row + [0]
    return tuple(new_row)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

newColName = "attrib"
newColValue = 0
csv_dir_path = "/home/marco/Documents/file_di_input/"
output_log_csv = "/home/marco/Documents/output_log.csv"

list_csv = estrai_nomi_file(csv_dir_path)
   
# Spark session
spark = SparkSession.builder.appName("CSVtoRDD").getOrCreate()

for file in list_csv:

    print()
    
    csv_file_path = csv_dir_path + file

    estensione = getEstensione(csv_file_path)
    
    # Nome prima colonna
    if estensione == ".wkt":
        header = 'GEOM'
    elif estensione == ".csv":
        header = 'GEOM_X,GEOM_Y'
    else:
        continue

    AX1 = round(random.uniform(0.2, 1),   3) # minimo positivo
    AX2 = round(random.uniform(AX1, 1),  3) # massimo positivo
    BX1 = round(random.uniform(0, AX1),  3) # minimo negativo
    BX2 = round(random.uniform(BX1, AX1), 3) # massimo negativo


    AY1 = round(random.uniform(0.2, 1),   3) # minimo positivo
    AY2 = round(random.uniform(AY1, 1),  3) # massimo positivo
    BY1 = round(random.uniform(0, 0.2),  3) # minimo negativo
    BY2 = round(random.uniform(BY1, AY1), 3) # massimo negativo

    print(f"Elaborazione per il file {csv_file_path} in corso")

    try:
        # Apri il file in modalità lettura
        with open(csv_file_path, 'r') as file:
            # Leggi il contenuto esistente
            file_contents = file.read()

        # Controlla se "GEOM" è già presente sulla prima riga
        if not file_contents.startswith(header):
            # Apri il file in modalità scrittura sovrascrivendo il contenuto esistente
            with open(csv_file_path, 'w') as file:
                # Scrivi il nuovo header all'inizio
                file.write(header + '\n')
                # Scrivi il contenuto originale dopo il nuovo header
                file.write(file_contents)

    except FileNotFoundError:
        print(f'File non trovato: {file_path}')
    except Exception as e:
        print(f'Si è verificato un errore: {str(e)}')

    # CSV file to DataFrame
    spark_csv_file_path = "file://" + csv_file_path
    if estensione == ".wkt":
        df = spark.read.option("delimiter", ";").csv(spark_csv_file_path, header=True, inferSchema=True)
    else:
        df = spark.read.option("delimiter", ",").csv(spark_csv_file_path, header=True, inferSchema=True)

    # DataFrame to RDD
    rdd = df.rdd

    # Define the schema for the "attrib" column as DoubleType()
    schema = StructType(df.schema.fields + [StructField(newColName, DoubleType(), True)])

    if estensione == '.wkt':
        new_rdd = rdd.map(add_column_wkt)
    else:
        new_rdd = rdd.map(add_column)

    # RDD to DataFrame
    new_df = spark.createDataFrame(new_rdd, schema)

    # Ottieni la data e l'ora attuali
    data_ora_attuali = datetime.datetime.now()

    # Formatta la data e l'ora come una stringa
    data_ora_formattata = data_ora_attuali.strftime("%Y-%m-%d_%H:%M:%S.%f")

    output_file_name = f"{csv_dir_path}output_{data_ora_formattata}.csv"

    # Define the path for the new CSV file
    output_spark_csv_file_path = f"file:///{output_file_name}"

    # Save the new DataFrame as CSV
    new_df.write.option("delimiter", ";").mode('overwrite').csv(output_spark_csv_file_path, header=True)

    try:
        # Apri il file CSV in modalità append
        with open(output_log_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Scrivi le 5 stringhe su 5 colonne diverse
            writer.writerow([csv_file_path, output_file_name, AX1, AX2, BX1, BX2])
            
    except Exception as e:
        print(f"Si è verificato un errore: {str(e)}")

# Stop the Spark session
spark.stop()


