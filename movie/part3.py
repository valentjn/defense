#!/usr/bin/python3

import numpy as np

import blender

import bpy



def addModelBiomech(loc, scale, rot):
  blendPath = blender.getInPath("biomechModel.blend")
  
  with bpy.data.libraries.load(blendPath) as (dataFrom, dataTo):
    dataTo.objects = [
        name for name in dataFrom.objects
        if (len(name) == 3) and (len(name.strip("0123456789")) == 0)]
  
  objs = []
  
  for child in dataTo.objects:
    if child is not None:
      objs.append(child)
      bpy.context.scene.objects.link(child)
  
  obj = blender.addParent(loc, objs)
  obj.scale = 3*[scale]
  obj.rotation_euler = rot
  return obj

def addModelTopoOpt(loc, scale, rot, id_):
  plyPath = blender.getInPath("topoOptStructure{}.ply".format(id_))
  bpy.ops.import_mesh.ply(filepath=plyPath)
  obj = blender.getNewObject()
  bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
  obj.scale = 3*[scale]
  obj.rotation_euler = rot
  obj.location = loc
  obj.active_material.diffuse_color = blender.getColor("mittelblau")
  return obj



def animate(ani):
  rad = blender.rad
  rotBiomech, rotTopoOpt = rad(0, 0, -90), rad(180, 0, 180)
  objBiomech = addModelBiomech(
      (1, 11, -0.7), 0.8, rotBiomech)
  objTopoOpt = addModelTopoOpt(
      (-1.4, 11, 1.1), 2, rotTopoOpt, 660)
  objPolygon = blender.addPolygonHUD((0, 0, 11), [
    (0.1,  3.3, 0),
    (0.1, -0.2, 0),
    (1.8, -1.3, 0),
    (1.8, -3.3, 0),
    (5.5, -3.3, 0),
    (5.5,  3.3, 0),
  ])
  objsTexts = [
    blender.addLaTeXHUD((0.3, 2.65, 11),
r"\textbf{Results in applications:}", scale=0.9),
    blender.addLaTeXHUD((0.3, 2.15, 11), r"""
\begin{itemize}
  \item
  \emph{Topology optimization:}
  Cho\-lesky factor interpolation pre\-serves positive definiteness
  and derivatives of elasticity tensors
\end{itemize}""", scale=0.9, textWidth="56mm"),
    blender.addLaTeXHUD((0.3, 0.6, 11), r"""
\begin{itemize}
  \item
  \emph{Financial application:}
  Solve dynamic portfolio choice problems with 5 states and 11\\
  \hspace{6mm}policies in high precision
\end{itemize}""", scale=0.9, textWidth="56mm"),
    blender.addLaTeXHUD((1.9, -0.95, 11), r"""
\begin{itemize}
  \item
  \emph{Biomechanical application:}
  Reduce computational time by up to 99\,\% with surrogates
\end{itemize}""", scale=0.9, textWidth="40mm"),
#    blender.addLaTeXHUD((0, 1.15, 11), r"""
#\begin{itemize}
#  \item
#  Other applications: Fuzzy extension principle, explicit test problems
#\end{itemize}""", scale=0.9, textWidth="40mm"),
  ]
  
  for obj in [objBiomech, objTopoOpt, objPolygon] + objsTexts:
    ani.fadeOut(obj, 0)
  
  rotBiomech[2] += 3*(2*np.pi)
  rotTopoOpt[2] += 3*(2*np.pi)
  ani.rotate(objBiomech, 40, rotBiomech, intp="LINEAR")
  ani.rotate(objTopoOpt, 40, rotTopoOpt, intp="LINEAR")
  
  for obj in [objBiomech, objTopoOpt, objPolygon] + objsTexts:
    ani.fadeIn(obj, 1)
  ani.wait(1)
  ani.wait(23)
  
  for obj in [objBiomech, objTopoOpt, objPolygon] + objsTexts:
    ani.fadeOut(obj, 1)
