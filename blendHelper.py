import scipy.io
import bpy
import numpy as np
import colorsys
from abc import ABC, abstractmethod
import os
import argparse
import sys
import glob

def getInterpColor(abn_level, sigmaLevel, NR_SIGN_LEVELS, COLOR_POINTS):
  # given an abnormality level, it computes the associated color
  # works in HSV space

  #print "abn_level: %f" % abn_level
  assert(0 <= abn_level <= 3.001) # it can exceed 1 because I add the abnormalities for consecutive sigmas together

  if 2 >= abn_level > 1:
    sigmaLevel += 1
    abn_level -= 1

  if abn_level > 2:
    sigmaLevel += 2
    abn_level -= 2

  if sigmaLevel > NR_SIGN_LEVELS: # maximum displayed is 3sigma, so anything above is proj. to 3sigma
    sigmaLevel = 3
    abn_level = 1

  # hue - 120 green 80 - yellow 40 - orange 0 -red
  #hue = HUE_START - HUE_CHUNK*(sigmaLevel-1 + abn_level)
  rgb_color = (1-abn_level)*COLOR_POINTS[sigmaLevel-1] + abn_level*COLOR_POINTS[sigmaLevel]
  #rgb_color = colorsys.hsv_to_rgb(hue/360, 1, 1)
  return rgb_color

def nZeroOne(a):
  return not (a == 0 or a == 1)


class BrainPainter(ABC):
  @abstractmethod
  def loadMeshes(self):
    pass

  def prepareScene(self):
    # delete the cube
    scene = bpy.context.scene
    for ob in scene.objects:
      if ob.type == 'MESH' and ob.name.startswith("Cube"):
        ob.select = True
      else:
        ob.select = False
    bpy.ops.object.delete()
    bpy.data.worlds['World'].horizon_color = (1, 1, 1)

    self.setCamera()
    self.setLamp()

  def deletePrevLamps(self):
    scene = bpy.data.scenes["Scene"]
    for key in [k for k in scene.objects.keys() if k.startswith('Lamp')]:
      scene.objects[key].select = True
    bpy.ops.object.delete()

    for lamp_data in bpy.data.lamps:
      bpy.data.lamps.remove(lamp_data)

  def prepareCamera(self):
    scene = bpy.data.scenes["Scene"]

    # Set render resolution
    scene.render.resolution_x = 1200  # resolutions are twice what shown here
    scene.render.resolution_y = 900

    # Set camera fov in degrees
    fov = 50.0
    pi = 3.14159265
    scene.camera.data.angle = fov * (pi / 180.0)

    # Set camera rotation in euler angles
    scene.camera.rotation_mode = 'XYZ'

  @abstractmethod
  def setCamera(self):
    pass

  @abstractmethod
  def setLamp(self):
    pass


class CorticalPainter(BrainPainter):
  def __init__(self, cortFiles):
    self.cortFiles = cortFiles

    # def loadCortical(cortFiles):

  def loadMeshes(self):
    # import cortical regions and set them to be almost transparent
    for i in range(len(self.cortFiles)):
      bpy.ops.import_mesh.ply(filepath=self.cortFiles[i])

    if bpy.context.selected_objects:
      for obj in bpy.context.selected_objects:
        regionName = obj.name
        if not 'mat_%s' % regionName in bpy.data.materials.keys():
          material = makeMaterial('mat_%s' % regionName, (0.3, 0.3, 0.3), (1, 1, 1), 1.0)
          obj.data.materials.append(material)
        else:
          material = bpy.data.materials['mat_%s' % regionName]
          material.diffuse_color = (0.3, 0.3, 0.3)
          material.alpha = 1
          obj.data.materials.append(material)

  def setCamera(self):

    scene = bpy.data.scenes["Scene"]

    self.prepareCamera()

    pi = 3.14159265
    scene.camera.rotation_euler = (pi / 2, 0, -3 * pi / 2)
    # Set camera location
    scene.camera.location = (167.00, -15.1, 3.824)

    bpy.data.cameras['Camera'].type = 'ORTHO'
    bpy.data.cameras['Camera'].ortho_scale = 178
    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self):

    energyAll = 5
    distanceAll = 1000

    scene = bpy.data.scenes["Scene"]
    self.deletePrevLamps()

    lampIndices = [1, 2, 3, 4]
    lampLocs = [(136, 45, 72), (136, -105, -64), (136, -105, 72), (136, 45, -64)]
    nrLamps = len(lampIndices)

    for l in range(nrLamps):
      # Create new lamp datablock
      lamp_data = bpy.data.lamps.new(name="lamp%d data" % lampIndices[l], type='POINT')
      # Create new object with our lamp datablock
      lamp = bpy.data.objects.new(name="Lamp%d" % lampIndices[l], object_data=lamp_data)
      # Link lamp object to the scene so it'll appear in this scene
      scene.objects.link(lamp)
      # Place lamp to a specified location
      scene.objects['Lamp%d' % lampIndices[l]].location = lampLocs[l]
      lamp_data.energy = energyAll
      lamp_data.distance = distanceAll


      # print(lampaaa)


