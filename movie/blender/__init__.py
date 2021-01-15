#!/usr/bin/python3

import collections.abc
import os

import numpy as np

import bpy



colorDict = {
  "anthrazit"  : ( 62/255,  68/255,  76/255),
  "mittelblau" : (  0/255,  81/255, 158/255),
  "hellblau"   : (  0/255, 190/255, 255/255),
  "C0"         : (  0.000,   0.447,   0.741),
  "C1"         : (  0.850,   0.325,   0.098),
  "C2"         : (  0.749,   0.561,   0.102),
  "C3"         : (  0.494,   0.184,   0.556),
  "C4"         : (  0.466,   0.674,   0.188),
  "C5"         : (  0.301,   0.745,   0.933),
  "C6"         : (  0.635,   0.078,   0.184),
  "C7"         : (  0.887,   0.465,   0.758),
  "C8"         : (  0.496,   0.496,   0.496),
  "black"      : (  0.000,   0.000,   0.000),
  "white"      : (  1.000,   1.000,   1.000),
}



def rad(*deg):
  return [x / 180 * np.pi for x in deg]

def getColor(color):
  if isinstance(color, str): color = colorDict[color]
  return color

def getParentPath():
  return os.path.realpath(
      os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

def getInPath(name=""):
  return os.path.join(getParentPath(), "in",  name)

def getTmpPath(name=""):
  return os.path.join(getParentPath(), "tmp", name)

def getOutPath(name=""):
  return os.path.join(getParentPath(), "out", name)

usedTmpFiles = []

def useTmpFile(name):
  if not os.path.isdir(getTmpPath()): os.mkdir(getTmpPath())
  path = getTmpPath(name)
  exists = os.path.isfile(path)
  usedTmpFiles.append(path)
  return path, exists

def deleteUnusedTmpFiles():
  for name in os.listdir(getTmpPath()):
    path = getTmpPath(name)
    if os.path.isfile(path) and (path not in usedTmpFiles):
      print("Removing unused temp. file {}...".format(path))
      os.remove(path)

def getNewObject():
  obj = bpy.context.object
  mat = bpy.data.materials.new(name="Material")
  obj.data.materials.append(mat)
  return obj

def addParent(loc, objs):
  parentObj = bpy.data.objects.new("empty", None)
  bpy.context.scene.objects.link(parentObj)
  parentObj.location = loc
  for obj in objs: obj.parent = parentObj
  return parentObj

def select(objs, active=None):
  if not isinstance(objs, collections.abc.Iterable): objs = [objs]
  for obj in bpy.data.objects: obj.select = False
  for obj in objs: obj.select = True
  #for obj in bpy.data.objects: obj.select_set(state=True)
  if active is not None: bpy.context.scene.objects.active = active



from blender.animation import *
from blender.plot import *
