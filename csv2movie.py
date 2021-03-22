from os import sep
from numpy.lib.shape_base import split
import pandas as pd
import numpy as np
from config import *


INPUT = pd.read_csv('./input/mouse_template.csv')
template_location = './input/movie_template.csv' # where the generated movie csv data goes
ATLAS = 'Mice' # specify the Atlas you are using


columns = INPUT.columns[1:].tolist()
# print(columns)

rows = []
inputData = INPUT.values

# add zero matrix as initial value 
# this increments into the first value
keepZeros = False
biomarkerData = []

if keepZeros:
    biomarkerData = np.zeros(len(inputData[0]) - 1, dtype = int).tolist()
    biomarkerData = [biomarkerData]

for i in inputData: 
    biomarkerData.append(i[1:].tolist())



iter = 0
nrFrames = 8 # number of frames per data point

movieData = []

nrFrames-=1
for sub in range(len(biomarkerData) - 1):
    for count in range(int(nrFrames) + 1):
        split_data = []

        for i in range(len(columns)):
            number = biomarkerData[sub+1][i] - biomarkerData[sub][i]
            delta_change = count * (number/nrFrames)

            new_data_point = biomarkerData[sub][i] + delta_change

            split_data.append(new_data_point)
        
        count+=1
        movieData.append(split_data)

    print(count)

for i in range(len(movieData)):
    rows.append('Image_' + str(i))


movieData = pd.DataFrame(movieData, columns = columns, index = rows)
print(movieData)

movieData.to_csv(template_location, index=True, index_label='Image-name-unique')
