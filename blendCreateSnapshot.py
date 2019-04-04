#!BPY


#import Blender
import scipy.io
import bpy
import numpy as np
import colorsys
from abc import ABC, abstractmethod
import os
import argparse
import sys
import glob
import pandas as pd

import config


blendFullPath = os.path.abspath('.')
# print(blendFullPath)
os.chdir(blendFullPath)
sys.path.append(blendFullPath)
from blendHelper import *


# filename = 'blendCreateSnapshot.py'
# exec(compile(open('blendCreateSnapshot.py').read(), 'blendCreateSnapshot.py', 'exec'))

#argv = sys.argv

#if "--" not in argv:
#  argv = []  # as if no args are passed
#else:
#  argv = argv[argv.index("--") + 1:]  # get all args after "--"

#parser = argparse.ArgumentParser(description='Launches processes that previously failed, i.e. which have missing idealLiks files')
#parser.add_argument('--cortical', action="store_true", help='set this is you want to draw cortical regions, otherwise will draw subcortical regions')
#args = parser.parse_args()



# INPUT_FILES_SHORT = ['14082016', '17082016_ADNI1pt5T', '17082016_ADNI3T', '17082016_C9orf72_1Seq', '17082016_C9orf72', '17082016_GRN', '17082016_MAPT_1Seq', '17082016_MAPT', '17082016_MUTpos']#, '17082016_Static']
# INPUT_FILES_LONG = ['%s/Plotting_Raz_%s.mat' % (EXPERIMENT_NAME, x) for x in INPUT_FILES_SHORT]

#INPUT_FILES_LONG = ['Plotting_Raz_06032017_MUTposFTSXVal.mat']
# the static matrix should be the last one, as it gets removed later
INPUT_FILE = config.INPUT_FILE
print(INPUT_FILE)


OUT_FOLDER = config.OUTPUT_FOLDER

# white -> red
COLOR_POINTS = [np.array(x) for x in config.COLORS_RGB]
NR_SIGN_LEVELS = len(COLOR_POINTS)-1

IMG_TYPE = config.IMG_TYPE

BRAIN_TYPE = config.BRAIN_TYPE

#print(SNAP_STAGES, NR_STAGES, labels, nonZlabels)

# take the EBMlabels and find their indices, then construct the two indexMaps below
# 'Frontal Lobe Atrophy' 0
# 'Parietal Lobe Atrophy' 1
# 'Temporal Lobe Atrophy' 2
# 'Occipital Lobe Atrophy' ...
# 'Cingulate Atrophy'
# 'Insula Atrophy'
# 'Amygdala Atrophy'
# 'Hippocampus Atrophy'
# 'Pallidum Atrophy'
# 'Putamen Atrophy'
# 'Thalamus Atrophy'



# map to amygdala 6, hippocampus 7, pallidum 8, putamen 9, thalamus 10
subcortAreasIndexMap = config.subcortAreasIndexMap

# map between subcortical areas and the biomarkers from EBMlabels, used in Alex's matrices, starting from 0
subcortRightAreas = ['Right' + x[4:] for x in subcortAreasIndexMap.keys()]
subcortRightAreasIndexMap = dict(zip(subcortRightAreas, subcortAreasIndexMap.values()))
subcortAreasIndexMap.update(subcortRightAreasIndexMap)
subcortAreas = [x for x in subcortAreasIndexMap.keys() if subcortAreasIndexMap[x] != -1]
subcortFiles = ['./models/subcortical_ply/%s.ply' % x for x in subcortAreas]
#subcortAreasIndexMap = [12, 9, 6, -1, 11, 13, 8, 6, 7, -1, 10, -1]

# map to frontal 0, parietal 1, temporal 2, occipital 3, cingulate 4, insula 5

cortAreasIndexMap = config.cortAreasIndexMap
cortAreas = cortAreasIndexMap.keys()

cortFilesRight = ['models/DK_atlas_%s/rh.%s.DK.%s.ply' % (BRAIN_TYPE, BRAIN_TYPE, x) for x in cortAreas]
cortFilesLeft = ['models/DK_atlas_%s/lh.%s.DK.%s.ply' % (BRAIN_TYPE, BRAIN_TYPE, x) for x in cortAreas]
cortFilesAll = cortFilesLeft + cortFilesRight
cortAreasNamesFull = [x.split("/")[-1][:-4] for x in cortFilesAll]
#make cortAreasIndexMap map from blender obj name to index of biomk in nonZlabels
cortAreasIndexMap = dict(zip(cortAreasNamesFull, 2*list(cortAreasIndexMap.values())))


# merge the 2 dicts
#allRegionsIndexMap = subcortAreasIndexMap.copy()
#allRegionsIndexMap.update(cortAreasIndexMap)

nrSubcortRegions = len(subcortAreas)
nrCortRegions = len(cortFilesAll)

if IMG_TYPE == 'subcortical':
  #loadSubcortical(cortFilesRight,subcortFiles)
  painter = SubcorticalPainter(cortFilesRight,subcortFiles)
  indexMap = subcortAreasIndexMap
elif IMG_TYPE == 'cortical':
  #loadCortical(cortFilesAll)
  painter = CorticalPainter(cortFilesAll)
  indexMap = cortAreasIndexMap
else:
  raise ValueError('mode has to be either cortical or subcortical')

painter.prepareScene(resolution=config.RESOLUTION, bckColor = config.BACKGROUND_COLOR)
painter.loadMeshes()


fileIndex = 0
# indexMapCurr = indexMap.copy()


# matDict = scipy.io.loadmat(INPUT_FILE)
matDf = pd.read_csv(INPUT_FILE)

print(matDf)

labels = matDf.columns.to_list()
print('-------------%s---------', INPUT_FILE)
print(labels)


#zscoreEventIndices = matDict['zscore_event'] # array of numbers showing which sigma level is used in entries of labels
NR_EVENTS = len(labels) # nr events, could be more than nr of biomk if different sigma levels are used
SNAP_STAGES = range(NR_EVENTS+1) # stages at which to take the snapshots
NR_STAGES = len(SNAP_STAGES)

INPUT_FILES_SHORT = ['%d.png' % x for x in range(matDf.shape[0])]
# generate latex and write it to file
inputFile = INPUT_FILES_SHORT[fileIndex]
outFolderCurrMat = OUT_FOLDER
#os.system("cd %s && xelatex %s" % (outFileName.split("/")[0], outFileName.split("/")[1] ))
# os.system("cd %s && pdflatex %s" % (outFileName.split("/")[0], outFileName.split("/")[1] ))


colorRegionsAndRender(indexMap, matDf, COLOR_POINTS, OUT_FOLDER, IMG_TYPE)

#print(asda)

#delobj()
