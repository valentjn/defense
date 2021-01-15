#!/usr/bin/python3

import hashlib
import os
import shutil
import subprocess
import tempfile

import matplotlib as mpl
import matplotlib.cm
import numpy as np

from blender import *

import bmesh
import bpy



def addSphere(loc, size, accuracy=8):
  bpy.ops.mesh.primitive_uv_sphere_add(
      segments=2*accuracy, ring_count=accuracy, location=loc, size=size)
  return getNewObject()

def addCylinder(loc, size, rot):
  bpy.ops.mesh.primitive_cylinder_add(
      vertices=256, location=loc, radius=size[0], depth=size[1], rotation=rot)
  return getNewObject()

def addCircle(loc, size, rot):
  bpy.ops.curve.primitive_nurbs_circle_add(
      location=loc, radius=size, rotation=rot)
  return getNewObject()

def addGrid(loc, size, rot, nn):
  bpy.ops.mesh.primitive_grid_add(
      location=loc, radius=size, rotation=rot,
      x_subdivisions=nn[0], y_subdivisions=nn[1])
  return getNewObject()



def normalizePoints(*args):
  return [np.array(xx) for xx in np.broadcast_arrays(*args)]

def loadImageTexture(obj, path):
  image = bpy.data.images.load(path)
  texture = bpy.data.textures.new("Texture", type="IMAGE")
  texture.image = image
  texture.filter_type = "BOX"
  slot = obj.active_material.texture_slots.add()
  slot.texture = texture
  slot.texture_coords = "ORCO"
  return slot

def addPlotLine(loc, xx, yy, zz, lw=0.05, addAsShapeKeyTo=None):
  xx, yy, zz = normalizePoints(xx, yy, zz)
  scene = bpy.context.scene
  
  curve = bpy.data.curves.new("Curve", "CURVE")
  obj = bpy.data.objects.new("Curve Object", curve)
  scene.objects.link(obj)
  scene.objects.active = obj
  curve.dimensions = "3D"
  
  spline = curve.splines.new("POLY")
  spline.points.add(len(xx) - 1)
  
  for point, x, y, z in zip(spline.points, xx, yy, zz):
    point.co = (loc[0]+x, loc[1]+y, loc[2]+z, 1)
  
  circle = addCircle(loc, lw, rad(0, 0, 0))
  obj.data.bevel_object = circle
  obj.data.use_fill_caps = True
  
  mat = bpy.data.materials.new(name="Material")
  obj.data.materials.append(mat)
  
  shapeKey = obj.shape_key_add("Shape Key")
  obj.data.shape_keys.use_relative = False
  
  #mesh = objCurve.to_mesh(scene, False, "PREVIEW")
  #obj = bpy.data.objects.new("Mesh Object", mesh)
  #scene.objects.link(obj)
  #obj.matrix_world = objCurve.matrix_world
  #mat = bpy.data.materials.new(name="Material")
  #obj.data.materials.append(mat)
  #scene.objects.unlink(objCurve)
  #scene.objects.unlink(circle)
  #return obj
  
  return obj

def addPlotLineAsShapeKey(loc, xx, yy, zz, obj):
  xx, yy, zz = normalizePoints(xx, yy, zz)
  shapeKey = obj.shape_key_add("Shape Key")
  
  for point, x, y, z in zip(shapeKey.data, xx, yy, zz):
    point.co = (loc[0]+x, loc[1]+y, loc[2]+z)
  
  return obj

def addPlotSurface(loc, XX, YY, ZZ):
  XX, YY, ZZ = normalizePoints(XX, YY, ZZ)
  nn = XX.shape[::-1]
  obj = addGrid(loc, 1, rad(0, 0, 0), nn)
  
  for j in range(nn[0]):
    for i in range(nn[1]):
      obj.data.vertices[i+j*nn[0]].co = (XX[i,j], YY[i,j], ZZ[i,j])
  
  slot = loadImageTexture(obj, getInPath("colorbar.png"))
  slot.mapping_x = "NONE"
  slot.mapping_y = "Z"
  slot.mapping_z = "NONE"
  obj.active_material.specular_intensity = 0.1
  
  shapeKey = obj.shape_key_add("Shape Key")
  obj.data.shape_keys.use_relative = False
  
  return obj

def addPlotSurfaceAsShapeKey(loc, XX, YY, ZZ, obj):
  XX, YY, ZZ = normalizePoints(XX, YY, ZZ)
  nn = XX.shape[::-1]
  shapeKey = obj.shape_key_add("Shape Key")
  
  for j in range(nn[0]):
    for i in range(nn[1]):
      shapeKey.data[i+j*nn[0]].co = (XX[i,j], YY[i,j], ZZ[i,j])
  
  return obj

