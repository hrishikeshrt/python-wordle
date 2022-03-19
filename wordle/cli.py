#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI for Wordle"""

import sys
import logging

from .wordle import Wordle
from .solver import WordleSolver
from .defaults import MAXIMUM_ATTEMPTS

###############################################################################

ROOT_LOGGER = logging.getLogger()
ROOT_LOGGER.hasHandlers() or ROOT_LOGGER.addHandler(logging.StreamHandler())

###############################################################################


def main():
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
    parser.add_argument(
        "--helper",
        action="store_true",
        help="Take help from WordleSolver for a Wordle in a different platform"
    )
    args = vars(parser.parse_args())

    if args.get("random"):
        wordle = Wordle(seed=None, display=True)
    elif args.get("seed"):
        wordle = Wordle(seed=args.get("seed"), display=True)
    else:
        wordle = Wordle(display=True)

    if args.get("helper"):
        description = [
            "Helper Mode",
            "===========",
            "",
            "* Suggestions for words will be provided at each step.",
            "* You may choose a word and obtain result.",
            "* Enter the obtained result as a ternary string, ",
            "  i.e., a string made of 0, 1, and 2.",
            "  - 0 : (grey)   : an incorrect letter.",
            "  - 1 : (yellow) : a correct letter in wrong position.",
            "  - 2 : (green)  : a correct letter in correct position.",
            ("  e.g., if the third letter turned green"
             " and fifth letter turned yellow in the third party Wordle,"
             " then you should input 00201 as the result obtained."),
            "",
            "Happy Wordling!"
        ]
        print("\n".join(description))
        solver = WordleSolver(None)
        while solver.num_attempts < MAXIMUM_ATTEMPTS:
            print(f"\nAttempt {solver.num_attempts + 1}\n=========\n")
            if len(solver.valid_words) < 10:
                print(f"Valid Words: {solver.valid_words}")

                if len(solver.valid_words) == 1:
                    print("\nCongratulations!")
                    print(f"Solution: {solver.valid_words[0]}")
                    break

            print(f"Suggestions: {solver.best_options()[:5]}")
            _word = ""
            while not _word.strip():
                _word = input("Chosen word: ")

            _result = ""
            while not _result.strip():
                _result = input("Obtained result: ")

            if _result.strip() == "22222":
                print("\nCongratulations!")
                print(f"Solution: {_word}")
                break

            result = zip(_word.strip(), map(int, _result.strip()))
            solver.handle_result(result)
    elif args.get("solve"):
        solver = WordleSolver(wordle)
        solver.solve()
    else:
        wordle.show()
        while not wordle.solved and not wordle.failed:
            guess = ""
            while not guess.strip():
                guess = input("Guess: ")
            wordle.guess(guess)

    if args.get("random") and wordle.failed:
        wordle.message(f"The word was '{wordle.word}'.")

    return 0


###############################################################################


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
