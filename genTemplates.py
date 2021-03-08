import os
import glob
import numpy as np
import pandas as pd
import numpy.random

import config

subcortFiles = list(config.subcortAreasIndexMap.values())
subcortMouseFiles = list(config.subcortMouseAreasIndexMap.values())

def templateCreator(path, templateName, subcorticalFiles, nrImages, inputLocation): 
  # makes templates for each atlas
  filesLeft = glob.glob(path + 'lh.*')
  filesLeft = list(np.sort(['Left-' + f.split('.')[3] for f in filesLeft])) 

  filesRight = glob.glob(path + 'rh.*')
  filesRight = list(np.sort(['Right-' + f.split('.')[3] for f in filesRight]))
  files = filesLeft + filesRight + subcorticalFiles

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
templateCreator('models/DK_atlas_pial/', 'DK', subcortFiles, 20, 'input/DK_template.csv')

# DK template
templateCreator('models/DK_atlas_pial/', 'DK', subcortFiles, 2, 'input/DK_template.csv')

# destrieux template
templateCreator('models/Destrieux_atlas_pial/', 'Destrieux', subcortFiles, 2, 'input/Destrieux_template.csv') 

# tourville template
templateCreator('models/DKT_atlas_pial/', 'Tourville', subcortFiles, 2, 'input/Tourville_template.csv') 

# mouse template
templateCreator('models/Mice_atlas_pial/', 'MouseTemplate', subcortMouseFiles, 2, 'input/mouse_template.csv') 



