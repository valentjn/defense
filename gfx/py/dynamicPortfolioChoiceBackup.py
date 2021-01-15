#!/usr/bin/python3
# number of output figures = 2

import matplotlib as mpl
#import mpl_toolkits.mplot3d.art3d
import numpy as np
import scipy.interpolate

from helper.figure import Figure
import helper.plot



def plotFigure1():
  largeMargin = 0.5
  smallMargin = 0
  largeArrowWidth = 0.4
  smallArrowWidth = 0.2
  barWidth = 0.5
  barHeight = 1.8
  axisMarginX = 0.1
  axisMarginY = 0.1
  #choices = [
  #  1.0 * np.array([3, 2, 1.5, 1.5]),
  #  1.0 * np.array([3.1, 2.5, 2.0, 1.0]),
  #  0.24 * np.array([3.1, 2.5, 2.0, 1.0]),
  #  1.0 * np.array([0, 0, 0, 1.0]),
  #]
  choices = [
    1.0 * np.array([2.8, 0.5]),
    1.0 * np.array([3.05, 0.6]),
    0.52 * np.array([3.1, 1.0]),
    1.0 * np.array([0, 1.0]),
  ]
  T = len(choices)
  
  fig = Figure.create(figsize=(1.8, 2.4), scale=1.35, preamble=r"""
\contourlength{1pt}
  """)
  ax = fig.gca()
  
  x = 0
  
  for t in range(T):
    choice1, choice2 = choices[t], choices[(t+1)%T]
    c = np.sum(choices[0])
    choice1 *= barHeight / c
    choice2 *= barHeight / c
    choice1CumSum = np.hstack(([0], np.cumsum(choice1)))
    choice2CumSum = np.hstack(([0], np.cumsum(choice2)))
    tStr = (("T" if t == T-1 else "t+{}".format(t)) if t > 0 else "t")
    
    rectArgs = {"clip_on" : False, "ec" : "k"}
    #colors = ["C1", "C2", "C4", "C7"]
    colors = ["C1", "C2"]
    #labels = [r"$\bond_{{{}}}$", r"$\stock_{{{},1}}$",
    #          r"$\stock_{{{},2}}$", r"$\consume_{{{}}}$"]
    labels = [r"$\bond\smash{{_{{{}}}}}$", r"$\consume\smash{{_{{{}}}}}$"]
    contour = lambda x, c: r"\contour{{{}!60}}{{{}}}".format(c, x)
    
    y = choice1CumSum[-1]
    ax.add_artist(mpl.patches.Rectangle(
        (0, x), y, barWidth, **rectArgs))
    ax.text(y/2, x+barWidth/2,
            contour(r"$\wealth\smash{{_{{{}}}}}$".format(tStr), "C0"),
            ha="center", va="center")
    
    x += barWidth + smallMargin
    
    if t == T - 2:
      ax.plot([-axisMarginY-0.04, -axisMarginY+0.04],
              2 * [x-barWidth/2], "k-", clip_on=False)
      ax.text(-axisMarginY-0.08, x-barWidth/2, "${}$".format(tStr),
              ha="right", va="center")
      ax.text(choice2CumSum[-1]/2, x+largeMargin, r"$\vdots$",
              ha="center", va="center")
      ax.text(-axisMarginY-0.15, x+largeMargin, r"$\vdots$",
              ha="center", va="center")
      x += 2 * largeMargin
      continue
    
    for y1, y2, label, color in zip(
          choice1CumSum[:-1], choice1CumSum[1:], labels, colors):
      if y2 - y1 > 0:
        ax.add_artist(mpl.patches.Rectangle(
            (y1, x), y2 - y1, barWidth, fc=color, **rectArgs))
        ax.text((y1+y2)/2, x+barWidth/2, contour(label.format(tStr), color),
                ha="center", va="center")
    
    ax.plot([-axisMarginY-0.04, -axisMarginY+0.04],
            2 * [x-smallMargin/2], "k-", clip_on=False)
    ax.text(-axisMarginY-0.08, x-smallMargin/2, "${}$".format(tStr),
            ha="right", va="center")
    
    y = barHeight
    helper.plot.plotArrow(ax, [y2+0.1, x+barWidth/2],
                          [y2+0.35, x+barWidth/2])
    ax.text(y2+0.4, x+barWidth/2,
            r"$\utilityfun(\consume_{{{}}})$".format(tStr),
            ha="left", va="center")
    
    if t == T - 1:
      x += barWidth
      continue
    
    for y in [0, barHeight]:
      ax.plot([y, y], [x - smallMargin, x], "k--", clip_on=False)
    
    x += barWidth + largeMargin
    
    ax.plot([0, 0], [x - largeMargin, x], "k--", clip_on=False)
    ax.plot([choice1CumSum[-2], choice2CumSum[-1]], [x - largeMargin, x],
            "k--", clip_on=False)
    
    left = np.array([x - largeMargin, choice1CumSum[-2]/2])
    right = np.array([x, choice2CumSum[-1]/2])
    direction = right - left
    t = largeArrowWidth / largeMargin
    left  += (1-t)/2 * direction
    right -= (1-t)/2 * direction
    helper.plot.plotArrow(ax, left[::-1], right[::-1])
    
    for y in [0, choice2CumSum[-1]]:
      ax.plot([y, y], [x - smallMargin, x], "k--", clip_on=False)
  
  x += axisMarginX + 0.05
  helper.plot.plotArrow(ax, [-axisMarginY, -axisMarginX], [-axisMarginY, x])
  
  ax.set_aspect("equal")
  ax.set_xlim(-0.1, barHeight+0.1)
  ax.set_ylim(0, x)
  ax.set_axis_off()
  
  fig.save()