class SubcorticalPainter(BrainPainter):
  def __init__(self, cortFiles, subcortFiles):
    self.cortFiles = cortFiles
    self.subcortFiles = subcortFiles

  # def loadSubcortical(self, cortFiles, subcortFiles):
  def loadMeshes(self):
    # import cortical regions and set them to be almost transparent
    for i in range(len(self.cortFiles)):
      bpy.ops.import_mesh.ply(filepath=self.cortFiles[i])

    if bpy.context.selected_objects:
      for obj in bpy.context.selected_objects:
        regionName = obj.name
        if not 'mat_%s' % regionName in bpy.data.materials.keys():
          material = makeMaterial('mat_%s' % regionName, (0.3, 0.3, 0.3), (1, 1, 1), 0.1)
          obj.data.materials.append(material)
        else:
          bpy.data.materials['mat_%s' % regionName].diffuse_color = (0.3, 0.3, 0.3)
          bpy.data.materials['mat_%s' % regionName].alpha = 1

        obj.select = False

    # import subcortical regions
    for i in range(len(self.subcortFiles)):
      bpy.ops.import_mesh.ply(filepath=self.subcortFiles[i])

    if bpy.context.selected_objects:
      for obj in bpy.context.selected_objects:
        regionName = obj.name
        if not 'mat_%s' % regionName in bpy.data.materials.keys():
          material = makeMaterial('mat_%s' % regionName, (0.3, 0.3, 0.3), (1, 1, 1), 1)
          obj.data.materials.append(material)
        else:
          # assert(False)
          material = bpy.data.materials['mat_%s' % regionName]
          material.diffuse_color = (0.3, 0.3, 0.3)
          material.alpha = 1
          obj.data.materials.append(material)

  def setCamera(self):

    scene = bpy.data.scenes["Scene"]
    self.prepareCamera()

    # scene.camera.rotation_euler = (1.15, -0.02, -8.63) # subcort only
    scene.camera.rotation_euler = (1.1499, -0.01999, -8.2985)  # half-cort hald subcort

    # Set camera translation
    # scene.camera.location = (-107.3, 66.8, 43.1) # subcort only
    scene.camera.location = (-168.3, 66.8, 83.1)  # half cort half subcort

    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self):

    energyAll = 7
    distanceAll = 1000

    scene = bpy.data.scenes["Scene"]
    self.deletePrevLamps()

    lampIndices = [1, 2]
    lampLocs = [(-82.53, 0.79, 72.87), (88.53, 119.79, 72.87)]

    nrLamps = len(lampIndices)

    for l in range(nrLamps):
      # Create new lamp datablock
      lamp_data = bpy.data.lamps.new(name="lamp%d data" % lampIndices[l], type='POINT')
      # Create new object with our lamp datablock
      lamp = bpy.data.objects.new(name="Lamp%d" % lampIndices[l], object_data=lamp_data)
      # Link lamp object to the scene so it'll appear in this scene
      scene.objects.link(lamp)
      # Place lamp to a specified location
      scene.objects['Lamp%d' % lampIndices[l]].location = lampLocs[l]
      lamp_data.energy = energyAll
      lamp_data.distance = distanceAll


def delobj():
  scene = bpy.data.scenes["Scene"]
  for ob in scene.objects:
    if ob.type == 'MESH' and (
          ob.name.startswith("Left") or ob.name.startswith("Right") or ob.name.startswith('lh.') or ob.name.startswith(
      'rh.')):
      ob.select = True
    else:
      ob.select = False
    if ob.name.startswith('Lamp'):
      ob.select = True
  bpy.ops.object.delete()
  bpy.ops.object.material_slot_remove()
  for material in bpy.data.materials:
    if not material.users:
      bpy.data.materials.remove(material)


