#!BPY

import sys
print('blender python:', sys.exec_prefix)


import bpy
import numpy as np
import os
import pandas as pd



# filename = 'blendCreateSnapshot.py'
# exec(compile(open('blendCreateSnapshot.py').read(), 'blendCreateSnapshot.py', 'exec'))

blendFullPath = os.path.abspath('.')
os.chdir(blendFullPath)
sys.path.append(blendFullPath)
from blendHelper import *
from fileFormatChecker import *

# if environment variable configFile is set, read the path from there. Otherwise, load ./config.py
configFile = os.getenv('configFile', './config.py')
import importlib.util
spec = importlib.util.spec_from_file_location("module.name", configFile)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)


INPUT_FILE = config.INPUT_FILE
print(INPUT_FILE)


OUT_FOLDER = config.OUTPUT_FOLDER

COLORS_RGB = config.COLORS_RGB
COLOR_POINTS = [np.array(x) for x in COLORS_RGB]
NR_SIGN_LEVELS = len(COLOR_POINTS)-1

IMG_TYPE = config.IMG_TYPE

BRAIN_TYPE = config.BRAIN_TYPE

ATLAS = config.ATLAS

if ATLAS == 'DK':
  cortAreasIndexMap = config.cortAreasIndexMapDK
  subcortAreasIndexMap = config.subcortAreasIndexMap
elif ATLAS == 'Destrieux':
  cortAreasIndexMap = config.cortAreasIndexMapDestrieux
  subcortAreasIndexMap = config.subcortAreasIndexMap
elif ATLAS == 'Mice':
  cortAreasIndexMap = config.cortAreasIndexMapMice
  subcortAreasIndexMap = config.subcortMouseAreasIndexMap
elif ATLAS == 'Tourville':
  cortAreasIndexMap = config.cortAreasIndexMapTourville
  subcortAreasIndexMap = config.subcortAreasIndexMap
  ATLAS = 'DKT' # actually 3D models are labelled as DKT
elif ATLAS == 'Dorr':
  cortAreasIndexMap = config.cortAreasIndexMapDorr
  subcortAreasIndexMap = config.subcortDorrAreasIndexMap
elif ATLAS == 'Dsurque':
  cortAreasIndexMap = config.cortAreasIndexMapDsurque
  subcortAreasIndexMap = config.subcortDsurqueAreasIndexMap
elif ATLAS == 'Custom':
  cortAreasIndexMap = config.cortAreasIndexMapCustom
  subcortAreasIndexMap = config.subcortAreasIndexMapCustom
else:
  raise ValueError('ATLAS has to be either \'DK\', \'Destrieux\', \'Tourville\' or \'Custom\' ')

cortAreasList = cortAreasIndexMap.keys()
subcortAreasShort = subcortAreasIndexMap.keys()
cortAreas = []

cortRegionsThatShouldBeInTemplate = cortAreasIndexMap.values()
subcortRegionsThatShouldBeInTemplate = subcortAreasIndexMap.values()

for mesh in cortAreasList:
  if 'Right-' in mesh:
    cortAreas.append(mesh.replace('Right-', ''))
  elif 'Left-' in mesh:
    cortAreas.append(mesh.replace('Left-', ''))
cortAreas = list(set(cortAreas)) # remove duplicated items

cortFilesRight = ['models/%s_atlas_%s/rh.%s.%s.%s.ply' % (ATLAS, BRAIN_TYPE, BRAIN_TYPE, ATLAS, x) for x in cortAreas]
cortFilesLeft =  ['models/%s_atlas_%s/lh.%s.%s.%s.ply' % (ATLAS, BRAIN_TYPE, BRAIN_TYPE, ATLAS, x) for x in cortAreas]


cortFilesAll = list(set(cortFilesLeft + cortFilesRight))

cortAreasNamesFull = [x.split("/")[-1][:-4] for x in cortFilesAll]

cortAreasNamesMatching = [] # for the new mesh order
for index, mesh in enumerate(cortAreasNamesFull):
  if 'rh.' in mesh:
    cortAreasNamesMatching.append(cortAreasIndexMap.get('Right-' + mesh.split(".")[-1]))
  elif 'lh.' in mesh:
    cortAreasNamesMatching.append(cortAreasIndexMap.get('Left-' + mesh.split(".")[-1]))

cortAreasIndexMap = dict(zip(cortAreasNamesFull, cortAreasNamesMatching))


if ATLAS == 'Mice':
  subcortMiceAreas = [x[4:] for x in subcortAreasIndexMap.keys()]
  subcortMiceAreasIndexMap = dict(zip(subcortMiceAreas, subcortAreasIndexMap.values()))
  subcortAreas = [x for x in subcortAreasIndexMap.keys() if subcortAreasIndexMap[x] != -1]
  subcortFiles = ['./models/mouse_subcortical_ply/%s.ply' % x for x in subcortAreas]
else:
  subcortRightAreas = [x[4:] for x in subcortAreasIndexMap.keys()]
  subcortRightAreasIndexMap = dict(zip(subcortRightAreas, subcortRegionsThatShouldBeInTemplate))
  subcortAreas = [x for x in subcortAreasIndexMap.keys() if subcortAreasIndexMap[x] != -1]
  subcortFiles = ['./models/subcortical_ply/%s.ply' % x for x in subcortAreas]


