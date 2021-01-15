#!/usr/bin/python3
# number of output figures = 8

import numpy as np
import matplotlib.patches

import helper.basis
from helper.figure import Figure
import helper.grid
import helper.misc
import helper.plot



def isEquivalent(l, lp, xl):
  d = xl.shape[0]
  T = [t for t in range(d) if l[t] == lp[t]]
  return all([min(l[t], lp[t]) >= xl[t] for t in range(d) if t not in T])



def plotSGScheme(basis, n, showDiagonal=True, highlightedSubspaces=None,
                 highlightedPoints=None, whiteMode=False, withBoundary=True,
                 isModified=False, combinationTechnique=False,
                 singleGrid=False, equivalenceRelation=False):
  subspaceSize = 1
  subspaceMargin = 0.2
  basisSize = (0.3 if singleGrid else 0.6)
  basisMargin = (0.1 if singleGrid else 0.2)
  
  upperLevel = n
  
  if singleGrid:
    lowerLevel = n
    levelSumDiagonal = 2*n
  elif withBoundary:
    lowerLevel = 0
    levelSumDiagonal = n
  else:
    lowerLevel = 1
    levelSumDiagonal = n+1
  
  numberOfSubspaces = upperLevel - lowerLevel + 1
  
  schemeSize = numberOfSubspaces * (subspaceSize + subspaceMargin) - subspaceMargin
  xOffsetGlobal = basisSize + basisMargin
  yOffsetGlobal = schemeSize
  
  xSquare = np.array([0, 1, 1, 0, 0])
  ySquare = np.array([0, 0, 1, 1, 0])
  
  I = (helper.grid.getNodalIndices if combinationTechnique else
       helper.grid.getHierarchicalIndices)
  
  hellhellblau = helper.plot.mixColors("hellblau", 0.5)
  
  fig = Figure.create(figsize=(3, 3), scale=1, facecolor="none",
                      preamble=r"""
\definecolor{{hellhellblau}}{{rgb}}{{{},{},{}}}
""".format(*hellhellblau))
  ax = fig.gca()
  
  stairsCornersInner = []
  stairsCornersOuter = []
  
  for l0 in range(lowerLevel, upperLevel + 1):
    Il0 = I(l0)
    hl0Inv = 2**l0
    hl0 = 1 / hl0Inv
    Xl0 = [i * hl0 for i in Il0]
    
    for l1 in range(lowerLevel, upperLevel + 1):
      Il1 = I(l1)
      hl1Inv = 2**l1
      hl1 = 1 / hl1Inv
      Xl1 = [i * hl1 for i in Il1]
      
      xOffset = (xOffsetGlobal + (l0 - lowerLevel) *
                 (subspaceSize + subspaceMargin))
      yOffset = (yOffsetGlobal - (l1 - lowerLevel) *
                 (subspaceSize + subspaceMargin) - subspaceSize)
      corner = (xOffset + subspaceSize + subspaceMargin / 2,
                yOffset - subspaceMargin / 2)
      
      if l0 + l1 == levelSumDiagonal - 1:
        stairsCornersInner.append(corner)
      elif l0 + l1 == levelSumDiagonal:
        stairsCornersOuter.append(corner)
      
      s = lambda x, y: (xOffset + subspaceSize * np.array(x),
                        yOffset + subspaceSize * np.array(y))
      
      if combinationTechnique:
        brightness = 0.4
        
        if equivalenceRelation:
          if levelSumDiagonal - 1 <= l0 + l1 <= levelSumDiagonal:
            xl = np.array((2, 1))
            xi = np.array((1, 1))

            allL = ([(i, n-i) for i in range(n+1)] +
                    [(i, n-i-1) for i in range(n)])
            L = [l for l in allL if not ((l[0] >= xl[0]) and (l[1] >= xl[1]))]
            
            equivalenceClasses = helper.misc.getEquivalenceClasses(
                L, (lambda l, lp: isEquivalent(l, lp, xl)))
            
            J = [j for j, equivalenceClass in enumerate(equivalenceClasses)
                 if (l0, l1) in equivalenceClass]
            
            if len(J) == 0:
              j = None
              contourColor = "anthrazit!20"
              faceColor = helper.plot.mixColors("anthrazit", 0.2)
              color = "k"
            else:
              j = J[0]
              colorIndices = [2, 5, 7]
              contourColor = "C{}".format(colorIndices[j])
              faceColor = contourColor
              color = [brightness * x
                       for x in matplotlib.colors.to_rgba(contourColor)[:3]]
          else:
            contourColor = "anthrazit!20"
            faceColor = helper.plot.mixColors("anthrazit", 0.2)
            color = 3*[0.6]
        else:
          if l0 + l1 == levelSumDiagonal:
            if singleGrid:
              contourColor = "hellhellblau"
              faceColor = hellhellblau
              color = "mittelblau"
            else:
              contourColor = "C4"
              faceColor = "C4"
              color = [brightness * x
                      for x in matplotlib.colors.to_rgba(contourColor)[:3]]
          elif l0 + l1 == levelSumDiagonal - 1:
            contourColor = "C1"
            faceColor = "C1"
            color = [brightness * x
                    for x in matplotlib.colors.to_rgba(contourColor)[:3]]
          else:
            contourColor = "anthrazit!20"
            faceColor = helper.plot.mixColors("anthrazit", 0.2)
            color = 3*[0.6]
        
        rect = matplotlib.patches.Rectangle(
          (xOffset, yOffset), subspaceSize, subspaceSize, edgecolor="none",
          facecolor=faceColor)
        ax.add_patch(rect)
      elif (((highlightedSubspaces is not None) and
           ((l0, l1) in highlightedSubspaces)) or
          ((highlightedSubspaces is None) and
           (highlightedPoints is None) and
           (l0 + l1 <= levelSumDiagonal))):
        contourColor = "hellhellblau"
        color = "mittelblau"
        rect = matplotlib.patches.Rectangle(
          (xOffset, yOffset), subspaceSize, subspaceSize, edgecolor="none",
          facecolor=hellhellblau)
        ax.add_patch(rect)
      else:
        contourColor = "white"
        color = "k"
      
      if highlightedPoints is not None:
        borderColor = "k"
      else:
        borderColor = color
      
      Xl = np.array([(x0, x1) for x0 in Xl0 for x1 in Xl1])
      
      if highlightedPoints is None:
        K = np.zeros((Xl.shape[0],), dtype=bool)
      else:
        K = np.any(np.all(highlightedPoints == Xl[:,np.newaxis], axis=2), axis=1)
      
      for k in np.where(K)[0]:
        x = Xl[k,:]
        rect = matplotlib.patches.Rectangle(
          s(max(x[0]-hl0, 0), max(x[1]-hl1, 0)), min(2*hl0, 1), min(2*hl1, 1),
          edgecolor="none", facecolor=hellhellblau)
        ax.add_patch(rect)
      
      ax.plot(*s(xSquare, ySquare), "-", clip_on=False, color=borderColor)
      
      superscript = (r"\modified" if isModified else "")
      subspaceName = ("V" if combinationTechnique else "W")
      
      text = "${}_{{({},{})}}^{{{}}}$".format(
          subspaceName, l0, l1, superscript)
      y = 0.042
      
      if not (equivalenceRelation and (l0 >= 2) and (l1 == 0)):
        text = "\\contour{{{}}}{{{}}}".format(contourColor, text)
        y = 0
      
      ax.text(*s(0.5, y), text, color=color, ha="center", va="bottom")
      
      ax.plot(*s(Xl[K,0], Xl[K,1]), ".", clip_on=False,
              color="mittelblau")
      ax.plot(*s(Xl[np.invert(K),0], Xl[np.invert(K),1]), ".", clip_on=False,
              color=color)
      
      if not combinationTechnique:
        if l0 > 0:
          for x0 in np.linspace(0, 1, hl0Inv // 2 + 1):
            ax.plot(*s([x0, x0], [0, 1]), "-", clip_on=False,
                    color=borderColor)
        
        if l1 > 0:
          for x1 in np.linspace(0, 1, hl1Inv // 2 + 1):
            ax.plot(*s([0, 1], [x1, x1]), "-", clip_on=False,
                    color=borderColor)
      elif (equivalenceRelation and
            (levelSumDiagonal - 1 <= l0 + l1 <= levelSumDiagonal)):
        d = 2
        x = helper.grid.getCoordinates(xl, xi)
        ax.plot(*s(x[0], x[1]), "x", clip_on=False, color=color,
                markeredgewidth=2)
        
        if j is not None:
          lAst = [l0, l1]
          
          for l2 in equivalenceClasses[j]:
            lAst = [(None if lAst[t] is None else
                     (lAst[t] if l2[t] == lAst[t] else None))
                    for t in range(d)]
          
          T = [t for t in range(d) if lAst[t] is not None]
          
          if T[0] == 0:
            ax.plot(*s([0, 1], [x[1], x[1]]), "-", clip_on=False, color=color)
          else:
            ax.plot(*s([x[0], x[0]], [0, 1]), "-", clip_on=False, color=color)
  
  if not singleGrid:
    stairsCorners = [stairsCornersOuter[0]]
    
    for l in range(n - lowerLevel):
      stairsCorners.append(stairsCornersInner[l])
      stairsCorners.append(stairsCornersOuter[l+1])
    
    stairsCorners = np.array(stairsCorners)
    
    if showDiagonal:
      ax.plot(stairsCorners[:,0], stairsCorners[:,1], "k--", clip_on=False)
  
  maxY = {}
  modifiedScale = (0.56 if isModified else 1)
  
  for l in range(lowerLevel, upperLevel + 1):
    maxY[l] = 0
    
    for i in I(l):
      lb, ub = basis.getSupport(l, i)
      xx = np.linspace(lb, ub, 33)
      yy = basis.evaluate(l, i, xx)
      if (i == 1) or (i == 2**l - 1): yy = [modifiedScale * y for y in yy]
      maxY[l] = max(max(yy), maxY[l])
  
  for l0 in range(lowerLevel, upperLevel + 1):
    xOffset = xOffsetGlobal + (l0 - lowerLevel) * (subspaceSize + subspaceMargin)
    
    for i0 in I(l0):
      color = "C{}".format((i0 * 2**(n - l0)) % 9)
      yOffset = yOffsetGlobal + basisMargin
      s = lambda x, y: (xOffset + subspaceSize * np.array(x),
                        yOffset + basisSize * np.array(y) / maxY[l0])
      
      lb, ub = basis.getSupport(l0, i0)
      xx = np.linspace(lb, ub, 33)
      yy = basis.evaluate(l0, i0, xx)
      if (i0 == 1) or (i0 == 2**l0 - 1): yy = [modifiedScale * y for y in yy]
      ax.plot(*s(xx, yy), "-", clip_on=False, color=color)
  
  for l1 in range(lowerLevel, upperLevel + 1):
    yOffset = (yOffsetGlobal - (l1 - lowerLevel) *
               (subspaceSize + subspaceMargin) - subspaceSize)
    
    for i1 in I(l1):
      color = "C{}".format((i1 * 2**(n - l1)) % 9)
      xOffset = xOffsetGlobal - basisMargin
      s = lambda x, y: (xOffset - basisSize * np.array(y) / maxY[l1],
                        yOffset + subspaceSize * np.array(x))
      
      lb, ub = basis.getSupport(l1, i1)
      xx = np.linspace(lb, ub, 200)
      yy = basis.evaluate(l1, i1, xx)
      if (i1 == 1) or (i1 == 2**l1 - 1): yy = [modifiedScale * y for y in yy]
      ax.plot(*s(xx, yy), "-", clip_on=False, color=color)
  
  color = "k"
  ax.plot((xOffsetGlobal - basisMargin) * np.ones((2,)),
          [0, yOffsetGlobal + basisMargin + 0.2 * basisSize],
          "-", c=color, clip_on=False)
  ax.plot([xOffsetGlobal - basisMargin - 0.2 * basisSize,
           xOffsetGlobal + schemeSize],
          (yOffsetGlobal + basisMargin) * np.ones((2,)),
          "-", c=color, clip_on=False)
  
  ax.set_xlim([0, xOffsetGlobal + schemeSize])
  ax.set_ylim([0, yOffsetGlobal + basisMargin + basisSize])
  
  ax.set_xticks([])
  ax.set_yticks([])
  ax.spines["left"].set_visible(False)
  ax.spines["bottom"].set_visible(False)
  
  return fig, ax



def plotGrid(sgType, n=None, includedSubspaces=[], includedPoints=None,
             withBoundary=True, distribution="uniform", scale=1.65):
  fig = Figure.create(figsize=(1, 1), scale=scale)
  ax = fig.gca()
  
  X = np.zeros((0, 2))
  I = lambda l: ([0, 1] if l == 0 else list(range(1, 2**l, 2)))
  
  if (sgType == "full") or (sgType == "regular"):
    upperLevel = n
    
    if withBoundary:
      lowerLevel = 0
      levelSumDiagonal = n
    else:
      lowerLevel = 1
      levelSumDiagonal = n + 1
    
    for l0 in range(lowerLevel, upperLevel + 1):
      Xl0 = helper.grid.getCoordinates(len(I(l0)) * [l0], I(l0),
                                       distribution=distribution)
      
      for l1 in range(lowerLevel, upperLevel + 1):
        Xl1 = helper.grid.getCoordinates(len(I(l1)) * [l1], I(l1),
                                         distribution=distribution)
        Xl = np.array([(x0, x1) for x0 in Xl0 for x1 in Xl1])
        
        if (sgType == "full") or ((sgType == "regular") and
                                  (l0 + l1 <= levelSumDiagonal)):
          X = np.vstack((X, Xl))
  elif sgType == "adaptive":
    X = (np.array(includedPoints) if includedPoints is not None else
         np.array((0, 2)))
    
    for l in includedSubspaces:
      l0, l1 = l
      Xl0 = [i * 2**(-l0) for i in I(l0)]
      Xl1 = [i * 2**(-l1) for i in I(l1)]
      Xl = np.array([(x0, x1) for x0 in Xl0 for x1 in Xl1])
      X = np.vstack((X, Xl))
  else:
    raise ValueError("Unsupported grid type.")
  
  ax.plot(X[:,0], X[:,1], "k.", clip_on=False)
  ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], "k-", clip_on=False)
  
  ax.set_xlim([0, 1])
  ax.set_ylim([0, 1])
  ax.set_xticks([])
  ax.set_yticks([])
  ax.spines["left"].set_visible(False)
  ax.spines["bottom"].set_visible(False)
  
  return fig, ax



