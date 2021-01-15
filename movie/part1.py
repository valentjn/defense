#!/usr/bin/python3

import numpy as np

import helper.basis
import blender



def addHierarchicalBasis():
  size = (2, 1)
  margin = 0.3
  n = 3
  xx = np.linspace(0, 1, 100)
  
  objsAxis = []
  objsBasis = []
  
  for l in range(n+1):
    loc = (0, 0, (n-l)*(size[1]+margin))
    objsAxis.append(blender.addPlotLine(loc, [0, size[0]], 0, 0))
    objsAxis.append(blender.addPlotLine(loc, 0, 0, [0, size[1]]))
    
    for i in helper.grid.getHierarchicalIndices(l):
      for p in [1, 3, 5]:
        basis = helper.basis.HierarchicalBSpline(p)
        yy = basis.evaluate(l, i, xx) / basis.evaluate(1, 1, 0.5)
        if p == 1:
          obj = blender.addPlotLine(loc, size[0]*xx, 0, size[1]*yy)
          color = "C{}".format(2**(n-l)*i)
          obj.active_material.diffuse_color = blender.getColor(color)
          objsBasis.append(obj)
        else:
          blender.addPlotLineAsShapeKey(
              loc, size[0]*xx, 0, size[1]*yy, objsBasis[-1])
  
  #for obj in objsAxis: obj.active_material.diffuse_intensity = 0.3
  
  objAxis  = blender.addParent((0, 0, 0), objsAxis)
  objBasis = blender.addParent((0, 0, 0), objsBasis)
  return objAxis, objBasis



def addInterpolant():
  loc = (0, 0, 0)
  size = (3, 3, 1.5)
  gridType = "regularSparse"
  XX, YY, XXYY = helper.grid.generateMeshGrid((129, 129))
  
  objsAxes = [
      blender.addPlotLine(loc, [0, size[0]], 0, 0),
      blender.addPlotLine(loc, 0, [0, size[1]], 0),
      blender.addPlotLine(loc, 0, 0, [0, size[2]]),
  ]
  
  for p in [1, 3, 5]:
    ftEvaluate = getInterpolant(gridType, p)
    ZZ = np.reshape(ftEvaluate(XXYY), XX.shape)
    
    if p == 1:
      objInterpolant = blender.addPlotSurface(
          loc, size[0]*XX, size[1]*YY, size[2]*ZZ)
    else:
      blender.addPlotSurfaceAsShapeKey(
          loc, size[0]*XX, size[1]*YY, size[2]*ZZ, objInterpolant)
  
  objAxis = blender.addParent(loc, objsAxes)
  return objAxis, objInterpolant

def getInterpolant(gridType, p):
  n, d, b = 3, 2, 0
  f = lambda X: 0.5 + 0.5 * (
      np.cos(1+1.4*np.pi*X[:,0]) * np.cos(0.3+1.6*np.pi*X[:,1]))
  
  if gridType is None:
    ftEvaluate = f
  else:
    if gridType == "full":
      grid = helper.grid.FullBoundary(d*[n])
      X, L, I = grid.generate()
    elif gridType == "regularSparse":
      grid = helper.grid.RegularSparseBoundary(n, d, b)
      X, L, I = grid.generate()
    elif gridType == "daSparse":
      L = [
        (0, 0), (1, 0), (2, 0), (3, 0),
        (0, 1), (1, 1), (2, 1), (3, 1),
        (0, 2),
      ]
      grid = helper.grid.DimensionallyAdaptiveSparse(L)
      X, L, I = grid.generate()
    elif gridType == "saSparse":
      L = [
        (0, 0), (0, 0), (0, 0), (0, 0),
        (1, 0), (1, 0),
        (2, 0), (2, 0), (2, 0), (2, 0),
        (0, 1), (0, 1),
        (1, 1),
        (2, 1), (2, 1),
        (0, 2), (0, 2), (0, 2), (0, 2),
        (1, 2), (1, 2),
        
        (0, 3), (0, 3), (0, 3), (0, 3),
        (3, 0), (3, 0), (3, 0), (3, 0),
        (3, 1), (3, 1),
        (2, 2), (2, 2),
        (3, 2), (3, 2),
        (2, 3), (2, 3),
        (1, 3), (1, 3),
      ]
      I = [
        (0, 0), (0, 1), (1, 0), (1, 1),
        (1, 0), (1, 1),
        (1, 0), (1, 1), (3, 0), (3, 1),
        (0, 1), (1, 1),
        (1, 1),
        (1, 1), (3, 1),
        (0, 1), (0, 3), (1, 1), (1, 3),
        (1, 1), (1, 3),
        
        (0, 5), (0, 7), (1, 5), (1, 7),
        (5, 0), (7, 0), (5, 1), (7, 1),
        (5, 1), (7, 1),
        (3, 1), (3, 3),
        (5, 3), (7, 3),
        (3, 5), (3, 7),
        (1, 5), (1, 7),
      ]
      grid = helper.grid.SpatiallyAdaptiveSparse(L, I)
      X, L, I = grid.getGrid()
    else:
      raise ValueError
    
    fX = f(X)
    basis1D = helper.basis.HierarchicalNotAKnotBSpline(p)
    basis = helper.basis.TensorProduct(basis1D, d)
    ft = helper.function.Interpolant(basis, X, L, I, fX)
    ftEvaluate = ft.evaluate
  
  return ftEvaluate