def getStages(NR_EVENTS, NR_STAGES):
  return [int(x * float(NR_EVENTS) / NR_STAGES) for x in range(1, NR_STAGES + 1)]


def makeMaterial(name, diffuse, specular, alpha):
  mat = bpy.data.materials.new(name)
  mat.diffuse_color = diffuse
  mat.diffuse_shader = 'LAMBERT'
  mat.diffuse_intensity = 1.0
  mat.specular_color = specular
  mat.specular_shader = 'COOKTORR'
  mat.specular_intensity = 0.2
  mat.alpha = alpha
  mat.ambient = 1
  mat.use_transparency = True
  mat.use_shadows = False
  return mat


def setMaterial(ob, mat):
  me = ob.data
  me.materials.append(mat)


def createNonZtoZmap(nonZlabels, labels):
  nonZtoZMap = []

  labelsCut = [x.split('-')[0] for x in labels]
  # print(labelsCut)
  for nonZlabel in nonZlabels:
    nonZtoZMap += [[i for i in range(len(labelsCut)) if labelsCut[i] == nonZlabel]]

    # print(nonZlabel, [labels[i] for i in nonZtoZMap[-1]])

  return nonZtoZMap


def assignColor(signifAbnorm, signifColor, NR_SIGN_LEVELS, COLOR_POINTS):
  # assigns colors to a region, assumes biomarkers at different sigma levels called <region>-1 sigma <region>-2 sigma, etc ..

  # print('signifAbnorm ', signifAbnorm)
  # assert(len(signifAbnorm) <= 3)
  assert (len(signifAbnorm) == len(signifColor))

  for signifInd in range(len(signifAbnorm)):
    # some abnormalities end up as 1.000000001 or 0.999999,
    # approximate them to 1 or 0
    if abs(signifAbnorm[signifInd] - 1) < 0.025:
      signifAbnorm[signifInd] = 1
    if abs(signifAbnorm[signifInd] - 0) < 0.025:
      signifAbnorm[signifInd] = 0

  finalColor = signifColor[0]  # initialise color with sig1Color
  for signifInd in range(1, len(signifAbnorm)):
    if signifAbnorm[signifInd] > 0:
      finalColor = signifColor[signifInd]

  # if there are two possible conflicting colors, interpolate them
  if len(signifAbnorm) > 1 and nZeroOne(signifAbnorm[0]) and nZeroOne(signifAbnorm[1]):
    finalColor = getInterpColor(signifAbnorm[0] + signifAbnorm[1], 1, NR_SIGN_LEVELS, COLOR_POINTS)

  if len(signifAbnorm) > 2 and nZeroOne(signifAbnorm[1]) and nZeroOne(signifAbnorm[2]):
    finalColor = getInterpColor(signifAbnorm[1] + signifAbnorm[2], 2, NR_SIGN_LEVELS, COLOR_POINTS)

  if len(signifAbnorm) > 2 and nZeroOne(signifAbnorm[0]) \
    and nZeroOne(signifAbnorm[1]) and nZeroOne(signifAbnorm[2]):
    finalColor = getInterpColor(signifAbnorm[0] + signifAbnorm[1]
                                + signifAbnorm[2], 1, NR_SIGN_LEVELS, COLOR_POINTS)
    # raise ValueError('need to implement 3-color interpolation')

  return finalColor


