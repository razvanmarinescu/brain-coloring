import scipy.io
import bpy
import numpy as np
import pandas as pd
import colorsys
from abc import ABC, abstractmethod
import os
import argparse
import sys
import glob
import sys

def getInterpColor(abn_level, COLOR_POINTS):
  # given an abnormality level, it computes the associated color
  # works in HSV space

  if abn_level >= (len(COLOR_POINTS)-1):
    abn_level = len(COLOR_POINTS) - 1.01

  sigmaLevel = int(abn_level)
  abn_level -= sigmaLevel
  # print('abn_level', abn_level)
  # print('len(COLOR_POINTS)', len(COLOR_POINTS))
  # print('sigmaLevel', sigmaLevel)
  assert 0 <= abn_level <= 1

  # hue - 120 green 80 - yellow 40 - orange 0 -red
  rgb_color = (1-abn_level)*COLOR_POINTS[sigmaLevel] + abn_level*COLOR_POINTS[sigmaLevel+1]

  return rgb_color

def nZeroOne(a):
  return not (a == 0 or a == 1)


class BrainPainter(ABC):
  @abstractmethod
  def loadMeshes(self):
    pass

  def prepareScene(self, resolution, bckColor, fov, ortho_scale, BRAIN_TYPE):
    # delete the cube
    scene = bpy.context.scene
    for ob in scene.objects:
      if ob.type == 'MESH' and ob.name.startswith("Cube"):
        ob.select = True
      else:
        ob.select = False
    bpy.ops.object.delete()
    bpy.data.worlds['World'].horizon_color = bckColor

    self.setCamera(resolution, fov, ortho_scale, BRAIN_TYPE)
    self.setLamp(BRAIN_TYPE)

  def deletePrevLamps(self):
    scene = bpy.data.scenes["Scene"]
    for key in [k for k in scene.objects.keys() if k.startswith('Lamp')]:
      scene.objects[key].select = True
    bpy.ops.object.delete()

    for lamp_data in bpy.data.lamps:
      bpy.data.lamps.remove(lamp_data)

  def prepareCamera(self, resolution, fov):
    scene = bpy.data.scenes["Scene"]

    # Set render resolution
    scene.render.resolution_x = resolution[0]*2  # need to multiply by 2 for some reason
    scene.render.resolution_y = resolution[1]*2

    # Set camera fov in degrees

    pi = 3.14159265
    scene.camera.data.angle = fov * (pi / 180.0)

    # Set camera rotation in euler angles
    scene.camera.rotation_mode = 'XYZ'

  @abstractmethod
  def setCamera(self, resolution, fov, ortho_scale, BRAIN_TYPE):
    pass

  @abstractmethod
  def setLamp(self, BRAIN_TYPE):
    pass


class CorticalPainter(BrainPainter):
  def __init__(self, cortFiles, subcortFiles=''):
    self.cortFiles = cortFiles
    self.subcortFiles = subcortFiles

  def loadMeshes(self):
    # import cortical regions and set them to be almost transparent
    for i in range(len(self.cortFiles)):
      bpy.ops.import_mesh.ply(filepath=self.cortFiles[i])

    # import subcortical regions
    for i in range(len(self.subcortFiles)):
      bpy.ops.import_mesh.ply(filepath=self.subcortFiles[i])

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
        
  def setCamera(self, resolution, fov, ortho_scale, BRAIN_TYPE):

    scene = bpy.data.scenes["Scene"]

    self.prepareCamera(resolution, fov)

    pi = 3.14159265
    scene.camera.rotation_euler = (pi / 2, 0, -3 * pi / 2)
    # Set camera location
    scene.camera.location = (167.00, -15.1, 3.824)
    if BRAIN_TYPE == 'inflated':
      scene.camera.location = (167.00, -0.3, 3.824)

    bpy.data.cameras['Camera'].type = 'ORTHO'
    bpy.data.cameras['Camera'].ortho_scale = ortho_scale
    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self, BRAIN_TYPE):

    energyAll = 5
    distanceAll = 1000

    scene = bpy.data.scenes["Scene"]
    self.deletePrevLamps()

    lampIndices = [1, 2, 3, 4]
    lampLocs = [(136, 45, 72), (136, -105, -64), (136, -105, 72), (136, 45, -64)]
    if BRAIN_TYPE == 'inflated':
      lampIndices = [1, 2, 3, 4, 5]
      lampLocs = [(136, 160, 130), (136, -140, -64), (136, -140, 130), (136, 160, -64), (136, 0, 130)]
      energyAll = 13

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


