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



# filename = 'blendCreateSnapshot.py'
# exec(compile(open('blendCreateSnapshot.py').read(), 'blendCreateSnapshot.py', 'exec'))

blendFullPath = os.path.abspath('.')
# print(blendFullPath)
os.chdir(blendFullPath)
sys.path.append(blendFullPath)
from blendHelper import *
import config



INPUT_FILE = config.INPUT_FILE
print(INPUT_FILE)


OUT_FOLDER = config.OUTPUT_FOLDER

COLOR_POINTS = [np.array(x) for x in config.COLORS_RGB]
NR_SIGN_LEVELS = len(COLOR_POINTS)-1

IMG_TYPE = config.IMG_TYPE

BRAIN_TYPE = config.BRAIN_TYPE

subcortAreasIndexMap = config.subcortAreasIndexMap

subcortRightAreas = ['Right' + x[4:] for x in subcortAreasIndexMap.keys()]
subcortRightAreasIndexMap = dict(zip(subcortRightAreas, subcortAreasIndexMap.values()))
subcortAreasIndexMap.update(subcortRightAreasIndexMap)
subcortAreas = [x for x in subcortAreasIndexMap.keys() if subcortAreasIndexMap[x] != -1]
subcortFiles = ['./models/subcortical_ply/%s.ply' % x for x in subcortAreas]

cortAreasIndexMap = config.cortAreasIndexMap
cortAreas = cortAreasIndexMap.keys()

cortFilesRight = ['models/DK_atlas_%s/rh.%s.DK.%s.ply' % (BRAIN_TYPE, BRAIN_TYPE, x) for x in cortAreas]
cortFilesLeft = ['models/DK_atlas_%s/lh.%s.DK.%s.ply' % (BRAIN_TYPE, BRAIN_TYPE, x) for x in cortAreas]
cortFilesAll = cortFilesLeft + cortFilesRight
cortAreasNamesFull = [x.split("/")[-1][:-4] for x in cortFilesAll]
cortAreasIndexMap = dict(zip(cortAreasNamesFull, 2*list(cortAreasIndexMap.values())))


nrSubcortRegions = len(subcortAreas)
nrCortRegions = len(cortFilesAll)

if IMG_TYPE == 'subcortical':
  #loadSubcortical(cortFilesRight,subcortFiles)
  painter = SubcorticalPainter(cortFilesRight,subcortFiles)
  indexMap = subcortAreasIndexMap
elif IMG_TYPE == 'cortical-front':
  #loadCortical(cortFilesAll)
  painter = CorticalPainter(cortFilesAll)
  indexMap = cortAreasIndexMap
elif IMG_TYPE == 'cortical-back':
  painter = CorticalPainterBack(cortFilesRight)
  indexMap = cortAreasIndexMap
else:
  raise ValueError('mode has to be either cortical-front, cortical-back or subcortical')

painter.prepareScene(resolution=config.RESOLUTION, bckColor = config.BACKGROUND_COLOR)
painter.loadMeshes()


fileIndex = 0
matDf = pd.read_csv(INPUT_FILE)

labels = matDf.columns.to_list()
print('-------------%s---------', INPUT_FILE)
colorRegionsAndRender(indexMap, matDf, COLOR_POINTS, OUT_FOLDER, IMG_TYPE)

