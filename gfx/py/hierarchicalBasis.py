#!/usr/bin/python3
# number of output figures = 9

import multiprocessing

import numpy as np

import helper.basis
from helper.figure import Figure
import helper.grid

def plotSubspace(ax, basis, l, n,
                 nodal=False, modified=False, clenshawCurtis=False,
                 notAKnot=False, natural=False,
                 fundamental=False, drawModifiedOnTop=False,
                 showSubspaces=False, whiteCC=False, showD=False,
                 basisSymbol=r"\varphi", superscript=None):
  if modified and (l == 0): return
  
  try:    p = basis.p
  except: p = None
  
  hInv = 2**l
  I = (list(range(1, hInv, 2)) if l > 0 else [0, 1])
  plotI = (list(range(hInv + 1)) if nodal else I)
  maxY = 0
  
  if superscript is None: superscript = ("p" if p > 1 else "1")
  if clenshawCurtis:  superscript += r",\cc"
  if notAKnot:        superscript += r",\nak"
  if modified:        superscript += r",\modified"
  if superscript != "": superscript = r"^{{{}}}".format(superscript)
  
  if clenshawCurtis: pointSuperscript = r"^{\cc}"
  elif whiteCC:      pointSuperscript = r"^{\vphantom{\cc}}"
  else:              pointSuperscript = ""
  
  for i in plotI:
    if drawModifiedOnTop:
      if (l == 0) or ((l >= 3) and (1 < i < hInv - 1)): continue
      ls = "--"
    else:
      ls = "-"
    
    color = "C{}".format((i * 2**(n - l)) % 9)
    
    lb, ub = basis.getSupport(l, i)
    xx = np.linspace(lb, ub, 200)
    yy = basis.evaluate(l, i, xx)
    ax.plot(xx, yy, ls, clip_on=False, color=color)
    maxY = max(max(yy), maxY)
    
    if drawModifiedOnTop: continue
    
    j = np.argmax(yy)
    x, y = xx[j], yy[j] * 1.05
    if modified:
      if l == 1:     x, y = 0.5, 1.02
      elif l == 2:
        if   i == 1: x, y = 0.32, 1
        elif i == 3: x, y = 0.73, 1
      elif l == 3:
        if   i == 1: x, y = 0.20, 1
        elif i == 3: x += 0.03
        elif i == 5: pass
        elif i == 7: x, y = 0.83, 1
    if notAKnot:
      if nodal:
        if   i == 2: x -= 0.03
        elif i == 5: x += 0.05
        elif i == 6: x += 0.03
      else:
        if ((not modified) and (not clenshawCurtis) and
            ("{fs}" not in superscript)):
          if (l == 0) and (i == 1): x -= 0.03
          if (l == 3) and (i == 3): x += 0.03
          if (l == 3) and (i == 5): x -= 0.03
    
    text = "${}_{{{},{}}}{}$".format(basisSymbol, l, i, superscript)
    if nodal or (l == 0):
      text = r"\contour{{white}}{{{}}}".format(text)
      y -= 0.02
    ax.text(x, y, text, color=color, ha="center", va="bottom")
  
  if showD:
    D = [2**(-n) * (p-1)/2, 1 - 2**(-n) * (p-1)/2]
    ax.plot(D, [0, 0], "k-", clip_on=False, lw=2)
  
  maxY *= 1.1
  color = "k"
  
  distribution = ("clenshawCurtis" if clenshawCurtis else "uniform")
  x = helper.grid.getCoordinates(l, plotI, distribution=distribution)
  ax.plot(x, 0*x, ".", c=color, clip_on=False)
  
  if notAKnot and (l > 0):
    nakI = list(range(1, (p+1)//2)) + list(range(hInv - (p-1)//2, hInv))
    x = helper.grid.getCoordinates(l, nakI, distribution=distribution)
    ax.plot(x, 0*x, "x", c=color, clip_on=False, ms=5)
  
  if showSubspaces:
    restriction = (r"|_{{D_{{{}}}^{{{}}}}}".format(n, "p") if showD else "")
    spaceSuperscript = superscript
    
    if not nodal:
      ax.text(-0.03, maxY / 2, "$l = {}$".format(l),
              ha="right", va="center", color=color)
  
  L = (hInv + 1) * [l]
  x = helper.grid.getCoordinates(L, list(range(hInv + 1)), distribution=distribution)
  ax.set_xticks(x)
  ax.set_xticklabels([("$x_{{{},{}}}{}$".format(l, i, pointSuperscript)
                       if i in plotI else "")
                      for i in range(hInv + 1)])
  
  ax.set_xlim(0, 1)
  
  if fundamental:
    ax.set_yticks([0, 1])
    ax.set_ylim(0, 1.1)
  else:
    ax.set_yticks([0])
    ax.set_ylim(0, maxY)



def plotHierarchicalHatFunctions(q):
  fig = Figure.create(figsize=(3.0, 4.2), scale=0.85)
  basis = helper.basis.HierarchicalBSpline(1)
  for l in range(n+1):
    ax = fig.add_subplot(n+1, 1, l+1)
    plotSubspace(ax, basis, l, n, showSubspaces=True)
  fig.save(tightLayout=tightLayout, graphicsNumber=q+1)

def plotNodalUniformBSplines(q):
  fig = Figure.create(figsize=(3.0, 1.74), scale=0.85)
  basis = helper.basis.HierarchicalBSpline(p)
  ax = fig.gca()
  plotSubspace(ax, basis, n, n, nodal=True, showSubspaces=True, showD=True)
  fig.save(tightLayout=tightLayout, graphicsNumber=q+1)

def plotHierarchicalUniformBSplines(q):
  fig = Figure.create(figsize=(3.0, 4.2), scale=0.85)
  basis = helper.basis.HierarchicalBSpline(p)
  for l in range(n+1):
    ax = fig.add_subplot(n+1, 1, l+1)
    plotSubspace(ax, basis, l, n, showSubspaces=True)
  fig.save(tightLayout=tightLayout, graphicsNumber=q+1)

def plotHierarchicalUniformBSplinesWithD(q):
  fig = Figure.create(figsize=(3.0, 4.2), scale=0.85)
  basis = helper.basis.HierarchicalBSpline(p)
  for l in range(n+1):
    ax = fig.add_subplot(n+1, 1, l+1)
    plotSubspace(ax, basis, l, n, showSubspaces=True, showD=True)
  fig.save(tightLayout=tightLayout, graphicsNumber=q+1)

def plotNodalNotAKnotBSplines(q):
  fig = Figure.create(figsize=(3.0, 1.74), scale=0.85)
  basis = helper.basis.HierarchicalNotAKnotBSpline(p)
  ax = fig.gca()
  plotSubspace(ax, basis, n, n, nodal=True, notAKnot=True, showSubspaces=True)
  fig.save(tightLayout=tightLayout, graphicsNumber=q+1)

def plotHierarchicalNotAKnotBSplines(q):
  fig = Figure.create(figsize=(3.0, 4.2), scale=0.85)
  basis = helper.basis.HierarchicalNotAKnotBSpline(p)
  for l in range(n+1):
    ax = fig.add_subplot(n+1, 1, l+1)
    plotSubspace(ax, basis, l, n, notAKnot=True, showSubspaces=True)
  fig.save(tightLayout=tightLayout, graphicsNumber=q+1)

def plotHierarchicalUniformBSplinesForFundamental(q):
  fig = Figure.create(figsize=(3.0, 3.9), scale=0.85)
  basis = helper.basis.HierarchicalBSpline(p)
  for l in range(n+1):
    ax = fig.add_subplot(n+1, 1, l+1)
    plotSubspace(ax, basis, l, n)
  fig.save(tightLayout=tightLayout, graphicsNumber=q+1)

def plotHierarchicalFundamentalSplines(q):
  fig = Figure.create(figsize=(3.0, 3.9), scale=0.85)
  basis = helper.basis.HierarchicalFundamentalSpline(p)
  for l in range(n+1):
    ax = fig.add_subplot(n+1, 1, l+1)
    plotSubspace(ax, basis, l, n, superscript=r"p,\mathrm{fs}",
                 fundamental=True)
  fig.save(tightLayout=tightLayout, graphicsNumber=q+1)

def plotHierarchicalWeaklyFundamentalSplines(q):
  fig = Figure.create(figsize=(3.0, 3.9), scale=0.85)
  basis = helper.basis.HierarchicalWeaklyFundamentalSpline(p)
  for l in range(n+1):
    ax = fig.add_subplot(n+1, 1, l+1)
    plotSubspace(ax, basis, l, n, superscript=r"p,\mathrm{wfs}")
  myTightLayout = dict(tightLayout)
  myTightLayout["h_pad"] = 0.5
  fig.save(tightLayout=myTightLayout, graphicsNumber=q+1)



def callMethod(qAndMethod):
  q, method = qAndMethod
  method(q)

def main():
  methods = [
    plotHierarchicalHatFunctions,
    plotNodalUniformBSplines,
    plotHierarchicalUniformBSplines,
    plotHierarchicalUniformBSplinesWithD,
    plotNodalNotAKnotBSplines,
    plotHierarchicalNotAKnotBSplines,
    plotHierarchicalUniformBSplinesForFundamental,
    plotHierarchicalFundamentalSplines,
    plotHierarchicalWeaklyFundamentalSplines,
  ]
  
  with multiprocessing.Pool() as pool:
    pool.map(callMethod, enumerate(methods))



if __name__ == "__main__":
  n = 3
  p = 3
  tightLayout = {"h_pad" : 0, "pad" : 3}
  main()
