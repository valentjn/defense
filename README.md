# Julian Valentin's PhD Defense Talk

[![download](https://img.shields.io/badge/download-GitHub%20Releases-darkred)][gitHubReleases]
[![CC BY-SA 4.0 license](https://img.shields.io/badge/license-CC%20BY--SA%204.0-blue)][license]

This is the source code of the material of the defense talk of the PhD thesis of Julian Valentin.

The thesis is titled **B-Splines for Sparse Grids: Algorithms and Application to Higher-Dimensional Optimization**. It was submitted to the University of Stuttgart, Germany, and it was successfully defended on April 2, 2019.

The code is provided here as is, without any further support or warranty. The material of the defense talk and the thesis are Copyright © 2019 Julian Valentin. Both are licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)][license].

## Download

The material of the defense talk can be downloaded on the [GitHub Releases page][gitHubReleases]. The PhD thesis itself can be downloaded at [arXiv][arxiv].

## Details

The material of the defense talk consists of the following components:

- Slides as PDF (as a whole and split into two parts): These are the slides that are shown on the screen.
- “Handout” as PDF: This is not an actual handout, but the slides compiled in Beamer's `handout` mode. This can be used by the presenter for handwritten notes during the presentation.
- Movie as MKV: This movie summarizes the talk as an anaglyph 3D movie, as is shown between the two parts of the slides.
- Flyer as PDF: This is the actual handout, printed on A4 paper and folded twice.

Before the talk, each member of the audience is given one flyer and one pair of cardboard anaglyph 3D glasses. Both are supposed to be taken home.

It is recommended to use [Impressive](http://impressive.sourceforge.net/) for the presentation, as Impressive can smoothly switch between slides and movie. For suitable command-line arguments, see the `SConstruct` file in the root directory.

Building the material from scratch is currently not possible as essential data are missing (`data/` directory).

## How to Cite

This section applies if you want to cite the thesis in a scientific paper, in a blog, or in any other kind of publication. Please only cite the thesis, not the defense talk.

Cite the thesis as follows:

> Julian Valentin: B-Splines for Sparse Grids: Algorithms and Application to Higher-Dimensional Optimization. PhD thesis, University of Stuttgart, Germany, 2019. Available at `arXiv:1910.05379 [math.NA]`. DOI: `10.18419/opus-10504`.

```biblatex
@phdthesis{Valentin2019,
  author      = {Valentin, Julian},
  title       = {B-Splines for Sparse Grids: Algorithms and Application to Higher-Dimensional Optimization},
  institution = {University of Stuttgart, Germany},
  year        = {2019},
  eprint      = {1910.05379},
  eprinttype  = {arxiv},
  eprintclass = {math.NA},
  doi         = {10.18419/opus-10504}
}
```

## How to Attribute

This section applies if you want to share the slides or the thesis, even in modified form (“Adapted Material” in terms of the license). Examples include:

- Distribution of the source code or compiled PDFs.
- Distribution of an excerpt, e.g., a figure.
- Distribution of printouts, e.g., as books.
- Translation into other languages.
- Compilation of the source code to different formats, e.g., to PDF via pdfL<sup>A</sup>T<sub>E</sub>X.

This applies to source code and compiled documents (e.g., PDF), as a whole and to parts thereof such as text, figures, tables, other components, or source code snippets.

Per the [license][license], you must at least do the following:

- Attribute the author and reproduce the copyright notice: Copyright © 2019 Julian Valentin
- Link to the license: [licensed under CC BY-SA 4.0][license]
- Link to the thesis: [https://arxiv.org/abs/1910.05379][arxiv]
- List modifications, if any

Modified versions must be licensed under the CC BY-SA 4.0 license as well (share alike), or a compatible license.

[arxiv]: https://arxiv.org/abs/1910.05379
[gitHubReleases]: https://github.com/valentjn/defense/releases
[license]: https://creativecommons.org/licenses/by-sa/4.0/
