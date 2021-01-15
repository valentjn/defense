#!/usr/bin/python3

import numpy as np

import helper.basis
from helper.figure import Figure
import helper.plot



def main():
  p = 3
  
  fig = Figure.create(figsize=(2.3, 1.3))
  ax = fig.gca()
  
  basisWF = helper.basis.WeaklyFundamentalSpline(p)
  supportWF = basisWF.getSupport()
  
  K = np.linspace(supportWF[0]+(p+1)/2, supportWF[1]-(p+1)/2,
                  supportWF[1]-supportWF[0]-(p+1)+1)
  xl = [supportWF[0] - 0.5, supportWF[1] + 0.5]
  
  basis = helper.basis.CentralizedCardinalBSpline(p)
  support = basis.getSupport()
  color = helper.plot.mixColors("C0", 0.5)
  
  for k in K:
    xx = np.linspace(max(support[0]-k, xl[0]), min(support[1]-k, xl[1]), 101)
    yy = basis.evaluate(xx + k)
    ax.plot(xx, yy, "-", color=color, clip_on=False)
  
  xx = np.linspace(*supportWF, 129)
  yy = basisWF.evaluate(xx)
  ax.plot(xx, yy, "-", color="C0", lw=1.5, clip_on=False)
  
  ax.plot(np.linspace(2-p, p-2, p-1), np.zeros((p-1,)), "o", color="C0",
          mfc="none", clip_on=False)
  
  ax.set_xticks(np.linspace(np.ceil(xl[0]), np.floor(xl[1]),
                            int(np.floor(xl[1]) - np.ceil(xl[0]) + 1)))
  ax.set_xlim(*xl)
  
  ax.set_yticks([0])
  
  ax.spines["bottom"].set_position("zero")
  
  fig.save()



if __name__ == "__main__":
  main()