def addPlotPoints(loc, ms, X):
  X = np.array(X)
  if X.shape[1] == 2: X = np.append(X, np.zeros((X.shape[0],)), axis=1)
  objs = [addSphere(x, ms) for x in X]
  return addParent(loc, objs)

def addLogo(loc, n=2):
  r = 1
  size, rot = (1, 0.2), rad(90, 0, 0)
  objs = []
  pngNames = {
    (0, 0) : "circleBSpline.png",
    (1, 0) : "circleTopoOpt.png",
    (1, 1) : "circleBiomech.png",
    (1, 2) : "circleAlgorithm.png",
    (1, 3) : "circleSparseGrid.png",
    (1, 4) : "circleProof.png",
    (1, 5) : "circleFinance.png",
  }
  
  for i in range(n):
    phi = np.linspace(0, 2*np.pi, 7)
    corners = i*2*r * np.array([np.cos(phi), 7*[0], np.sin(phi)]).T
    for j in np.linspace(0, 6, max(6*i+1,2))[:-1]:
      k, t = int(j), j % 1
      obj = addCylinder((1-t)*corners[k] + t*corners[k+1], size, rot)
      objs.append(obj)
      obj.active_material.diffuse_color = getColor("mittelblau")
      if i <= 1: loadImageTexture(obj, getInPath(pngNames[(i, j)]))
  
  return addParent(loc, objs)

def roundCorners(obj, radius, corners=None):
  if corners is False: return
  
  if corners is not None:
    corners = [
      {"nw" : 2, "ne" : 3, "sw" : 0, "se" : 1}.get(x, x)
      for x in corners
    ]
    vertexGroup = obj.vertex_groups.new(name="Vertex Group")
    vertexGroup.add(corners, 1, "ADD")
  
  modifier = obj.modifiers.new("Bevel", "BEVEL")
  modifier.width = radius
  modifier.segments = 128
  modifier.use_only_vertices = True
  
  if corners is not None:
    modifier.limit_method = "VGROUP"
    modifier.vertex_group = vertexGroup.name
  
  #bpy.ops.object.modifier_apply(apply_as="DATA", modifier=modifier.name)

def addRectangleHUD(loc, size, roundedCorners=None, rcRadius=0.1,
                    color="hellblau"):
  bpy.ops.mesh.primitive_plane_add(location=loc)
  obj = bpy.context.object
  
  camera = bpy.context.scene.camera
  obj.scale = (size[0]/2, size[1]/2, 0)
  bpy.ops.object.transform_apply(scale=True)
  obj.location = (loc[0]+size[0]/2, loc[1]-size[1]/2, -loc[2]-0.01)
  obj.parent = camera
  constraint = obj.constraints.new("COPY_ROTATION")
  constraint.target = camera
  
  mat = bpy.data.materials.new(name="Material")
  mat.diffuse_color = getColor(color)
  mat.use_shadeless = True
  obj.data.materials.append(mat)
  
  roundCorners(obj, rcRadius, corners=roundedCorners)
  return obj

def addCircleHUD(loc, size, color="hellblau"):
  return addRectangleHUD(loc, [size, size], rcRadius=size, color=color)

def addPolygonHUD(loc, vertices, roundedCorners=None, rcRadius=0.1,
                  color="hellblau"):
  n = len(vertices)
  mesh = bpy.data.meshes.new("Mesh")
  bMesh = bmesh.new()
  vertices = [bMesh.verts.new(vertex) for vertex in vertices]
  edges    = [bMesh.edges.new([vertices[i], vertices[(i+1)%n]])
              for i in range(n)]
  face     = bMesh.faces.new(vertices)
  bMesh.to_mesh(mesh)
  bMesh.free()
  
  obj = bpy.data.objects.new("Polygon", mesh)
  bpy.context.scene.objects.link(obj)
  
  camera = bpy.context.scene.camera
  obj.location = (loc[0], loc[1], -loc[2]-0.01)
  obj.parent = camera
  constraint = obj.constraints.new("COPY_ROTATION")
  constraint.target = camera
  
  mat = bpy.data.materials.new(name="Material")
  mat.diffuse_color = getColor(color)
  mat.use_shadeless = True
  obj.data.materials.append(mat)
  
  roundCorners(obj, rcRadius, corners=roundedCorners)
  return obj

