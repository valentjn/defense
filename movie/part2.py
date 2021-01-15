#!/usr/bin/python3

import numpy as np

import blender
import helper.grid



def addSparseGrid(loc, size, n, d, b):
  loc = np.array(loc)
  ms = 0.07
  
  grid = (helper.grid.RegularSparseBoundary(n, d, b) if b >= 0 else
          helper.grid.RegularSparse(n, d))
  X, L, I = grid.generate()
  obj = blender.addPlotPoints(loc, ms, size * (np.array(X) - 0.5))
  
  return obj, X, L, I



def animate(ani):
  rad = blender.rad
  n, d, b = 4, 3, 1
  s = 2
  
  objRectangle = blender.addRectangleHUD((-5.55, 3.3, 11), [5.5, 4.75])
  objsText = [
    blender.addLaTeXHUD((-4.8, 2.65, 11),
r"\textbf{Results in theory/algorithms:}", scale=0.9),
    blender.addLaTeXHUD((-4.8, 2.15, 11), r"""
\begin{itemize}
  \item
  \emph{Boundary conditions:}
  Hierar-\\chical not-a-knot B-splines
\end{itemize}""", scale=0.9, textWidth="55mm"),
    blender.addLaTeXHUD((-4.8, 1.35, 11), r"""
\begin{itemize}
  \item
  \emph{Sparse grid algorithms:}
  Hierarchization as example
\end{itemize}""", scale=0.9, textWidth="55mm"),
    blender.addLaTeXHUD((-4.8, 0.55, 11), r"""
\begin{itemize}
  \item
  \emph{Dim. adaptive SGs:}
  Combi-\\nation technique,
  method of residual interpolation
\end{itemize}""", scale=0.9, textWidth="55mm"),
    blender.addLaTeXHUD((-4.8, -0.6, 11), r"""
\begin{itemize}
  \item
  \emph{Spat. adaptive SGs:}
  BFS, (weakly) fundamental splines
\end{itemize}""", scale=0.9, textWidth="55mm"),
  ]
  loc = (-s/2, -s/2, -s/2)
  objsAxis = [
    [
      blender.addPlotLine(loc, [0, s], 0, 0, lw=0.04),
      blender.addPlotLine(loc, [0, s], s, 0, lw=0.04),
      blender.addPlotLine(loc, 0, [0, s], 0, lw=0.04),
      blender.addPlotLine(loc, s, [0, s], 0, lw=0.04),
      blender.addPlotLine(loc, [0, s], 0, s, lw=0.04),
      blender.addPlotLine(loc, [0, s], s, s, lw=0.04),
      blender.addPlotLine(loc, 0, [0, s], s, lw=0.04),
      blender.addPlotLine(loc, s, [0, s], s, lw=0.04),
      blender.addPlotLine(loc, 0, 0, [0, s], lw=0.04),
      blender.addPlotLine(loc, 0, s, [0, s], lw=0.04),
      blender.addPlotLine(loc, s, 0, [0, s], lw=0.04),
      blender.addPlotLine(loc, s, s, [0, s], lw=0.04),
    ] for q in range(2)
  ]
  #for q in range(2):
  #  for obj in objsAxis[q]: obj.active_material.diffuse_intensity = 0.3
  objSG, X, L, I = addSparseGrid((0, 0, 0), s, n, d, b)
  objSGPar = blender.addParent(
      (0, 0, 0), objsAxis[0] + objsAxis[1] + [objSG])
  objSGParPar = blender.addParent((0.3, 11, 0.5), [objSGPar])
  objPoints = objSG.children
  locPoints = [list(obj.location) for obj in objPoints]
  xx = np.linspace(0, 1, 5)
  dist = s*0.4
  
  for obj in objsAxis[0]: ani.fadeOut(obj, 0)
  for obj in objsAxis[1]: ani.cutCurve(obj, 0, 0, 0)
  for obj in objPoints: ani.changeColor(obj, 0, blender.getColor("C0"))
  for obj in [objRectangle, objSG] + objsText: ani.fadeOut(obj, 0)
  ani.rotate(objSGParPar, 0, rad(25, 11.5, -39))
  
  for obj in [objRectangle] + objsText: ani.fadeIn(obj, 1)
  
  for t in [2, 0, 1]:
    if t == 1:
      xxCur = xx[::-1]
      factor = 1
    else:
      xxCur = xx
      factor = -1
    
    if t != 2:
      for obj in [objSG] + objsAxis[0]:
        loc = list(obj.location)
        loc[t] -= factor * dist
        ani.move(obj, 1, loc)
      ani.wait(1)
    
    if t == 0:
      R1, R2, R3 = [0, 1, 4, 5], [2, 6, 8, 9], [3, 7, 10, 11]
    elif t == 1:
      R1, R2, R3 = [2, 3, 6, 7], [0, 4, 8, 10], [1, 5, 9, 11]
    
    for x in xxCur:
      sec = 0.5
      
      if t != 2:
        if x == 0:
          for obj in [objsAxis[0][r] for r in R2]:
            loc = list(obj.location)
            loc[t] += factor * dist
            ani.move(obj, sec, loc)
        elif x == 1:
          for obj in [objsAxis[0][r] for r in R3]:
            loc = list(obj.location)
            loc[t] += factor * dist
            ani.move(obj, sec, loc)
        for obj in [objsAxis[1][r] for r in R1]:
          if factor == -1: ani.cutCurve(obj, sec, 0, x)
          else:            ani.cutCurve(obj, sec, x, 1)
        for obj in [objsAxis[0][r] for r in R1]:
          if factor == -1: ani.cutCurve(obj, sec, x+0.25, 1)
          else:            ani.cutCurve(obj, sec, 0, x-0.25)
      
      K = np.where(X[:,t] == x)[0]
      for k in K:
        if t == 2: ani.fadeIn(objPoints[k], sec)
        locPoints[k][t] += factor * dist
        ani.move(objPoints[k], sec, locPoints[k])
        ani.changeColor(objPoints[k], sec/2, blender.getColor("C1"))
        ani.changeColor(objPoints[k], sec/2, blender.getColor("C0"),
                        wait=sec/2)
      ani.wait(sec)
      if (t == 2) and (x == 0): ani.wait(3)
    
    if t == 2:
      for obj in objsAxis[0] + objsAxis[1]:
        loc = list(obj.location)
        loc[t] += factor * dist
        ani.move(obj, 0, loc)
        ani.fadeIn(obj, 1)
      ani.wait(1)
    else:
      for r in R1:
        objsAxis[0][r], objsAxis[1][r] = objsAxis[1][r], objsAxis[0][r]
    
    if t == 1: ani.rotate(objSGPar, 20, rad(0, 0, 360), wait=1, intp="SINE")
    
    ani.wait(2)
  
  ani.wait(5)
  
  for obj in objsAxis[0] + objsText + [objRectangle, objSG]:
    ani.fadeOut(obj, 1)
