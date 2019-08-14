import os
import glob
import numpy as np
import pandas as pd
import numpy.random

files = glob.glob('models/DK_atlas_pial/lh.*')
files = list(np.sort([f.split('.')[3] for f in files]))
desikanKillianyDict = dict(zip(files, files))
print(files)
print('desikanKillianyDict',desikanKillianyDict)
print('\n\n')

# generate template for DK
nrBiomk = len(files)
desikanKillianyDf = pd.DataFrame(index=range(2), columns=['Image-name-unique'] + files)
desikanKillianyDf.loc[0,'Image-name-unique'] = 'Image_1'
desikanKillianyDf.loc[0,files[0]:] = numpy.random.rand(nrBiomk) * 3
desikanKillianyDf.loc[1,'Image-name-unique'] = 'Image_2'
desikanKillianyDf.loc[1,files[0]:] = numpy.random.rand(nrBiomk) * 3
desikanKillianyDf.to_csv('input/DK_template.csv', index=False)
print(desikanKillianyDf)

# asd

files = glob.glob('models/Destrieux_atlas_pial/lh.*')
files = np.sort([f.split('.')[3] for f in files])
destrieuxDict = dict(zip(files, files))
print(files)
print('destrieuxDict',destrieuxDict)
print('\n\n')

TODO generate templates for other atlases

files = glob.glob('models/DKT_atlas_pial/lh.*')
files = np.sort([f.split('.')[3] for f in files])
tourvilleDict = dict(zip(files, files))
print(files)
print('tourvilleDict',tourvilleDict)