class CorticalPainterLeft(BrainPainter):
  
  def __init__(self, cortFiles, subcortFiles=''):
    self.cortFiles = cortFiles
    self.subcortFiles = subcortFiles
    
  def loadMeshes(self):
    # import cortical regions and set them to be almost transparent
    for i in range(len(self.cortFiles)):
      bpy.ops.import_mesh.ply(filepath=self.cortFiles[i])

    for i in range(len(self.subcortFiles)):
      bpy.ops.import_mesh.ply(filepath=self.subcortFiles[i])

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

  def setCamera(self, resolution, fov, ortho_scale, BRAIN_TYPE):

    scene = bpy.data.scenes["Scene"]

    self.prepareCamera(resolution, fov)

    pi = 3.14159265
    scene.camera.rotation_euler = (pi / 2, 0, -1 * pi / 2)
    # Set camera location
    
    scene.camera.location = (-167.00, -15.1, 3.824)
    if BRAIN_TYPE == 'inflated':
      scene.camera.location = (-167.00, -0.3, 3.824)
          
    bpy.data.cameras['Camera'].type = 'ORTHO'
    bpy.data.cameras['Camera'].ortho_scale = ortho_scale
    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self, BRAIN_TYPE):
    
    energyAll = 5
    distanceAll = 1000

    scene = bpy.data.scenes["Scene"]
    self.deletePrevLamps()

    lampIndices = [1, 2, 3, 4]
    lampLocs = [(-136, 45, 72), (-136, -105, -64), (-136, -105, 72), (-136, 45, -64)]

    if BRAIN_TYPE == 'inflated':
      lampIndices = [1, 2, 3, 4, 5]
      lampLocs = [(-136, 160, 130), (-136, -140, -64), (-136, -140, 130), (-136, 160, -64), (-136, 0, 130)]
      
      energyAll = 13

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


class CorticalPainterInnerRight(CorticalPainter):
  def __init__(self, cortFiles, subcortFiles):
    self.cortFiles = cortFiles
    self.subcortFiles = subcortFiles

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

  def setCamera(self, resolution, fov, ortho_scale, BRAIN_TYPE):

    scene = bpy.data.scenes["Scene"]

    self.prepareCamera(resolution, fov)

    pi = 3.14159265
    scene.camera.rotation_euler = (pi / 2, 0, -pi / 2)
    # Set camera location
    scene.camera.location = (-71, -15.1, 3.824)
    if BRAIN_TYPE == 'inflated':
      scene.camera.location = (-71, -1.3, 3.824)

    bpy.data.cameras['Camera'].type = 'ORTHO'
    bpy.data.cameras['Camera'].ortho_scale = ortho_scale
    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self, BRAIN_TYPE):

    energyAll = 5
    distanceAll = 1000

    scene = bpy.data.scenes["Scene"]
    self.deletePrevLamps()

    lampIndices = [1, 2, 3, 4]
    # y + 20
    lampLocs = [(-80, 70, 72), (-80, -80, -64), (-80, -80, 72), (-80, 70, -64)]
    if BRAIN_TYPE == 'inflated':
      lampIndices = [1, 2, 3, 4, 5]
      lampLocs = [(-130, 150, 70), (-130, -150, -120), (-130, -150, 70), (-130, 150, -130), (-130, 0, 170), (-90, 0, -90)]
      energyAll = 11

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


class CorticalPainterInnerLeft(CorticalPainter):
  def __init__(self, cortFiles, subcortFiles):
    self.cortFiles = cortFiles
    self.subcortFiles = subcortFiles

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
    
  def setCamera(self, resolution, fov, ortho_scale, BRAIN_TYPE):

    scene = bpy.data.scenes["Scene"]

    self.prepareCamera(resolution, fov)

    pi = 3.14159265
    scene.camera.rotation_euler = (pi / 2, 0, -3 * pi / 2)
    # Set camera location
    scene.camera.location = (71, -15.1, 3.824)
    if BRAIN_TYPE == 'inflated':
      scene.camera.location = (71, -1.3, 3.824)

    bpy.data.cameras['Camera'].type = 'ORTHO'
    bpy.data.cameras['Camera'].ortho_scale = ortho_scale
    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self, BRAIN_TYPE):

    energyAll = 5
    distanceAll = 1000

    scene = bpy.data.scenes["Scene"]
    self.deletePrevLamps()

    lampIndices = [1, 2, 3, 4]
    # y + 20
    lampLocs = [(80, 70, 72), (80, -80, -64), (80, -80, 72), (80, 70, -64)]
    if BRAIN_TYPE == 'inflated':
      lampIndices = [1, 2, 3, 4, 5]
      lampLocs = [(130, 150, 70), (130, -150, -120), (130, -150, 70), (130, 150, -130), (130, 0, 170), (90, 0, -90)]
      energyAll = 11

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

  def setCamera(self, resolution, fov, ortho_scale, BRAIN_TYPE):

    scene = bpy.data.scenes["Scene"]
    self.prepareCamera(resolution, fov)

    # scene.camera.rotation_euler = (1.15, -0.02, -8.63) # subcort only
    scene.camera.rotation_euler = (1.1499, -0.01999, -8.2985)  # half-cort half subcort

    # Set camera translation
    # scene.camera.location = (-107.3, 66.8, 43.1) # subcort only
    scene.camera.location = (-177.16, 69.74, 83.1)  # half cort half subcort

    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self, BRAIN_TYPE):

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