def colorRegionsAndRender(indexMap, NR_MATRICES, NR_STAGES, NR_EVENTS,
  mats, MAT_NAMES, SNAP_STAGES, nonZtoZMap, NR_SIGN_LEVELS, COLOR_POINTS, OUT_FOLDER, inputFile, IMG_TYPE):
  objList = bpy.context.selected_objects[::-1]  # make sure to remove the cube from the scene
  # print(objList)

  eventsAbnormalityAll = np.zeros([NR_MATRICES, NR_STAGES, NR_EVENTS], float)
  # for matrixIndex in [0]:
  for matrixIndex in range(0, NR_MATRICES):
    # matrixIndex = 0
    matrix = mats[matrixIndex]
    matrixName = MAT_NAMES[matrixIndex]

    for stageIndex in range(NR_STAGES):
      # for stageIndex in [5]:

      # stageIndex = 3

      # for each event get the sum of all the probabilities until the current stage
      eventsAbnormality = np.sum(matrix[:, :SNAP_STAGES[stageIndex]], 1)

      assert (len(eventsAbnormality) == NR_EVENTS)
      eventsAbnormalityAll[matrixIndex, stageIndex, :] = eventsAbnormality

      # calc abnorm for plottable biomk
      if bpy.context.selected_objects:
        for obj in bpy.context.selected_objects:
          # print(obj.name, obj, obj.type)
          regionName = obj.name

          if regionName in indexMap.keys():
            # 'Left-Caudate -> nonZlabelNr -> [z-labelNrs], between 1-3'
            nonZlabelNr = indexMap[regionName]
            if nonZlabelNr != -1:
              eventEntriesCurr = nonZtoZMap[nonZlabelNr]

              # abnormality values for each significance levels
              signifAbnorm = [eventsAbnormality[x] for x in eventEntriesCurr]

              # colors for each significance levels
              signifColor = [getInterpColor(signifAbnorm[sigmaLevel - 1], sigmaLevel,
                NR_SIGN_LEVELS, COLOR_POINTS) for sigmaLevel in
                range(1, len(signifAbnorm) + 1)]

              print("regionName", regionName, nonZlabelNr, eventEntriesCurr)
              # print(adsas)
              finalColor = assignColor(signifAbnorm, signifColor, NR_SIGN_LEVELS, COLOR_POINTS)
              # print(finalColor)
              # if regionName == 'rh.pial.DK.inferiortemporal':
              #   print('finalColor', finalColor)
              #   print('eventEntriesCurr', eventEntriesCurr)
              #   print('eventsAbnormality', eventsAbnormality)
              #   print('signifAbnorm', signifAbnorm)
              #   print('signifColor', signifColor)
              #   print(adsa)

              # material = makeMaterial('mat_%d_%d_%s' % (matrixIndex, stageIndex, regionName), finalColor, (1,1,1), 1)
              # setMaterial(obj, material)
              # obj.material_slots[0].material = bpy.data.materials['mat_%d_%d_%s' % (matrixIndex, stageIndex, regionName)]
              bpy.data.materials['mat_%s' % regionName].diffuse_color = finalColor

              # obj.data.materials.append(material)

          else:
            print('object not found: %s', obj.name)

      # print(adsas)
      outputFile = '%s/%s/%s/%s_stage%d.png' % (
      OUT_FOLDER, inputFile, matrixName, IMG_TYPE, SNAP_STAGES[stageIndex])
      print('rendering file %s', outputFile)
      bpy.data.scenes['Scene'].render.filepath = outputFile
      bpy.ops.render.render(write_still=True)

  return eventsAbnormalityAll


