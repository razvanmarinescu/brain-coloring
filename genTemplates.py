import os
import glob
import numpy as np
import pandas as pd
import numpy.random

import config

subcortFiles = list(config.subcortAreasIndexMap.values())
subcortMouseFiles = list(config.subcortMouseAreasIndexMap.values())

files = glob.glob('models/DK_atlas_pial/lh.*')
files = list(np.sort([f.split('.')[3] for f in files])) + subcortFiles
desikanKillianyDict = dict(zip(files, files))
print(files)
print('desikanKillianyDict',desikanKillianyDict)
print('\n\n')

# generate template for DK with many entries
nrBiomk = len(files)
nrImages = 20
desikanKillianyDf = pd.DataFrame(index=range(20), columns=['Image-name-unique'] + files)
for i in range(nrImages):
  desikanKillianyDf.loc[i,'Image-name-unique'] = 'Image_%d' % i
  desikanKillianyDf.loc[i,files[0]:] = numpy.random.rand(nrBiomk) * 3
desikanKillianyDf.to_csv('input/DK_template_many.csv', index=False)
print(desikanKillianyDf)


# generate template for DK
nrBiomk = len(files)
desikanKillianyDf = pd.DataFrame(index=range(2), columns=['Image-name-unique'] + files)
desikanKillianyDf.loc[0,'Image-name-unique'] = 'Image_1'
desikanKillianyDf.loc[0,files[0]:] = numpy.random.rand(nrBiomk) * 3
desikanKillianyDf.loc[1,'Image-name-unique'] = 'Image_2'
desikanKillianyDf.loc[1,files[0]:] = numpy.random.rand(nrBiomk) * 3
desikanKillianyDf.to_csv('input/DK_template.csv', index=False)
print(desikanKillianyDf)



files = glob.glob('models/Destrieux_atlas_pial/lh.*')
files = list(np.sort([f.split('.')[3] for f in files])) + subcortFiles
destrieuxDict = dict(zip(files, files))
print('files', files)
print(type(files))
print([type(f) for f in files])
print('destrieuxDict',destrieuxDict)
print('\n\n')

# generate template for Destrieux
nrBiomk = len(files)
destrieuxDf = pd.DataFrame(index=range(2), columns=['Image-name-unique'] + files)
destrieuxDf.loc[0,'Image-name-unique'] = 'Image_1'
destrieuxDf.loc[0,files[0]:] = numpy.random.rand(nrBiomk) * 3
destrieuxDf.loc[1,'Image-name-unique'] = 'Image_2'
destrieuxDf.loc[1,files[0]:] = numpy.random.rand(nrBiomk) * 3
destrieuxDf.to_csv('input/Destrieux_template.csv', index=False)
print(destrieuxDf)


files = glob.glob('models/DKT_atlas_pial/lh.*')
files = list(np.sort([f.split('.')[3] for f in files])) + subcortFiles
tourvilleDict = dict(zip(files, files))
print(files)
print('tourvilleDict',tourvilleDict)


# generate template for Tourville
nrBiomk = len(files)
tourvilleDf = pd.DataFrame(index=range(2), columns=['Image-name-unique'] + files)
tourvilleDf.loc[0,'Image-name-unique'] = 'Image_1'
tourvilleDf.loc[0,files[0]:] = numpy.random.rand(nrBiomk) * 3
tourvilleDf.loc[1,'Image-name-unique'] = 'Image_2'
tourvilleDf.loc[1,files[0]:] = numpy.random.rand(nrBiomk) * 3
tourvilleDf.to_csv('input/Tourville_template.csv', index=False)
print(tourvilleDf)

# generate templates for Mouse Atlas
files = glob.glob('models/Mice_atlas_pial/fh*')
files = list(np.sort([f.split('.')[3] for f in files])) + subcortMouseFiles


mouseDict = dict(zip(files, files))
print(files)
print('MouseTemplate',mouseDict)
print('\n\n')

nrBiomk = len(files)
mouseDf = pd.DataFrame(index=range(2), columns=['Image-name-unique'] + files)
mouseDf.loc[0,'Image-name-unique'] = 'Image_1'
mouseDf.loc[0,files[0]:] = numpy.random.rand(nrBiomk) * 3
mouseDf.loc[1,'Image-name-unique'] = 'Image_2'
mouseDf.loc[1,files[0]:] = numpy.random.rand(nrBiomk) * 3
mouseDf.to_csv('input/mouse_template.csv', index=False)
print(mouseDf)