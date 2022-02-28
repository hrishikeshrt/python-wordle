#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evaluate Solver

@author: Hrishikesh Terdalkar
"""

###############################################################################

import json

from tqdm import tqdm
from numpy import average

from .vocab import Vocabulary
from .wordle import Wordle
from .solver import WordleSolver
from .defaults import EVALUATION_FILE

###############################################################################


def run_solver_on_all_words():
    result = {'status': {}}

    for v in tqdm(Vocabulary().vocab):
        s = WordleSolver(Wordle(word=v))
        s.solve()
        result['status'][v] = (s.wordle.solved, s.wordle.num_attempts)

        EVALUATION_FILE.write_text(json.dumps(result))

    return result


def analyse_solver():
    if EVALUATION_FILE.exists():
        result = json.loads(EVALUATION_FILE.read_text())
    else:
        result = run_solver_on_all_words()

    success = []
    success_in_number_of_attempts = []
    failure = []

    for word, (status, attempts) in result['status'].items():
        if status:
            success.append(word)
            success_in_number_of_attempts.append(attempts)
        else:
            failure.append(word)

    total_count = len(result['status'])
    success_count = len(success)
    failure_count = len(failure)
    success_rate = success_count / total_count * 100

    performance = {}
    performance['total_count'] = total_count
    performance['success_count'] = success_count
    performance['failure_count'] = failure_count
    performance['success_rate'] = success_rate
    performance['average_attempts'] = average(success_in_number_of_attempts)
    result['performance'] = performance

    EVALUATION_FILE.write_text(json.dumps(result))

    return performance

###############################################################################


if __name__ == "__main__":
    print(json.dumps(analyse_solver(), indent=2))

###############################################################################
