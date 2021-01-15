#!/usr/bin/python3
# number of output figures = 5

import numpy as np

import helper.basis
from helper.figure import Figure
import helper.function



def main():
  f = lambda x: -10.2 * x**3 + 14.7 * x**2 - 5 * x + 0.7
  n = 3
  d = 1
  b = 0
  p = 3
  
  bases = [helper.basis.HierarchicalBSpline(p),
           helper.basis.HierarchicalNotAKnotBSpline(p)]
  xtl = [r"$\gp{{{},{}}}$".format(n, i) for i in range(2**n + 1)]
  
  figsize = (2.2, 1.7)
  
  
  for q in range(2):
    basis = bases[q]
    
    for r in range(2):
      if (q == 1) and (r == 1): continue
      
      fig = Figure.create(figsize=figsize)
      ax = fig.gca()
      
      xx = np.linspace(0, 1, 513)
      yy = f(xx)
      ax.plot(xx, yy, "-", clip_on=False, color="C0")
      ax.text(0.95, 0.6, r"$\objfun$", ha="left", va="bottom", color="C0")
      
      grid = helper.grid.RegularSparseBoundary(n, d, b)
      X, L, I = grid.generate()
      fX = f(X)
      interpolant = helper.function.Interpolant(basis, X, L, I, fX)
      XX = np.array([xx]).T
      yy2 = interpolant.evaluate(XX)
      ax.plot(xx, yy2, "--", clip_on=False, color="C1")
      ax.text(0.91, 0.5, r"$\sgintp$", ha="right", va="top", color="C1")
      
      ax.plot(X, fX, "k.", clip_on=False)
      
      if r > 0:
        D = [2**(-n) * (p-1)/2, 1 - 2**(-n) * (p-1)/2]
        ax.plot(D, [0, 0], "k-", clip_on=False, lw=2, solid_capstyle="butt")
        ax.text(0.5, 0.05, r"$\rspldomain{{{}}}{{{}}}$".format(n, "p"),
                ha="center", va="bottom")
      
      ax.set_xlim(0, 1)
      ax.set_xticks(np.sort(X.flatten()))
      ax.set_xticklabels(xtl)
      
      ax.set_ylim(0, 1)
      ax.set_yticks([0, 1])
      ax.set_yticklabels(
          [r"$\textcolor{anthrazit!20}{10^{-18}}\mathllap{0}$", r"$1$"])
      
      fig.save()
    
    
    
    fig = Figure.create(figsize=figsize)
    ax = fig.gca()
    yMin = 1e-16
    
    err = np.abs((yy - yy2.flatten()) / yy)
    err = np.maximum(err, yMin)
    ax.plot(xx, err, "k-", clip_on=False)
    ax.text(0.86, (1e-4 if q == 0 else 1e-12),
            r"\contour{anthrazit!20}{$\abs{\objfun - \sgintp}$}",
            ha="right", va="top")
    
    ax.set_xlim(0, 1)
    ax.set_xticks(np.sort(X.flatten()))
    ax.set_xticklabels(
        [r"\textcolor{{anthrazit!20}}{{{}}}".format(x) for x in xtl])
    
    ax.set_yscale("log")
    ax.set_ylim([yMin, 1e0])
    
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.xaxis.tick_top()
    
    fig.save(hideSpines=False)



if __name__ == "__main__":
  main()
