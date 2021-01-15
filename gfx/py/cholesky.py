#!/usr/bin/python3
# number of output figures = 3

import helper.basis
from helper.figure import Figure
import helper.grid
import helper.plot
import helper.topo_opt

import matplotlib as mpl
import numpy as np



def main():
  normalTransformation = helper.topo_opt.Stats.Transformation.normal
  transformations = [
    helper.topo_opt.Stats.Transformation.normal,
    helper.topo_opt.Stats.Transformation.cholesky,
  ]
  
  d, p = 2, 3
  basis1D = helper.basis.HierarchicalBSpline(p)
  basis = helper.basis.TensorProduct(basis1D, d)
  
  for q in range(2):
    fig = Figure.create(figsize=(3, 3), scale=0.75)
    ax = fig.gca()
    
    stats = helper.topo_opt.Stats()
    stats.load("./data/topoOpt/stats/cross-reg6b4-lb0.01-ub0.99")
    stats.transform(transformations[q])
    stats.hierarchize(basis)
    
    nn = 100
    _, _, XX = helper.grid.generateMeshGrid((nn, nn))
    
    XX = stats.convertGridToDomainCoords(XX)
    YY = stats.evaluate(XX)
    YY = helper.topo_opt.Stats.transformValues(
        YY, transformations[q], helper.topo_opt.Stats.Transformation.normal)
    YY = helper.topo_opt.Stats.getSmallestEigenvalues(YY)
    YY = np.reshape(YY, (nn, nn))
    
    XX = stats.convertDomainToGridCoords(XX)
    XX0, XX1 = np.reshape(XX[:,0], (nn, nn)), np.reshape(XX[:,1], (nn, nn))
    v = np.linspace(0, 0.4, 33)
    ax.contourf(XX0, XX1, -YY, [0, 100], colors="C1")
    ax.contour(XX0, XX1, YY, v)
    
    # remove weird hairline from (0.00015128, 0) to (0, 0.00015128)
    # (behind origin grid point, has line width of 0.0311
    # according to Preflight)
    for child in ax.get_children():
      if isinstance(child, mpl.collections.LineCollection):
        segments = [XX for XX in child.get_segments()
                    if not np.any(np.all(XX < 0.01, axis=1))]
        if len(segments) != len(child.get_segments()):
          child.set_segments(segments)
    
    X = stats.convertDomainToGridCoords(stats.X)
    ax.plot(X[:,0], X[:,1], "k.", clip_on=False)
    
    ax.set_aspect("equal")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    xt, yt = np.linspace(0, 1, 5), np.linspace(0, 1, 5)
    ax.set_xticks(xt)
    ax.set_yticks(yt)
    ax.set_xticklabels(["${:g}$".format(x) for x in xt])
    ax.set_yticklabels(["${:g}$".format(y) for y in yt])
    
    trafo = helper.plot.getTransformationFromUnitCoordinates(ax)
    ax.text(*trafo(0.625, -0.05), r"$x_1$", ha="center", va="top")
    ax.text(*trafo(-0.05, 0.625), r"$x_2$", ha="right", va="center")
    
    fig.save()
  
  
  
  fig = Figure.create(figsize=(0.8, 2.3), scale=0.9)
  ax = fig.gca()
  
  colorMap = mpl.cm.viridis
  colorMap.set_under("C1")
  norm = mpl.colors.BoundaryNorm(v, colorMap.N)
  colorBar = mpl.colorbar.ColorbarBase(
      ax, cmap=colorMap, norm=norm, extend="min", drawedges=True,
      ticks=[0, 0.1, 0.2, 0.3, 0.4])
  colorBar.dividers.set_color(
      [colorMap(x) for x in np.linspace(0, 1, len(v)-1)])
  
  fig.save()



if __name__ == "__main__":
  main()