class SubcorticalPainterLeft(BrainPainter):
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

  def setCamera(self, resolution, fov, ortho_scale, BRAIN_TYPE):

    scene = bpy.data.scenes["Scene"]
    self.prepareCamera(resolution, fov)

    # scene.camera.rotation_euler = (1.15, -0.02, -8.63) # subcort only
    # scene.camera.rotation_euler = (1.1499, -0.01999, -8.2985)  # half-cort half subcort

    # Set camera translation
    # scene.camera.location = (-107.3, 66.8, 43.1) # subcort only
    scene.camera.location = (177.16, 69.74, 83.1)  # half cort half subcort
    
    # pi = 3.14159265
    scene.camera.rotation_euler = (1.204, 0, 2.02)

    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self, BRAIN_TYPE):

    energyAll = 7
    distanceAll = 1000

    scene = bpy.data.scenes["Scene"]
    self.deletePrevLamps()

    lampIndices = [1, 2]
    lampLocs = [(82.53, 0.79, 72.87), (-88.53, -119.79, 72.87)]

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

class SubcorticalPainterTop(BrainPainter):
  def __init__(self, cortFiles, subcortFiles):
    self.cortFiles = [] # cortical files would obstruct top view of subcort meshes
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

  def setCamera(self, resolution, fov, ortho_scale, BRAIN_TYPE):

    scene = bpy.data.scenes["Scene"]
    self.prepareCamera(resolution, fov)

    # scene.camera.rotation_euler = (1.15, -0.02, -8.63) # subcort only
    # scene.camera.rotation_euler = (1.1499, -0.01999, -8.2985)  # half-cort half subcort

    # Set camera translation
    # scene.camera.location = (-107.3, 66.8, 43.1) # subcort only
    scene.camera.location = (0, -29, 200.25)  # half cort half subcort
    
    pi = 3.14159265
    scene.camera.rotation_euler = (0, 0, pi/2)

    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self, BRAIN_TYPE):

    energyAll = 7
    distanceAll = 1000

    scene = bpy.data.scenes["Scene"]
    self.deletePrevLamps()

    lampIndices = [1, 2, 3, 4]
    lampLocs = [(-45, 45, 150), (45, 45, 150), (45, -100, 150), (-45, -100, 150)]

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

class SubcorticalPainterBottom(BrainPainter):
  def __init__(self, cortFiles, subcortFiles):
    self.cortFiles = [] # cortical files would obstruct bottom view of subcort meshes
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

  def setCamera(self, resolution, fov, ortho_scale, BRAIN_TYPE):

    scene = bpy.data.scenes["Scene"]
    self.prepareCamera(resolution, fov)

    # scene.camera.rotation_euler = (1.15, -0.02, -8.63) # subcort only
    # scene.camera.rotation_euler = (1.1499, -0.01999, -8.2985)  # half-cort half subcort

    # Set camera translation
    # scene.camera.location = (-107.3, 66.8, 43.1) # subcort only

    pi = 3.14159265
    scene.camera.rotation_euler = (pi, 0, pi/2)

    # Set camera location
    scene.camera.location = (0, -33.8, -209.46)

    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self, BRAIN_TYPE):

    energyAll = 7
    distanceAll = 1000

    scene = bpy.data.scenes["Scene"]
    self.deletePrevLamps()

    lampIndices = [1, 2, 3, 4]
    lampLocs = [(-45, 45, -150), (45, 45, -150), (45, -100, -150), (-45, -100, -150)]

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