def addLaTeX(loc, rot, text, scale=1.0, textWidth=r"\textwidth",
             color="black", contourColor=None):
  tex = r"""
\documentclass{article}

% language and encodings
\usepackage[ngerman,american]{babel}

% amsmath with improvements
\usepackage{mathtools}

% need T1 font encoding for Charter,
% otherwise there will be "undefined font shape" warnings
\usepackage[T1]{fontenc}

% use Bitstream Charter as main font
\usepackage[bitstream-charter]{mathdesign}

% colors
\usepackage{xcolor}

% contours
\usepackage{contour}

% use display style by default (undo with \textstyle)
\everymath{\displaystyle}

% automatically replace "l" with \ell in math mode
\makeatletter
\mathcode`l="8000
\begingroup
\lccode`\~=`\l
\DeclareMathSymbol{\lsb@l}{\mathalpha}{letters}{`l}
\lowercase{\gdef~{\ifnum\the\mathgroup=\m@ne \ell \else \lsb@l \fi}}%
\endgroup
\makeatother

% define line colors (mix between MATLAB and matplotlib colors)
\definecolor{C0}{rgb}{0.000,0.447,0.741}
\definecolor{C1}{rgb}{0.850,0.325,0.098}
\definecolor{C2}{rgb}{0.749,0.561,0.102}
\definecolor{C3}{rgb}{0.494,0.184,0.556}
\definecolor{C4}{rgb}{0.466,0.674,0.188}
\definecolor{C5}{rgb}{0.301,0.745,0.933}
\definecolor{C6}{rgb}{0.635,0.078,0.184}
\definecolor{C7}{rgb}{0.887,0.465,0.758}
\definecolor{C8}{rgb}{0.496,0.496,0.496}

% define university CD colors
\definecolor{anthrazit}{RGB}{62,68,76}
\definecolor{mittelblau}{RGB}{0,81,158}
\definecolor{hellblau}{RGB}{0,190,255}

% omit page number
\pagestyle{empty}

\begin{document}
  \begin{minipage}{""" + textWidth + r"""}
    % don't justify text, set hyphenation penalty to zero
    \raggedright
    \hyphenpenalty=0
""" + ((r"\contour{" + contourColor + r"}{" + text + r"}")
       if contourColor is not None else text) + r"""
  \end{minipage}%
\end{document}
"""
  
  texHash = hashlib.sha512(tex.encode()).hexdigest()
  tmpName = "latex-{}.svg".format(texHash[:8])
  tmpPath, tmpExists = useTmpFile(tmpName)
  
  if not tmpExists:
    with tempfile.TemporaryDirectory() as dir_:
      texPath = os.path.join(dir_, "temp.tex")
      with open(texPath, "w") as f: f.write(tex)
      subprocess.run(["lualatex", "temp.tex"], check=True, cwd=dir_)
      
      pdfPath = os.path.join(dir_, "temp.pdf")
      svgPath = os.path.join(dir_, "temp.svg")
      subprocess.run(["pdftocairo", "-svg", pdfPath, svgPath], check=True)
      subprocess.run(
          ["inkscape", "--without-gui", "-f", svgPath, "-D", "-l", svgPath],
          check=True)
      shutil.copy(svgPath, tmpPath)
  
  objs = bpy.data.objects[:]
  bpy.ops.import_curve.svg(filepath=tmpPath)
  objs = [obj for obj in bpy.data.objects if obj not in objs]
  
  for i, child in enumerate(objs):
    mat = bpy.data.materials.new(name="Material")
    if contourColor is None:
      curColor = color
    else:
      numberOfCopies = 16
      if i < numberOfCopies * len(objs) / (numberOfCopies + 1):
        curColor = contourColor
        child.location = (*child.location[:2], child.location[2] - 1e-6)
      else:
        curColor = color
    mat.diffuse_color = getColor(curColor)
    child.data.materials[0] = mat
  
  obj = addParent(loc, objs)
  obj.scale = 3*[scale*100]
  obj.rotation_euler = rot
  return obj

def addLaTeXHUD(loc, text, **kwargs):
  obj = addLaTeX(loc, rad(0, 0, 0), text, **kwargs)
  
  camera = bpy.context.scene.camera
  #direction = -camera.matrix_world.to_3x3().transposed()[2].normalized()
  #loc = (distance * direction)[:]
  obj.location = (loc[0], loc[1], -loc[2])
  obj.parent = camera
  constraint = obj.constraints.new("COPY_ROTATION")
  constraint.target = camera
  
  for child in obj.children:
    mat = child.active_material
    mat.use_shadeless = True
  
  return obj
