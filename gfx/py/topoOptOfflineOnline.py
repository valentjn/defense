#!/usr/bin/python3
# number of output figures = 7

import numpy as np

from helper.figure import Figure
import helper.grid



def main():
  backgroundColor = "anthrazit!20"
  edgeColor = "black"
  faceColor = "mittelblau"
  
  n, d, b = 3, 2, 1
  X, _, _ = helper.grid.RegularSparseBoundary(n, d, b).generate()
  
  for q in range(3):
    fig = Figure.create(figsize=(1, 1), scale=1.3)
    ax = fig.gca()
    
    #ax.fill([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=backgroundColor)
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], "-", clip_on=False,
            color=edgeColor)
    ax.plot(*X.T, ".", clip_on=False, color=edgeColor)
    
    if q > 0:
      ax.text(
          0.5, 0.5,
          r"\contour{{{}}}{{{}}}".format(backgroundColor,
            r"$\etensor(\gp{\*k})$" if q == 1 else r"$\cholfactor(\gp{\*k})$"
          ),
          ha="center", va="center", color=edgeColor)
    
    ax.set_aspect("equal")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    
    fig.save()
  
  
  
  as_, bs = [0.2, 0.4, 0.4, 0.5], [0.5, 0.3, 0.4, 0.2]
  x0s, x1s = [0, 1, 0, 1], [0, 0, 1, 1]
  
  for q in range(4):
    fig = Figure.create(figsize=(1, 1), scale=1.2)
    ax = fig.gca()
    
    for a, b, x0, x1 in zip(as_, bs, x0s, x1s):
      ax.fill(x0 + np.array([0, 1, 1, 0, 0]),
              x1 + np.array([(1-a)/2, (1-a)/2, (1+a)/2, (1+a)/2, (1-a)/2]),
              color=faceColor)
      ax.fill(x0 + np.array([(1-b)/2, (1+b)/2, (1+b)/2, (1-b)/2, (1-b)/2]),
              x1 + np.array([0, 0, 1, 1, 0]),
              color=faceColor)
    
    for x in range(3):
      ax.plot([-0.01, 1.99], [x+0.01, x+0.01], "k-", clip_on=False,
              color=edgeColor)
      ax.plot([x-0.01, x-0.01], [0.01, 2.01], "k-", clip_on=False,
              color=edgeColor)
    
    ax.text(
      1, 1,
      r"\contour{{{}}}{{{}}}".format(backgroundColor, [
        r"$\*x^{(j)}$",
        r"$\etensorintp(\*x^{(j)})$",
        r"$\cholfactorintp(\*x^{(j)})$",
        r"$\etensorcholintp(\*x^{(j)})$",
      ][q]), ha="center", va="center", color=edgeColor)
    
    ax.set_aspect("equal")
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_axis_off()
    
    fig.save()



if __name__ == "__main__":
  main()
