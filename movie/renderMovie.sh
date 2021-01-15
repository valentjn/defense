#!/bin/bash

PYTHONPATH=$REAL_HOME/git/defense/movie:$REAL_HOME/git/thesis/py \
  nice -n 20 blender --python renderMovie.py --background
