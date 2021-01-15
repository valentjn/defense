#!/usr/bin/python3
# number of output figures = 1

import matplotlib.patches as patches
import numpy as np

from helper.figure import Figure
import helper.grid
import helper.plot

def plotNodalSpace(X, l, ax, pos, size, K=None, KColor="r", notKColor="b",
                   textColor="k", borderColor="k"):
  xSquare = np.array([0, 1, 1, 0, 0])
  ySquare = np.array([0, 0, 1, 1, 0])
  s = lambda x, y: (pos[0] + size * np.array(x), pos[1] + size * np.array(y))
  
  ax.plot(*s(xSquare, ySquare), "-", color=borderColor,
          clip_on=False, zorder=-2)
  if textColor is not None:
    ax.text(*s(0.5, 0.02), r"$\ns{{({},{})}}$".format(*l),
            color=textColor, ha="center", va="bottom")
  
  N = X.shape[0]
  if K is None: K = np.zeros((N,), dtype=bool)
  
  ax.plot(*s(X[K,0], X[K,1]), ".", clip_on=False, color=KColor, zorder=-1)
  
  K = np.logical_not(K)
  ax.plot(*s(X[K,0], X[K,1]), ".", clip_on=False, color=notKColor, zorder=-1)

def plotSG(n, d, b, ax, pos, size):
  xSquare = np.array([0, 1, 1, 0, 0])
  ySquare = np.array([0, 0, 1, 1, 0])
  s = lambda x, y: (pos[0] + size * np.array(x), pos[1] + size * np.array(y))
  
  ax.plot(*s(xSquare, ySquare), "k-", clip_on=False)
  ax.text(*s(0.5, 0.03), r"$\regsgspace{n}{d}$",
          ha="center", va="bottom")
  
  grid = helper.grid.RegularSparseBoundary(n, d, b)
  X, L, I = grid.generate()
  ax.plot(*s(X[:,0], X[:,1]), "k.", clip_on=False)



def main():
  n = 3
  d = 2
  b = 0
  
  subspaceSize = 1
  subspaceMargin = 0.2
  sgSize = 1.5
  arrowMargin = 0.1
  startEndArrowLength = 0.5
  scaleArrowHead = 2.5
  
  L = [(i, n-i) for i in range(n+1)]
  
  
  
  brightness = 0.4
  schemeSize = (n + 1) * (subspaceSize + subspaceMargin) - subspaceMargin
  xOffsetGlobal = 0
  yOffsetGlobal = schemeSize
  hiddenColor = 3*[0.7]
  
  Xs = [helper.grid.getCoordinates(l, helper.grid.getNodalIndices(l))
        for l in L]
  
  fig = Figure.create(figsize=(5, 3), scale=1.1, facecolor="none")
  ax = fig.gca()
  
  for l0 in range(n+1):
    for l1 in range(n+1):
      l = (l0, l1)
      X = helper.grid.getCoordinates(l, helper.grid.getNodalIndices(l))
      
      xOffset = (xOffsetGlobal +
                 l[0] * (subspaceSize + subspaceMargin))
      yOffset = (yOffsetGlobal -
                 l[1] * (subspaceSize + subspaceMargin) - subspaceSize)
      
      if l not in L:
        plotNodalSpace(X, l, ax, (xOffset, yOffset), subspaceSize,
                       notKColor=hiddenColor, borderColor=hiddenColor,
                       textColor=None)
      else:
        q = L.index(l)
        
        XUnion = (np.unique(np.vstack(Xs[q+1:]), axis=0)
                  if q < len(L) - 1 else np.zeros((0, d)))
        N = X.shape[0]
        K = np.zeros((N,), dtype=bool)
        for k in range(N): K[k] = not (XUnion == X[k,:]).all(axis=1).any()
        
        plotNodalSpace(X, l, ax, (xOffset, yOffset), subspaceSize,
                      K=K, KColor="C0", notKColor="C1")
        
        if q == 0:
          arrowEnd = (xOffset - arrowMargin, yOffset + subspaceSize / 2)
          arrowStart = (arrowEnd[0] - startEndArrowLength, arrowEnd[1])
          helper.plot.plotArrow(ax, arrowStart, arrowEnd,
                                scaleHead=scaleArrowHead)
          ax.text(
              arrowStart[0] - 0.08, arrowStart[1] + 0.15,
              r"$y^{{({})}}_{{\*l,\*i}} = 0,$".format(0),
              ha="right", va="center")
          ax.text(
              arrowStart[0] - 0.08, arrowStart[1] - 0.15,
              (r"$r^{{({})}}(\gp{{\*l,\*i}}) = "
               r"\objfun(\gp{{\*l,\*i}})$").format(0),
              ha="right", va="center")
        elif q == len(L) - 1:
          arrowStart = (xOffset + subspaceSize + arrowMargin,
                        yOffset + subspaceSize / 2)
          arrowEnd = (arrowStart[0] + startEndArrowLength, arrowStart[1])
          helper.plot.plotArrow(ax, arrowStart, arrowEnd,
                                scaleHead=scaleArrowHead)
          ax.text(
              arrowEnd[0] + 0.08, arrowEnd[1] + 0.15,
              r"$y^{{({})}}_{{\*l,\*i}} = "
              r"\surplus{{\*l,\*i}},$".format(q+1),
              ha="left", va="center")
          ax.text(
              arrowEnd[0] + 0.08, arrowEnd[1] - 0.15,
              r"$r^{{({})}}(\gp{{\*l,\*i}}) = 0$".format(q+1),
              ha="left", va="center")
        
        if q < len(L) - 1:
          t = np.linspace(-np.pi/2, 0, 200)
          r = subspaceSize / 2 + subspaceMargin - arrowMargin
          center = (xOffset + subspaceSize + arrowMargin,
                    yOffset + subspaceSize + subspaceMargin - arrowMargin)
          #swap = (q == len(L) - 2)
          swap = False
          if swap: center, t = center[::-1], np.pi/2 - t
          circle = lambda t: (center[0] + r * np.cos(t),
                              center[1] + r * np.sin(t))
          helper.plot.plotArrowPolygon(ax, *circle(t), "k-",
                                       scaleHead=scaleArrowHead)
          ax.text(
              *circle(-np.pi/4 + (np.pi if swap else 0)),
              r"\contour{{white}}{{$y^{{({})}}_{{\*l,\*i}},\, "
              r"r^{{({})}}(\gp{{\*l,\*i}})$}}".format(q+1, q+1),
              ha=("right" if swap else "left"),
              va=("bottom" if swap else "top"))
  
  #plotSG(n, d, b, ax, (0, yOffsetGlobal - sgSize), sgSize)
  
  ax.set_aspect("equal")
  ax.set_xlim([-1.1*subspaceSize, xOffsetGlobal + schemeSize + subspaceSize])
  ax.set_ylim([0, yOffsetGlobal])
  ax.set_axis_off()
  
  fig.save()



if __name__ == "__main__":
  main()
