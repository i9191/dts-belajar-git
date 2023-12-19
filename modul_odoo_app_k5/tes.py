import numpy as np
import pandas as pd

data = [
    {
        'nim': '21312412', 
        'nama': 'agus', 
        'prestasi': 1, 
        'nilai': {
            'Keamanan Informasi': {'n': 4.0, 'sks': 2, 'jam': 4}, 
            'E-Business': {'n': 2.9, 'sks': 2, 'jam': 4},
            'Pemrograman Platform Bergerak (Mobile)': {'n': 2.5, 'sks': 3, 'jam': 6},
            'Sistem Pendukung Keputusan': {'n': 4.0, 'sks': 3, 'jam': 6},
            'Pengolahan Citra Digital': {'n': 4.0, 'sks': 3, 'jam': 6},
            'Proyek Tingkat III': {'n': 3.5, 'sks': 3, 'jam': 6},
        }, 
        'kompen': 3
    },{
        'nim': '2161422', 
        'nama': 'dwi', 
        'prestasi': 1, 
        'nilai': {
            'Keamanan Informasi': {'n': 3.0, 'sks': 3, 'jam': 6}, 
            'E-Business': {'n': 3.1, 'sks': 3, 'jam': 6},
            'Pemrograman Platform Bergerak (Mobile)': {'n': 3.5, 'sks': 3, 'jam': 6},
            'Sistem Pendukung Keputusan': {'n': 2.0, 'sks': 3, 'jam': 6},
            'Pengolahan Citra Digital': {'n': 4.0, 'sks': 3, 'jam': 6},
            'Proyek Tingkat III': {'n': 3.5, 'sks': 3, 'jam': 6},
        }, 
        'kompen': 3
    }
]
data_list = []
for row in data:
    data_list.append({
        'nim': row['nim'],
        'nama': row['nama'],
        'prestasi': row['prestasi'],
        'kompen': row['kompen'],
        **row['nilai']
    })
matakuliah = []
for mahasiswa in data:
    for matakuliah_key, matakuliah_value in mahasiswa['nilai'].items():
        matakuliah.append({
            'matkul': matakuliah_key,
            'sks': matakuliah_value['sks'],
            'jam': matakuliah_value['jam']
        })

print(matakuliah)

def calculate_weights(length):
    # Define the rank of the criteria
    # rank = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rank = []
    for x in range(length):
        rank.append(x+1)
    # Calculate the length of the rank list
    n = len(rank)
    # Initialize an empty list for the weights
    weights = []
    # Loop through each value in the rank list
    for i in rank:
        # Calculate the weight for each value
        # w = sum([1 / (n - j + 1) for j in range(i, n + 1)]) / n
        w = sum([1 / j for j in range(i, n + 1)]) / n
        # Append the weight to the list
        weights.append(w)
    # Convert the list to a numpy array
    weights = np.array(weights)
    
    # Return the weights
    return weights

print(calculate_weights(9))

asddd = calculate_weights(9) / calculate_weights(9).sum()
print(asddd)

def normalize_matrix(self):
    # Get the matrix from the get_criteria_alternatives method
    criteria, alternatives, matrix = self.get_criteria_alternatives()
    # Normalize the matrix using vector normalization
    norm_matrix = matrix / np.sqrt(np.sum(matrix ** 2, axis=0))
    # Return the normalized matrix
    return norm_matrix, criteria