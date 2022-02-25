#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI for Wordle

@author: Hrishikesh Terdalkar
"""

import logging

from wordle import Wordle
from solver import WordleSolver

###############################################################################

LOGGER = logging.getLogger()
LOGGER.hasHandlers() or LOGGER.addHandler(logging.StreamHandler())

###############################################################################

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Wordle on your terminal")
    parser.add_argument(
        "--random",
        action="store_true",
        help="Show a random Wordle"
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Seed the RNG"
    )
    parser.add_argument(
        "--solve",
        action="store_true",
        help="Simulate WordleSolver"
    )
    args = vars(parser.parse_args())

    if args.get("random"):
        wordle = Wordle(seed=None, display=True)
    elif args.get("seed"):
        wordle = Wordle(seed=args.get("seed"), display=True)
    else:
        wordle = Wordle(display=True)

    if args.get("solve"):
        solver = WordleSolver(wordle)
        solver.solve()
    else:
        wordle.show()
        while not wordle.solved and not wordle.failed:
            guess = input("Guess: ")
            wordle.guess(guess)

    if args.get("random") and wordle.failed:
        wordle.message(f"The word was '{wordle.word}'.")