def main():
  n = 3
  p = 1
  basis = helper.basis.HierarchicalBSpline(p)
  withBoundary = True
  isModified = False
  
  fig, ax = plotSGScheme(
      basis, n, showDiagonal=False, withBoundary=withBoundary,
      highlightedSubspaces=[(n, n)], isModified=isModified,
      singleGrid=True, combinationTechnique=True)
  fig.save()
  
  L = [(l0, l1) for l0 in range(n+1) for l1 in range(n+1)]
  fig, ax = plotSGScheme(
      basis, n, showDiagonal=False, withBoundary=withBoundary,
      highlightedSubspaces=L, isModified=isModified)
  fig.save()
  
  #fig, ax = plotGrid("full", n=n, withBoundary=withBoundary)
  #fig.save()
  
  
  
  fig, ax = plotSGScheme(
      basis, n, showDiagonal=True, withBoundary=withBoundary,
      isModified=isModified)
  fig.save()
  
  
  
  L = [
    (0, 0), (1, 0), (2, 0), (3, 0),
    (0, 1), (1, 1), (2, 1), (3, 1),
    (0, 2),
  ]
  
  fig, ax = plotSGScheme(
      basis, n, showDiagonal=False, highlightedSubspaces=L,
      withBoundary=withBoundary, isModified=isModified)
  fig.save()
  
  #fig, ax = plotGrid(
  #    "adaptive", includedSubspaces=L, withBoundary=withBoundary)
  #fig.save()
  
  
  
  L = [
    (0, 0), (1, 0), (2, 0),
    (0, 1), (1, 1), (2, 1),
    (0, 2), (1, 2),
  ]
  Omega = np.array([
    [0, 0.625], [0, 0.875], [1, 0.625], [1, 0.875],
    [0.625, 0], [0.875, 0], [0.625, 1], [0.875, 1],
    [0.625, 0.5], [0.875, 0.5],
    [0.75, 0.25], [0.75, 0.75],
    [0.625, 0.75], [0.875, 0.75],
    [0.75, 0.625], [0.75, 0.875],
    [0.5, 0.625], [0.5, 0.875],
  ])
  
  fig, ax = plotSGScheme(
      basis, n, showDiagonal=False, highlightedSubspaces=L,
      highlightedPoints=Omega, withBoundary=withBoundary,
      isModified=isModified)
  fig.save()
  
  p = 3
  basis = helper.basis.HierarchicalBSpline(p)
  
  #fig, ax = plotSGScheme(
  #    basis, n, showDiagonal=False, highlightedSubspaces=L,
  #    highlightedPoints=Omega, withBoundary=withBoundary,
  #    isModified=isModified)
  #fig.save()
  
  #fig, ax = plotGrid(
  #    "adaptive", includedSubspaces=L, includedPoints=Omega,
  #    withBoundary=withBoundary)
  #fig.save()
  
  
  
  fig, ax = plotSGScheme(
      basis, n, showDiagonal=False, combinationTechnique=True,
      withBoundary=withBoundary, isModified=isModified)
  fig.save()
  
  fig, ax = plotSGScheme(
      basis, n, showDiagonal=False, combinationTechnique=True,
      withBoundary=withBoundary, isModified=isModified,
      equivalenceRelation=True)
  fig.save()
  
  
  
  fig, ax = plotGrid("regular", n=n, withBoundary=withBoundary, scale=1.5)
  fig.save()



if __name__ == "__main__":
  main()
