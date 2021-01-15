#!/usr/bin/python3

import numpy as np

from blender import *

import bpy



class Animation(object):
  def __init__(self, fps):
    self.fps = fps
    self.time = 0
    self.scene = bpy.context.scene
    self.scene.render.fps = self.fps
    self.debugMode = False
  
  def frame(self, time=None):
    if time is None: time = self.time
    return int(round(time * self.fps))
  
  def finish(self):
    self.scene.frame_end = self.frame()
  
  def wait(self, duration):
    self.time += duration
  
  def move(self, obj, duration, loc, **kwargs):
    self.animate(obj, duration, "location", loc, **kwargs)
  
  def scale(self, obj, duration, scale, **kwargs):
    self.animate(obj, duration, "scale", scale, **kwargs)
  
  def rotate(self, obj, duration, rot, **kwargs):
    self.animate(obj, duration, "rotation_euler", rot, **kwargs)
  
  def fade(self, obj, duration, alpha, **kwargs):
    self.animate(obj, duration, "alpha", alpha, **kwargs)
    self.animate(obj, duration, "specular_alpha", alpha, **kwargs)
  
  def fadeOut(self, obj, duration, **kwargs):
    self.fade(obj, duration, 0.0, **kwargs)
  
  def fadeIn(self, obj, duration, **kwargs):
    self.fade(obj, duration, 1.0, **kwargs)
  
  def setAlpha(self, obj, alpha, **kwargs):
    self.fade(obj, 0.0, alpha, intp="CONSTANT", **kwargs)
  
  #def morphMesh(self, objFrom, objTo, duration, **kwargs):
  #  select([objFrom, objTo], active=objFrom)
  #  bpy.ops.object.join_shapes()
  #  shapeKey = objFrom.data.shape_keys
  #  key = "key_blocks[\"{}\"].value".format(objTo.name)
  #  self.animate(shapeKey, 0, key, 0, **kwargs)
  #  self.animate(shapeKey, duration, key, 1, **kwargs)
  #  self.setAlpha(objFrom, 1)
  #  self.setAlpha(objTo, 0)
  #  self.setAlpha(objFrom, 0, wait=duration)
  #  self.setAlpha(objTo, 1, wait=duration)
  
  def morph(self, obj, duration, state, **kwargs):
    self.animate(obj.data.shape_keys, duration, "eval_time", state*10,
                 **kwargs)
  
  def cutCurve(self, obj, duration, start, end, **kwargs):
    self.animate(obj.data, duration, "bevel_factor_start", start, **kwargs)
    self.animate(obj.data, duration, "bevel_factor_end",   end,   **kwargs)
  
  def changeColor(self, obj, duration, color, **kwargs):
    self.animate(obj, duration, "diffuse_color", color, **kwargs)
  
  def insertKeyframe(self, obj, key, frame):
    obj.keyframe_insert(data_path=key, frame=frame)
    if self.debugMode:
      print("{}: frame = {}, value = {}".format(
          obj.name, frame, eval("obj.{}".format(key))))
  
  def animate(self, obj, duration, key, value, wait=0.0,
              intp="BEZIER", easing="AUTO"):
    if key in ["alpha", "diffuse_color", "specular_alpha"]:
      if not hasattr(obj, key):
        if obj.active_material is not None:
          obj = obj.active_material
        else:
          for child in obj.children:
            self.animate(child, duration, key, value, intp=intp, wait=wait)
          return
      if key in ["alpha", "specular_alpha"]: obj.use_transparency = True
    elif (key == "scale") and (np.ndim(value) == 0):
      value = 3 * [value]
    
    frameStart = self.frame(self.time + wait)
    frameEnd = self.frame(self.time + wait + duration)
    
    if duration > 0:
      self.insertKeyframe(obj, key, frameStart)
    
    exec("obj.{} = value".format(key))
    self.insertKeyframe(obj, key, frameEnd)
    
    i = (-2 if duration > 0 else -1)
    for fCurve in obj.animation_data.action.fcurves:
      if fCurve.data_path == key:
        fCurve.keyframe_points[i].interpolation = intp
        fCurve.keyframe_points[i].easing        = easing
