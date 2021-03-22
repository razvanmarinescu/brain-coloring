import os
import glob
import numpy as np
import pandas as pd
import numpy.random

import config

subcortFiles = list(config.subcortAreasIndexMap.values())
subcortMouseFiles = list(config.subcortMouseAreasIndexMap.values())
destrieuxFiles = list(config.cortAreasIndexMapDestrieux.keys())
DKFiles = list(config.cortAreasIndexMapDK.keys())
miceFiles = list(config.cortAreasIndexMapMice.keys())
tourvilleFiles = list(config.cortAreasIndexMapTourville.keys())
tourvilleFiles = list(config.cortAreasIndexMapTourville.keys())

def templateCreator(indexMap, templateName, subcorticalFiles, nrImages, inputLocation): 
  # makes templates for each atlas
  files = indexMap + subcorticalFiles

  atlasDict = dict(zip(files, files))
  print(files)
  print(templateName,atlasDict)
  print('\n\n')

  # generate template 
  nrBiomk = len(files)
  atlasDf = pd.DataFrame(index=range(nrImages), columns=['Image-name-unique'] + files)

  for i in range(nrImages):  # number of images to generate
    atlasDf.loc[i,'Image-name-unique'] = 'Image_%d' % i
    atlasDf.loc[i,files[0]:] = numpy.random.rand(nrBiomk) * 3
  atlasDf.to_csv(inputLocation, index=False)
  print(atlasDf)


# DK template many
templateCreator(DKFiles, 'DK', subcortFiles, 20, 'input/DK_template.csv')

# DK template
templateCreator(DKFiles, 'DK', subcortFiles, 2, 'input/DK_template.csv')

# destrieux template
templateCreator(destrieuxFiles, 'Destrieux', subcortFiles, 2, 'input/Destrieux_template.csv') 

# tourville template
templateCreator(tourvilleFiles, 'Tourville', subcortFiles, 2, 'input/Tourville_template.csv') 

# mouse template
templateCreator(miceFiles, 'MouseTemplate', subcortMouseFiles, 2, 'input/mouse_template.csv') 

