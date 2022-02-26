#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evaluate Solver

@author: Hrishikesh Terdalkar
"""

###############################################################################

import json
from pathlib import Path

from tqdm import tqdm

from vocab import Vocabulary
from wordle import Wordle
from solver import WordleSolver

###############################################################################

EVALUATION_FILE = Path("evaluation.json")

###############################################################################


def run_solver_on_all_words():
    result = {'status': {}}

    for v in tqdm(Vocabulary().vocab):
        s = WordleSolver(Wordle(word=v))
        s.solve()
        result['status'][v] = (s.wordle.solved, s.wordle.num_attempts)

        EVALUATION_FILE.write_text(json.dumps(result))

    return result


###############################################################################
