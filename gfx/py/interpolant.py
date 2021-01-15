#!/usr/bin/python3
# number of output figures = 6

import matplotlib as mpl
import numpy as np

import helper.basis
from helper.figure import Figure
import helper.function
import helper.grid



def main():
  f = lambda X: np.cos(1+1.4*np.pi*X[:,0]) * np.cos(0.3+1.6*np.pi*X[:,1])
  
  for gridType, p in [(None, None), ("full", 1), ("regularSparse", 1),
                      ("daSparse", 1), ("saSparse", 1), ("saSparse", 3)]:
    n, d, b = 3, 2, 0
    
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
    
    fig = Figure.create(figsize=(2.5, 2.7))
    ax = fig.add_subplot(111, projection="3d")
    
    z = -3
    
    if gridType is not None:
      ax.plot(X[:,0], X[:,1], "k.", zs=z*np.ones_like(fX), zorder=-1)
      
      for x, fx in zip(X, fX):
        #if np.all(x > 0) and np.all(x < 1): continue
        if (x[0] < 1) and (x[1] > 0): continue 
        if np.all(x == (1, 0)) or np.all(x == (1, 0.25)):
          zOrder = 1
        else:
          zOrder = -1
        
        ax.plot([x[0], x[0]], [x[1], x[1]], "-", zs=[z, fx], zorder=zOrder,
                c=3*[0.5], alpha=0.8, solid_capstyle="butt")
    
    XX0, XX1, XX = helper.grid.generateMeshGrid((129, 129))
    YY = np.reshape(ftEvaluate(XX), XX0.shape)
    lightSource = mpl.colors.LightSource(90, 0)
    faceColors = lightSource.shade(YY, cmap=mpl.cm.viridis,
                                  vert_exag=0.1, blend_mode="soft")
    ax.plot_surface(XX0, XX1, YY, facecolors=faceColors, shade=False, lw=0)
    
    eps = 0.05
    ax.plot([0, 0],     [0, -eps], "k-", zs=[z, z])
    ax.plot([1, 1],     [0, -eps], "k-", zs=[z, z])
    ax.plot([1, 1+eps], [0, 0],    "k-", zs=[z, z])
    ax.plot([1, 1+eps], [1, 1],    "k-", zs=[z, z])
    
    eps = 0.1
    ax.text(0,     -eps, z, r"$0$", ha="right", va="top")
    ax.text(1,     -eps, z, r"$1$", ha="right", va="top")
    ax.text(1+eps, 0,    z, r"$0$", ha="left", va="top")
    ax.text(1+eps, 1,    z, r"$1$", ha="left", va="top")
    
    ax.text(0.52, -0.2, z, r"$x_1$", ha="left", va="top")
    ax.text(1.1,  0.45, z, r"$x_2$", ha="left", va="top")
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(z, 0.85)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    
    ax.w_xaxis.set_pane_color(4*[0])
    ax.w_yaxis.set_pane_color(4*[0])
    
    fig.save(fix3DTransparency=False)



if __name__ == "__main__":
  main()
