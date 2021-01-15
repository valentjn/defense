#!/usr/bin/python3
# number of output figures = 3

import matplotlib as mpl
import numpy as np

from helper.figure import Figure
import helper.plot



def main():
  largeMargin = 1
  smallMargin = 0.4
  largeArrowWidth = 0.5
  smallArrowWidth = 0.2
  barWidth = 0.5
  barHeight = 1.8
  axisMarginX = 0.1
  axisMarginY = 0.1
  choice1 = np.array([3, 2, 1.5, 3.5])
  choice2 = np.array([3.1, 2.5, 2.0])
  
  
  
  for q in range(3):
    stateColor = ("r" if q == 1 else "k")
    controlColor = ("r" if q == 2 else "k")
    
    fig = Figure.create(figsize=(2.5, 1.7), scale=1.4, preamble=r"""
\usepackage{contour}
\contourlength{1pt}
    """)
    ax = fig.gca()
    
    c = np.sum(choice1)
    choice1 *= barHeight / c
    choice2 *= barHeight / c
    choice1CumSum = np.hstack(([0], np.cumsum(choice1)))
    choice2CumSum = np.hstack(([0], np.cumsum(choice2)))
    
    rectArgs = {"clip_on" : False, "ec" : "k"}
    colors = ["C1", "C2", "C4", "C7"]
    labels = [
      r"$\stock_{{{}}}^{{(1)}}$",
      r"$\stock_{{{}}}^{{(2)}}$",
      r"$\stock_{{{}}}^{{(3)}}$",
      r"$\consume_{{{}}}$",
    ]
    contour = lambda x, c: r"\contour{{{}!50}}{{{}}}".format(c, x)
    
    x = 0
    
    y = barHeight
    ax.add_artist(mpl.patches.Rectangle(
        (x, 0), barWidth, y, **rectArgs))
    ax.text(x+barWidth/2, y/2, contour(r"$\wealth_t$", "C0"),
            ha="center", va="center", color=stateColor)
    
    x += barWidth + smallMargin
    
    for y1, y2, label, color in zip(
          choice1CumSum[:-1], choice1CumSum[1:], labels, colors):
      ax.add_artist(mpl.patches.Rectangle(
          (x, y1), barWidth, y2 - y1, fc=color, **rectArgs))
      ax.text(x+barWidth/2, (y1+y2)/2, contour(label.format("t"), color),
              ha="center", va="center", color=controlColor)
    
    ax.plot(2 * [x-smallMargin/2],
            [-axisMarginY-0.04, -axisMarginY+0.04], "k-", clip_on=False)
    ax.text(x-smallMargin/2, -axisMarginY-0.08, "$t$", ha="center", va="top")
    
    y = barHeight
    helper.plot.plotArrow(ax, [x - smallMargin/2 - smallArrowWidth/2, y/2],
                          [x - smallMargin/2 + smallArrowWidth/2, y/2])
    helper.plot.plotArrow(ax, [x+barWidth+0.1, (y1+y2)/2],
                          [x+barWidth+0.3, (y1+y2)/2+0.25])
    ax.text(x+barWidth+0.35, (y1+y2)/2+0.25, r"$\utilityfun(\consume_t)$",
            ha="left", va="bottom")
    
    for y in [0, barHeight]:
      ax.plot([x - smallMargin, x], [y, y], "k--", clip_on=False)
    
    x += barWidth + largeMargin
    
    for y1, y2, label, color in zip(
          choice2CumSum[:-1], choice2CumSum[1:], labels, colors):
      ax.add_artist(mpl.patches.Rectangle(
          (x, y1), barWidth, y2 - y1, fc=color, **rectArgs))
      ax.text(x+barWidth/2, (y1+y2)/2, contour(label.format("t+1"), color),
              ha="center", va="center", color="k")
    
    for y1, y2 in zip(choice1CumSum[:-1], choice2CumSum):
      ax.plot([x - largeMargin, x], [y1, y2], "k--", clip_on=False)
    
    choice1Centers = (choice1CumSum[1:] + choice1CumSum[:-1]) / 2
    choice2Centers = (choice2CumSum[1:] + choice2CumSum[:-1]) / 2
    
    for y1, y2 in zip(choice1Centers[:-1], choice2Centers):
      left, right = np.array([x - largeMargin, y1]), np.array([x, y2])
      direction = right - left
      t = largeArrowWidth / largeMargin
      left  += (1-t)/2 * direction
      right -= (1-t)/2 * direction
      helper.plot.plotArrow(ax, left, right)
    
    x += barWidth + smallMargin
    
    y = choice2CumSum[-1]
    ax.add_artist(mpl.patches.Rectangle(
        (x, 0), barWidth, y, **rectArgs))
    ax.text(x+barWidth/2, y/2, contour(r"$\wealth_{t+1}$", "C0"),
            ha="center", va="center", color="k")
    helper.plot.plotArrow(ax, [x - smallMargin/2 - smallArrowWidth/2, y/2],
                          [x - smallMargin/2 + smallArrowWidth/2, y/2])
    ax.plot(2 * [x-smallMargin/2],
            [-axisMarginY-0.04, -axisMarginY+0.04], "k-", clip_on=False)
    ax.text(x-smallMargin/2, -axisMarginY-0.08, "$t+1$", ha="center", va="top")
    
    for y in [0, choice2CumSum[-1]]:
      ax.plot([x - smallMargin, x], [y, y], "k--", clip_on=False)
    
    x += barWidth
    
    helper.plot.plotArrow(ax, [-axisMarginX, -axisMarginY],
                          [x+axisMarginX, -axisMarginY])
    
    ax.set_aspect("equal")
    ax.set_xlim(0, x)
    ax.set_ylim(-0.1, barHeight+0.1)
    ax.set_axis_off()
    
    fig.save()



if __name__ == "__main__":
  main()