nrSubcortRegions = len(subcortAreas)
nrCortRegions = len(cortFilesAll)

# merge cort and subcort index maps
cortIndexMap = cortAreasIndexMap.copy()
cortIndexMap.update(subcortAreasIndexMap) 
fullIndexMap = cortIndexMap # for mouse brain and cross section view

if IMG_TYPE == 'subcortical-outer-right-hemisphere' or IMG_TYPE == 'subcortical':
  painter = SubcorticalPainter(cortFilesRight,subcortFiles)
  indexMap = subcortAreasIndexMap
  areasShort = subcortAreasShort
  regionsThatShouldBeInTemplate = subcortRegionsThatShouldBeInTemplate
elif IMG_TYPE == 'subcortical-outer-left-hemisphere':
  painter = SubcorticalPainterLeft(cortFilesLeft,subcortFiles)
  indexMap = subcortAreasIndexMap
  areasShort = subcortAreasShort
  regionsThatShouldBeInTemplate = subcortRegionsThatShouldBeInTemplate
elif IMG_TYPE == 'subcortical-top':
  painter = SubcorticalPainterTop(cortFilesLeft,subcortFiles)
  indexMap = subcortAreasIndexMap
  areasShort = subcortAreasShort
  regionsThatShouldBeInTemplate = subcortRegionsThatShouldBeInTemplate
elif IMG_TYPE == 'subcortical-bottom':
  painter = SubcorticalPainterBottom(cortFilesLeft,subcortFiles)
  indexMap = subcortAreasIndexMap
  areasShort = subcortAreasShort
  regionsThatShouldBeInTemplate = subcortRegionsThatShouldBeInTemplate

# cortical painters  
# right side painter
elif IMG_TYPE == 'cortical-outer-right-hemisphere':
  # loadCortical(cortFilesAll)
  if ATLAS == 'Mice': painter = CorticalPainter(cortFilesAll, subcortFiles)
  else: painter = CorticalPainter(cortFilesRight)
  indexMap = fullIndexMap 
  areasShort = cortAreas
  regionsThatShouldBeInTemplate = cortRegionsThatShouldBeInTemplate
elif IMG_TYPE == 'cortical-inner-right-hemisphere':
  painter = CorticalPainterInnerRight(cortFilesRight, subcortFiles)
  indexMap = fullIndexMap
  areasShort = cortAreas
  regionsThatShouldBeInTemplate = cortRegionsThatShouldBeInTemplate

# left side painter
elif IMG_TYPE == 'cortical-outer-left-hemisphere':
  painter = CorticalPainterLeft(cortFilesLeft)
  if ATLAS == 'Mice': painter = CorticalPainterLeft(cortFilesLeft, subcortFiles)
  indexMap = fullIndexMap
  areasShort = cortAreas
  regionsThatShouldBeInTemplate = cortRegionsThatShouldBeInTemplate
elif IMG_TYPE == 'cortical-inner-left-hemisphere':
  painter = CorticalPainterInnerLeft(cortFilesLeft, subcortFiles)
  indexMap = fullIndexMap
  areasShort = cortAreas
  regionsThatShouldBeInTemplate = cortRegionsThatShouldBeInTemplate
elif IMG_TYPE == 'cortical-top' or IMG_TYPE == 'top': 
  painter = CorticalPainterTop(cortFilesAll, subcortFiles)
  indexMap = fullIndexMap
  areasShort = cortAreas
  regionsThatShouldBeInTemplate = cortRegionsThatShouldBeInTemplate
elif IMG_TYPE == 'cortical-bottom' or IMG_TYPE == 'bottom': 
  painter = CorticalPainterBottom(cortFilesAll, subcortFiles)
  indexMap = fullIndexMap
  areasShort = cortAreas
  regionsThatShouldBeInTemplate = cortRegionsThatShouldBeInTemplate
else:
  raise ValueError('mode has to be either cortical-outer, cortical-inner or subcortical')

fov = 50.0
if BRAIN_TYPE == 'inflated':
  ortho_scale = 280
elif IMG_TYPE in ['top', 'bottom']:
  ortho_scale = 190
else:
  ortho_scale = 180


matDf = pd.read_csv(INPUT_FILE)
labels = matDf.columns.to_list()


checkInputDf(matDf, regionsThatShouldBeInTemplate)


painter.prepareScene(resolution=config.RESOLUTION, bckColor = config.BACKGROUND_COLOR, fov=fov, ortho_scale=ortho_scale, BRAIN_TYPE=BRAIN_TYPE)
painter.loadMeshes()


print('-------------%s-------------' % INPUT_FILE)
colorRegionsAndRender(indexMap, matDf, COLOR_POINTS, OUT_FOLDER, IMG_TYPE)


# outFolderCurrMat = '%s' % (OUT_FOLDER.rsplit('/', 1)[0])
outFolderCurrMat = '%s' % OUT_FOLDER
text = genLaTex(INPUT_FILE, OUT_FOLDER, COLORS_RGB)
os.system('mkdir -p %s' % outFolderCurrMat)
out = open('%s/report.tex' % outFolderCurrMat, 'w')
out.write(text)
print("")
out.close()
