import os
import glob
import numpy as np
import pandas as pd
import numpy.random

import config

subcortFiles = list(config.subcortAreasIndexMap.values())


def sig(x,a,b,c):
  return a/(1 + np.exp(-b*(x-c)))

files = glob.glob('models/DK_atlas_pial/lh.*')
files = list(np.sort([f.split('.')[3] for f in files])) + subcortFiles
desikanKillianyDict = dict(zip(files, files))
print(files)
print('desikanKillianyDict',desikanKillianyDict)
print('\n\n')

centersReg = {
  #'frontal':
               'caudalmiddlefrontal' : 0.3,
               'frontalpole' : 0.2,
               'lateralorbitofrontal' : 0.3,
               'medialorbitofrontal' :0.3,
               'paracentral' : 0.2,
               'parsopercularis':0.25,
               'parsorbitalis' :0.2,
               'parstriangularis':0.2,
               'precentral':0.8,
               'rostralmiddlefrontal':0.2,
               'superiorfrontal':0.4,
  #'parietal'
             'inferiorparietal':0.3,
             'postcentral':0.8,
             'precuneus':0,
             'superiorparietal':0.2,
             'supramarginal':0.25,
  # 'temporal'
             'entorhinal':-0.57,
             'fusiform':-0.3,
             'inferiortemporal':-0.3,
             'middletemporal':-0.2,
             'parahippocampal':-0.53,
             'superiortemporal':0,
             'temporalpole':-0.3,
             'transversetemporal':-0.47,
  # 'occipital'
             'cuneus':0,
             'lateraloccipital':0.3,
             'lingual':0.35,
             'pericalcarine':0.2,
  # 'cingulate'
             'caudalanteriorcingulate':0.45,
             'isthmuscingulate':0.55,
             'posteriorcingulate':0.5,
             'rostralanteriorcingulate':0.6,
  # subcortical
             'Accumbens-area':0.3,
             'Caudate':0.3,
             'Cerebellum-White-Matter':0,
             'Pallidum':0,
             'Thalamus-Proper':-0.2,
             'Amygdala':-0.2,
             'Cerebellum-Cortex':1.0,
             'Hippocampus':-0.7,
             'Putamen':0,
             'VentralDC' : 0,
             'bankssts' : 0,
             'insula':0,
             'unknown':0,
             'Inf-Lat-Vent':0,
             'Lateral-Ventricle':0
}


# generate template for DK with many entries
nrBiomk = len(files)
nrImages = 600
maxBiomkValue = 3
desikanKillianyDf = pd.DataFrame(index=range(0), columns=['Image-name-unique'] + files + ['Image-text'])


roiNames = list(centersReg.keys())

counter = 0
for i in range(nrImages):
#for i in [0,150,300,450,599]:
  desikanKillianyDf.loc[counter, 'Image-name-unique'] = 'Image_%d' % i
  for r in range(len(files)):
    timeIndex = (float(i) - 0.5*nrImages)/nrImages
    desikanKillianyDf.loc[counter,files[r]] = sig(timeIndex,a=maxBiomkValue,b=4,c=centersReg[files[r]])

  desikanKillianyDf.loc[counter, 'Image-text'] = 'Years since onset: %.1f ' % (float(20*i)/nrImages)

  counter += 1



#desikanKillianyDf.to_csv('../generated/DK_movie/DK_template_movie.csv', index=False)
desikanKillianyDf.to_csv('DK_template_movie.csv', index=False)
print(desikanKillianyDf)