def createLatex(NR_MATRICES, NR_STAGES, NR_EVENTS,
  mats, MAT_NAMES, SNAP_STAGES, nonZtoZMap, blobsNonZNrs, blobsNames,
  NR_SIGN_LEVELS, COLOR_POINTS, NR_BALLS, BALL_COORDS, blobsLabels):
  eventsAbnormalityAll = np.zeros([NR_MATRICES, NR_STAGES, NR_EVENTS], float)
  text = r'''
\documentclass[11pt,a4paper,oneside]{report}

\usepackage{float}
\usepackage{tikz}
\usetikzlibrary{plotmarks}
\usepackage{amsmath,graphicx}
\usepackage{epstopdf}
\usepackage[font=normal,labelfont=bf]{caption}
\usepackage{subcaption}
\usepackage{color}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{scalefnt}

% margin size
\usepackage[margin=1in]{geometry}

\begin{document}
\belowdisplayskip=12pt plus 3pt minus 9pt
\belowdisplayshortskip=7pt plus 3pt minus 4pt

% scale parameter for the circles and the gradient
\tikzset{every picture/.append style={scale=0.5}}
% scale parameter for the upper and lower small brain images
\newcommand*{\scaleBrainImg}{0.1}'''

  for matrixIndex in range(NR_MATRICES):
    matrix = mats[matrixIndex]

    for stageIndex in range(NR_STAGES):
      # for each event get the sum of all the probabilities until the current stage
      eventsAbnormality = np.sum(matrix[:, :SNAP_STAGES[stageIndex]], 1)

      assert (len(eventsAbnormality) == NR_EVENTS)
      eventsAbnormalityAll[matrixIndex, stageIndex, :] = eventsAbnormality

      for ballIndex, blobNZNr in enumerate(blobsNonZNrs):
        indicesZ = nonZtoZMap[blobNZNr]
        # abnormality values for each significance levels
        signifAbnorm = [eventsAbnormality[x] for x in indicesZ]
        print("blobName", blobsNames[ballIndex], blobNZNr, indicesZ, signifAbnorm)
        print('nonZtoZMap', nonZtoZMap)

        # colors for each significance levels
        signifColor = [getInterpColor(signifAbnorm[sigmaLevel - 1], sigmaLevel,
          NR_SIGN_LEVELS, COLOR_POINTS) for sigmaLevel in
                       range(1, len(signifAbnorm) + 1)]

        finalColor = assignColor(signifAbnorm, signifColor, NR_SIGN_LEVELS, COLOR_POINTS)
        # print(finalColor)

        text += r'''
\definecolor{col''' + "%d%d%d" % (
          matrixIndex, stageIndex, ballIndex) + '''}{rgb}{''' + '%.3f,%.3f,%.3f' % (finalColor[0], finalColor[1], finalColor[2]) + '''}'''

  text += '''\n\n '''


  for matrixIndex in range(NR_MATRICES):
    matrix = mats[matrixIndex]

    text += r'''

\begin{figure}[H]
  \centering'''
    for stageIndex in range(NR_STAGES):

      # for each event get the sum of all the probabilities until the current stage
      eventsAbnormality = np.sum(matrix[:,:SNAP_STAGES[stageIndex]],1)

      assert(len(eventsAbnormality) == NR_EVENTS)
      eventsAbnormalityAll[matrixIndex, stageIndex, :] = eventsAbnormality

      text += r'''
        %\begin{subfigure}[b]{0.15\textwidth}
      \begin{tikzpicture}[scale=1.0,auto,swap]

      % the two brain figures on top
      \node (cortical_brain) at (0,1.5) { \includegraphics*[scale=\scaleBrainImg,trim=0 0 0 0]{'''

      text += '%s/cortical_stage%d.png' % (MAT_NAMES[matrixIndex], SNAP_STAGES[stageIndex]) + r'''}};
      \node (subcortical_brain) at (0,-1.5) { \includegraphics*[scale=\scaleBrainImg,trim=0 0 0 0]{'''
      text += '%s/subcortical_stage%d.png' % (MAT_NAMES[matrixIndex], SNAP_STAGES[stageIndex]) + r'''}};
      '''
      text += r'''\node (stage) at (0, 3.4) {Stage ''' + "%d" % SNAP_STAGES[stageIndex] + r'''};
      '''

      for ballIndex in range(NR_BALLS):
        text += '''\draw[fill=''' + "col%d%d%d" % (
        matrixIndex, stageIndex, ballIndex) + "] (%1.1f,%1.1f)" % (BALL_COORDS[ballIndex][0], BALL_COORDS[ballIndex][1]) + \
        ''' circle [radius=0.33cm] node {\scriptsize ''' + "%s" % blobsLabels[ballIndex] + '''};
          '''

      text += r'''\end{tikzpicture}
    %\end{subfigure}
    % next subfigure
    \hspace{-1.5em}
    ~'''

    upperLimitGradient = 6
    lowerLimitGradient = 0
    chunkLen = ((upperLimitGradient - lowerLimitGradient)/NR_SIGN_LEVELS)
    text += r'''
  \hspace{1em}
  % the red-to-yellow gradient on the right
  \begin{tikzpicture}[scale=1.1,auto,swap]
    \colorlet{redhsb}[hsb]{red}%
    \colorlet{bluehsb}[hsb]{blue}%
    \colorlet{yellowhsb}[hsb]{yellow}%
    \colorlet{orangehsb}[hsb]{orange}%
    \colorlet{magentahsb}[hsb]{magenta}%
    \shade[bottom color=white,top color=red] (0,0) rectangle (0.5,2.01); % bottom rectangle
    \shade[bottom color=red,top color=magenta] (0,2) rectangle (0.5,4.01);
    \shade[bottom color=magenta,top color=blue] (0,4) rectangle (0.5,6); % top rectangle
'''
    sigmaLabels = ['normal', '2-sigma', '3-sigma', '5-sigma']
    for s in range(NR_SIGN_LEVELS+1):
      text += "\n    \draw (0,%d) -- (0.5,%d);" % (s*chunkLen, s*chunkLen)
      text += r'''\node[inner sep=0] (corr_text) at (1.7,''' + str(s*chunkLen) + r''') {''' + sigmaLabels[s] + r'''};
'''
    text += r'''
  \end{tikzpicture}
  \caption{''' + " ".join(MAT_NAMES[matrixIndex].split("_")) +'''}
\end{figure}
'''

  text += r'''
\end{document}

'''

  return text