def colorRegionsAndRender(indexMap, matDf, COLOR_POINTS, OUT_FOLDER, IMG_TYPE):
  objList = bpy.context.selected_objects[::-1]  # make sure to remove the cube from the scene
  # print(objList)

  cols = matDf.columns.to_list()
  imageNames = matDf.loc[:,'Image-name-unique'].values

  imageNames = [str(n) for n in imageNames] # ensure names are strings
  imageNames = [''.join(n.split(' ')) for n in imageNames] # remove spaces in names
  matDf = matDf.loc[:,cols[1]:]

  for imgIndex in range(matDf.shape[0]):

    # for each event get the sum of all the probabilities until the current stage
    # eventsAbnormality = matDf.loc[imgIndex,:].values

    # calc abnorm for plottable biomk
    if bpy.context.selected_objects:
      for obj in bpy.context.selected_objects:
        # print(obj.name, obj, obj.type)
        regionName = obj.name

        if regionName in indexMap.keys():
          # 'Left-Caudate -> nonZlabelNr -> [z-labelNrs], between 1-3'
          targetLabel = indexMap[regionName]

          
          # need to come back and make this applicable to all subcort config after adding l/r for subcort
          if targetLabel != -1: 
            # abnormality values for each significance levels
            signifAbnorm = matDf.loc[imgIndex,targetLabel]

            # colors for each significance levels
            finalColor = getInterpColor(signifAbnorm, COLOR_POINTS)

            # print("regionName", regionName, finalColor)

            # if regionName == 'rh.pial.DK.inferiorparietal':
            #   print('targetLabel', targetLabel)
            #   print('finalColor', finalColor)
            #   print('signifAbnorm', signifAbnorm)

            # material = makeMaterial('mat_%d_%d_%s' % (matrixIndex, imgIndex, regionName), finalColor, (1,1,1), 1)
            # setMaterial(obj, material)
            # obj.material_slots[0].material = bpy.data.materials['mat_%d_%d_%s' % (matrixIndex, imgIndex, regionName)]
            try: 
              bpy.data.materials['mat_%s' % regionName].diffuse_color = finalColor
            except:
              print('error with painting region: ', regionName)

            # obj.data.materials.append(material)

        else:
          print('object not found: %s' % obj.name)

    outputFile = '%s/%s_%s.png' % (OUT_FOLDER, IMG_TYPE, imageNames[imgIndex])
    print('rendering file %s' % outputFile)
    bpy.data.scenes['Scene'].render.filepath = outputFile
    bpy.ops.render.render(write_still=True)
    sys.stdout.flush()

class CorticalPainterTop(BrainPainter):
  
  def __init__(self, cortFiles, subcortFiles):
    self.cortFiles = cortFiles
    self.subcortFiles = subcortFiles
    
  def loadMeshes(self):
    # import cortical regions and set them to be almost transparent
    for i in range(len(self.cortFiles)):
      bpy.ops.import_mesh.ply(filepath=self.cortFiles[i])

    for i in range(len(self.subcortFiles)):
      bpy.ops.import_mesh.ply(filepath=self.subcortFiles[i])

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

  def setCamera(self, resolution, fov, ortho_scale, BRAIN_TYPE):

    scene = bpy.data.scenes["Scene"]

    self.prepareCamera(resolution, fov)

    pi = 3.14159265
    scene.camera.rotation_axis_angle = (pi/2, 0, 0, 0)
    scene.camera.rotation_euler = (0, 0, pi/2)
    # scene.camera.Quaternion = (0, pi / 2, 0, -1 * pi / 2)
    # Set camera location
    scene.camera.location = (0, -10, 250)

    bpy.data.cameras['Camera'].type = 'ORTHO'
    bpy.data.cameras['Camera'].ortho_scale = ortho_scale
    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self, BRAIN_TYPE):
    
    energyAll = 5
    distanceAll = 1000

    scene = bpy.data.scenes["Scene"]
    self.deletePrevLamps()

    lampIndices = [1, 2, 3, 4]
    lampLocs = [(-45, 45, 150), (45, 45, 150), (45, -100, 150), (-45, -100, 150)]

    if BRAIN_TYPE == 'inflated':
      #! note: top does not work well for inflated type data
      lampIndices = [1, 2, 3, 4, 5]
      lampLocs = [(-45, 45, 150), (45, 45, 150), (45, -100, 150), (-45, -100, 150), (-45, -100, 200)]
      energyAll = 13

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
      
