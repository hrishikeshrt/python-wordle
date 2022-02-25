#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evaluate Solver

@author: Hrishikesh Terdalkar
"""

###############################################################################

import json
from pathlib import Path

from vocab import Vocabulary
from wordle import Wordle
from solver import WordleSolver
from tqdm import tqdm

###############################################################################

STATUS = {}

for v in tqdm(Vocabulary().vocab):
    s = WordleSolver(Wordle(word=v))
    s.solve()
    STATUS[v] = (s.wordle.solved, s.wordle.num_attempts)

    Path("evaluation.json").write_text(json.dumps(STATUS, indent=2))

###############################################################################