def plotSlice(ax, origin, funPoints, lineStyle, tStr):
  depth = 4
  height = 2
  
  fun = scipy.interpolate.lagrange(*zip(*funPoints))
  tt = np.linspace(0, 1, 129)
  ff = np.clip(fun(tt), 0, 1)
  ax.plot(np.full_like(tt, origin[0]), origin[1] + depth * tt, lineStyle,
          zs=origin[2] + height * ff, color="C0")
  
  if lineStyle == "-":
    iMax = np.argmax(ff)
    tMax, fMax = tt[iMax], ff[iMax]
    x, y, z = origin[0], origin[1] + depth * tMax, origin[2] + height * fMax
    pMax = [x, y, z]
    ax.plot([x], [y], ".", zs=[z], color="C0")
  
  x = 5 * [origin[0]]
  y = origin[1] + depth * np.array([0, 1, 1, 0, 0])
  z = origin[2] + height * np.array([0, 0, 1, 1, 0])
  ax.plot(x, y, "k-", zs=z)
  #ax.add_collection3d(mpl_toolkits.mplot3d.art3d.Poly3DCollection(
  #    [np.array([x, y, z]).T], facecolors=["w"]))
  
  #ax.text(origin[0], origin[1] + depth, origin[2] - 0.2,
  #        r"$\policy_{{{}}}$".format(tStr), ha="left", va="top")
  
  return (pMax if lineStyle == "-" else None)

def plotFigure2():
  fig = Figure.create(figsize=(5, 3))
  ax = fig.gca(projection="3d")
  
  for t in [0, 1]:
    tStr = ("t" if t == 0 else "t+1")
    z = 4*t
    origins = [[0, 0, z], [2, 0, z], [4, 0, z]]
    funPointss = [
      [[0.1, 0.2], [0.4, 0.3], [0.6, 0.6], [0.9, 0.4]],
      [[0.1, 0.2], [0.4, 0.3], [0.6, 0.4], [0.9, 0.2]],
      [[0.1, 0.1], [0.4, 0.4], [0.6, 0.6], [0.9, 0.2]],
    ]
    lineStyle = (":" if t == 0 else "-")
    pMaxs = []
    
    for k, (origin, funPoints) in enumerate(zip(origins, funPointss)):
      pMax = plotSlice(ax, origin, funPoints, lineStyle, tStr)
      pMaxs.append(pMax)
      ax.plot(2*[origin[0]], 2*[origin[1]], "k-",
              zs=[origin[2]-0.2,origin[2]])
      ax.text(origin[0] - 0.1, origin[1], origin[2] - 0.25,
              r"$\state_{{{}}}^{{({})}}$".format(tStr, k+1),
              ha="left", va="top")
    
    if t == 1:
      pMaxs = np.array(pMaxs)
      ax.plot(pMaxs[:,0], pMaxs[:,1], "k--", zs=pMaxs[:,2])
    
    ax.plot([-0.1, 5.5], [0, 0], "k-", zs=[z, z])
    ax.text(5.7, 0, z, r"$\state_{{{}}}$".format(tStr),
            ha="left", va="center")
  
  ax.set_proj_type("ortho")
  ax.set_axis_off()
  ax.view_init(10, -70)
  ax.set_xlim(0, 4)
  ax.set_ylim(0, 4)
  ax.set_zlim(0, 6)
  
  fig.save()



def main():
  plotFigure1()
  plotFigure2()



if __name__ == "__main__":
  main()
