#!/usr/bin/python3
# number of output figures = 1

import matplotlib
import numpy as np
import scipy.optimize

import helper.basis
from helper.figure import Figure



def main():
  ps = [3]
  xl = (-3.5, 3.5)
  yl = (-0.2, 1.1)
  
  gammas = []
  cutoffs = []
  betas = []
  betaTildes = []
  
  
  
  for p in ps:
    fundamentalSpline = helper.basis.FundamentalSpline(p)
    coeffs, cutoff, gamma = (fundamentalSpline.c, fundamentalSpline.cutoff,
                            fundamentalSpline.gamma)
    if p == 1: gamma = np.exp(1)
    gammas.append(gamma)
    cutoffs.append(cutoff)
    
    upperBound = lambda beta, x: beta * np.exp(-np.abs(x) * np.log(gamma))
    
    objFun = (
        lambda x: -np.abs(fundamentalSpline.evaluate(np.array([x]))[0]) /
        upperBound(1, x))
    result = scipy.optimize.minimize_scalar(objFun, bounds=(0, 1), method="bounded")
    beta = -result.fun
    betas.append(beta)
    
    if p == 1:
      cutoff = 6
      coeffs = np.hstack((np.zeros((5,)), coeffs, np.zeros((5,))))
    
    kk = np.array(range(-cutoff + 1, cutoff))
    betaTilde = np.max(np.abs(coeffs) / upperBound(1, kk))
    betaTildes.append(betaTilde)
    
    if p > 7: continue
    
    
    
    fig = Figure.create(figsize=(1.7, 1.7))
    ax1 = fig.gca()
    
    centralizedCardinalBSpline = helper.basis.CentralizedCardinalBSpline(p)
    brightness = 0.5
    color = [x + brightness * (1 - x)
            for x in matplotlib.colors.to_rgba("C0")[:3]]
    
    for k in range(-cutoff - (p+1)//2, cutoff + (p+1)//2 + 1):
      xx = np.linspace(max(-k-(p+1)//2, xl[0]), min(-k+(p+1)//2, xl[1]), 101)
      if xx[-1] <= xx[0]: continue
      print(xx[0], xx[-1])
      yy = centralizedCardinalBSpline.evaluate(xx + k)
      ax1.plot(xx, yy, "-", color=color, clip_on=False)
    
    #yy = upperBound(beta, xx)
    #ax1.plot(xx, yy, "-", color="C0")
    #ax1.plot(xx, yy, "--", color="C1", dashes=[4, 4])
    #ax1.plot(xx, -yy, "-", color="C0")
    #ax1.plot(xx, -yy, "--", color="C1", dashes=[4, 4])
    
    xx = np.linspace(*xl, 441)
    yy = fundamentalSpline.evaluate(xx)
    ax1.plot(xx, yy, "-", color="C0", lw=1.5, clip_on=False)
    
    x = np.linspace(np.ceil(xl[0]), 0, 1-int(np.ceil(xl[0])))[:-1]
    ax1.plot(x, np.zeros_like(x), "o", color="C0", mfc="none", clip_on=False)
    x = np.linspace(0, np.floor(xl[1]), np.floor(xl[1])+1)[1:]
    ax1.plot(x, np.zeros_like(x), "o", color="C0", mfc="none", clip_on=False)
    ax1.plot(0, 1, "o", color="C0", mfc="none", clip_on=False)
    
    ax1.set_xticks(range(-5, 6))
    ax1.set_xticklabels(["", "$-4$", "", "$-2$", "", "$0$", "", "$2$",
                         "", "$4$", ""])
    ax1.set_yticks([-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1, 1.2])
    ax1.set_yticklabels(["", "$0$", "", "", "", "", "$1$", ""])
    ax1.set_xlim(xl)
    ax1.set_ylim(yl)
    
    ax1.spines["bottom"].set_position("zero")
    
    """
    ax2 = ax1.twinx()
    ax2.plot(kk, coeffs, ".", color="C1")
    
    ax1.text(-5.1, 1.2, r"$\parentfundspl{p}(x),$",
            ha="left", va="center", color="C0")
    ax1.text(-2.6, 1.2, r"$\parentbspl{p\vphantom{,\fs}}(x - k)$",
            ha="left", va="center", color=color)
    ax1.text(-5.1, 1.05, r"$\pm\beta_p \cdot (\gamma_p)^{-|x|}$",
            ha="left", va="center", color="C0")
    ax1.text(5.1, 1.2, r"$\fundsplcoeff{k}{p}$",
            ha="right", va="center", color="C1")
    ax1.text(5.1, 1.05, r"$\pm\beta'_p \cdot (\gamma_p)^{-|k|}$",
            ha="right", va="center", color="C1")
    ax1.text(0, -0.2, r"\textcolor{C0}{$x$} or \textcolor{C1}{$k$}",
            ha="center", va="center")
    
    yl2 = np.array(yl) * betaTilde / beta
    yt2 = list(range(int(yl2[0]) - 1, int(yl2[1]) + 1))
    ax2.set_yticks(yt2)
    ytl2 = len(yt2) * [""]
    ytl2[yt2.index(0)] = r"$0$"
    ytl2[-1] = r"${}$".format(yt2[-1])
    ax2.set_yticklabels(ytl2)
    ax2.set_ylim(yl2)
    
    ax1.spines["left"].set_color("C0")
    ax1.tick_params(axis="y", colors="C0")
    ax1.spines["top"].set_visible(False)
    ax1.spines["bottom"].set_position("zero")
    ax2.spines["left"].set_visible(False)
    ax2.spines["right"].set_color("C1")
    ax2.tick_params(axis="y", colors="C1")
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    fig.save(hideSpines=False)
    """
    
    fig.save()
  
  
  
  formatFloat = (
      lambda x: "${{:.{:.0f}f}}$".format(3 - np.floor(np.log10(x))).
      format(x).replace(".0000", "").replace(".000", ""))
  print(r"\begin{tabular}")
  print(r"  \toprule")
  print(r"  $p$&" + "&".join(["${}$".format(p) for p in ps]) + r"\\")
  print(r"  \midrule")
  print(r"  $\gamma_p$&" +
        "&".join([formatFloat(x) for x in gammas]) + r"\\")
  print(r"  $\beta_p$&" +
        "&".join([formatFloat(x) for x in betas]) + r"\\")
  print(r"  $\beta'_p$&" +
        "&".join([formatFloat(x) for x in betaTildes]) + r"\\")
  print(r"  $\fundsplcutoff{p}$&" +
        "&".join(["${}$".format(x) for x in cutoffs]) + r"\\")
  print(r"  \bottomrule")
  print(r"\end{tabular}")



if __name__ == "__main__":
  main()