class CorticalPainterBottom(BrainPainter):
  
  def __init__(self, cortFiles, subcortFiles):
    self.cortFiles = cortFiles
    self.subcortFiles = subcortFiles
    
  def loadMeshes(self):
    # import cortical regions and set them to be almost transparent
    for i in range(len(self.cortFiles)):
      bpy.ops.import_mesh.ply(filepath=self.cortFiles[i])

    for i in range(len(self.subcortFiles)):
      bpy.ops.import_mesh.ply(filepath=self.subcortFiles[i])

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

  def setCamera(self, resolution, fov, ortho_scale, BRAIN_TYPE):

    scene = bpy.data.scenes["Scene"]

    self.prepareCamera(resolution, fov)

    pi = 3.14159265
    scene.camera.rotation_axis_angle = (pi/2, 0, 0, 0)
    scene.camera.rotation_euler = (pi, 0, pi/2)
    # scene.camera.Quaternion = (0, pi / 2, 0, -1 * pi / 2)
    # Set camera location
    scene.camera.location = (0, -10, -250)

    bpy.data.cameras['Camera'].type = 'ORTHO'
    bpy.data.cameras['Camera'].ortho_scale = ortho_scale
    bpy.data.cameras['Camera'].clip_end = 1000

  def setLamp(self, BRAIN_TYPE):
    
    energyAll = 5
    distanceAll = 1000

    scene = bpy.data.scenes["Scene"]
    self.deletePrevLamps()

    lampIndices = [1, 2, 3, 4]
    lampLocs = [(-45, 45, -150), (45, 45, -150), (45, -100, -150), (-45, -100, -150)]

    if BRAIN_TYPE == 'inflated':
      #! note: top does not work well for inflated type data
      lampIndices = [1, 2, 3, 4, 5]
      lampLocs = [(-45, 45, -150), (45, 45, -150), (45, -100, -150), (-45, -100, -150), (-45, -100, -200)]
      energyAll = 13

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


def genLaTex(inputFile, outputFolder, COLORS_RGB): # PARAMS: input folder, output folder, user color input
  
  tex = r'''
\documentclass[11pt,a4paper]{report}
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
%\documentclass[border=2pt,tikz]{standalone}
\usetikzlibrary{positioning}

\newcommand{\scl}{0.06}

\begin{document}'''
  INPUT_FILE = inputFile
  matDf = pd.read_csv(INPUT_FILE) # reading in image names from input
  directory = "."
  extension = ".png"
  output_folder = os.listdir(outputFolder) 
  # filtering output folder for png's
  img_files = [file for file in output_folder if file.lower().endswith(extension)] 
  img_path_groups = [] # grouping images together
  imageNames = matDf.loc[:,'Image-name-unique'].values # getting image name values
  imageNames = [''.join(n.split(' ')) for n in imageNames] # remove spaces in names

  for i in imageNames:
    # grouping the images by csv name
    latex_group = [file for file in output_folder if file.endswith(i + extension)] 
    img_path_groups.append(latex_group)

  for img_path in range(len(img_path_groups)):
    # adding parent tikzpictures
    tex+= r'''\tikzset{block/.style={node distance=-1pt, line width=1pt}}
\begin{tikzpicture}
\centering
'''
    for img in range(len(img_path_groups[img_path])): 
      # adding image nodes
      if(img==0): # positioning for first image
        position = r''' \node[block] (0) {\includegraphics[scale=\scl]{./''' 
      else: 
        position = r''' \node[block, below=of ''' + str(img-1) + r'''] (''' + str(img) + r''') {\includegraphics[scale=\scl]{./'''
      tex+= position + img_path_groups[img_path][img] + r'''}};
      ''' 

    tex+= r'''
    \node[block,above=of 0] {'''+ imageNames[img_path].replace('_', ' ') + r'''};
    \end{tikzpicture}'''
  # add colorbar
  tex+= r'''\begin{tikzpicture}[scale=0.9,auto,swap]'''
  
  for c in range(len(COLORS_RGB)): # defining colors based on user input in config
    tex+= r'''
    \definecolor{color_''' + str(c) + r'''}{rgb}{''' + str(COLORS_RGB[c]).replace('(', '').replace(')', '') + r'''}'''
  
  for c in range(len(COLORS_RGB)-1): # adding the color bar shading
    tex+= r'''
    \shade[bottom color=color_''' + str(c) + r''',top color=color_''' + str(c+1) + r'''] (0,''' + str(c*2) + r''') rectangle (0.5,''' + str((c * 2) + 2.01) + r''');
    '''
    
  for c in range(len(COLORS_RGB)): # drawing and labeling the lines on colorbar
    if(c==0): # name 0-sigma normal
      tex+= r''' 
    \draw (0,0) -- (0.5,0);\node[inner sep=0] (corr_text) at (1.6,0.0) {normal};
      '''
    else: # for 1-n sigmas
      tex+= r''' 
    \draw (0,''' + str(c*2) + r''') -- (0.5,''' + str(c*2) + r''');\node[inner sep=0] (corr_text) at (1.6,''' + str(c*2.0) + r''') {''' + str(c) + r'''-sigma};
      '''
  
  tex+= r'''

  \end{tikzpicture}
  \end{document}'''
  
  return tex 