def animate(ani):
  rad = blender.rad
  objAxisBasis,  objBasis  = addHierarchicalBasis()
  objAxisInterp, objInterp = addInterpolant()
  objsAxisBasis  = list(objAxisBasis.children)
  objsBasis      = list(objBasis.children)
  objsAxisInterp = list(objAxisInterp.children)
  objCircle = blender.addCircleHUD((-2, 1.2, 11), 1)
  objsTextDegree = [
      blender.addLaTeXHUD((-1.9, 0.84, 11), r"$p = {}$".format(p))
      for p in [1, 3, 5]]
  objPolygon = blender.addPolygonHUD((0, 0, 11), [
    (-0.2,  3.5,  0),
    (-0.2,  0.75, 0),
    ( 2.1,  0.75, 0),
    ( 2.1, -1.0,  0),
    ( 5.5, -1.0,  0),
    ( 5.5,  3.5,  0),
  ])
  objsTextPoints = [
    blender.addLaTeXHUD((0, 2.65, 11),
r"\textbf{B-splines:}", scale=0.9),
    blender.addLaTeXHUD((0, 2.15, 11), r"""
\begin{itemize}
  \item
  Generalize hat functions
\end{itemize}""", scale=0.9),
    blender.addLaTeXHUD((0, 1.65, 11), r"""
\begin{itemize}
  \item
  Gradient-based optimization
\end{itemize}""", scale=0.9),
    blender.addLaTeXHUD((0, 1.15, 11), r"""
\begin{itemize}
  \item
  Higher order of convergence
\end{itemize}""", scale=0.9),
    blender.addLaTeXHUD((2.3, 0.65, 11), r"""
\begin{itemize}
  \item
  Non-uniform knot sequences
  %Hierarchical not-a-knot B-splines
\end{itemize}""", scale=0.9, textWidth="33mm"),
    blender.addLaTeXHUD((2.3, -0.15, 11), r"""
\begin{itemize}
  \item
  Goal:\\$h$-$p$-adaptivity
\end{itemize}""", scale=0.9, textWidth="30mm"),
  ]
  
  for obj in objsAxisBasis + objsBasis + objsAxisInterp:
    ani.cutCurve(obj, 0, 0, 0)
  for obj in [objAxisBasis, objBasis]:
    ani.move(obj, 0, (-4.5, 11, -2.5))
  for obj in [objAxisInterp, objInterp]:
    ani.move(obj, 0, (-1.2, 9.5, -2))
  for obj in [objAxisBasis, objBasis, objAxisInterp, objInterp]:
    ani.rotate(obj, 0, rad(20, 0, 20))
  for obj in (
      [objInterp] +
      [objCircle] + objsTextDegree +
      [objPolygon] + objsTextPoints):
    ani.fadeOut(obj, 0)
  
  for obj in [objAxisBasis, objBasis, objAxisInterp, objInterp]:
    ani.rotate(obj, 30, rad(20, 0, 30), intp="LINEAR")
  
  for obj in [objPolygon] + objsTextPoints:
    ani.fadeIn(obj, 1)
  
  for obj in objsAxisBasis + objsBasis:
    ani.cutCurve(obj, 0.5, 0, 1)
    ani.wait(0.2)
  ani.wait(1)
  
  for obj in objsAxisInterp:
    ani.cutCurve(obj, 0.5, 0, 1)
    ani.wait(0.2)
  
  ani.fadeIn(objCircle, 1)
  ani.fadeIn(objsTextDegree[0], 1)
  ani.fadeIn(objInterp, 1)
  ani.wait(1)
  
  for obj in objsBasis + [objInterp]: ani.morph(obj, 2, 1)
  ani.fadeOut(objsTextDegree[0], 2)
  ani.fadeIn(objsTextDegree[1], 2)
  ani.wait(2)
  ani.wait(2)
  
  for obj in objsBasis + [objInterp]: ani.morph(obj, 2, 2)
  ani.fadeOut(objsTextDegree[1], 2)
  ani.fadeIn(objsTextDegree[2], 2)
  ani.wait(1)
  ani.wait(20)
  
  for obj in (
      objsAxisBasis + objsBasis +
      objsAxisInterp + [objInterp] +
      [objCircle, objsTextDegree[-1]] +
      [objPolygon] + objsTextPoints):
    ani.fadeOut(obj, 1)
