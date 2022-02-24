#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wordle for Python"""

from collections import defaultdict
import datetime

import numpy as np
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel

from vocab import Vocabulary

###############################################################################


class Wordle:
    def __init__(self, max_attempts=6, seed=None):
        self.vocabulary = Vocabulary()
        self.console = Console()

        if seed is None:
            today = datetime.date.today()
            seed = today.year * 10000 + today.month * 100 + today.day

        np.random.seed(seed)
        self.word = np.random.choice(list(self.vocabulary.vocab))
        self.letter_position = defaultdict(set)
        for position, letter in enumerate(self.word):
            self.letter_position[letter].add(position)

        self.max_attempts = max_attempts
        self.num_attempts = 0

        self.attempts = tuple([
            [(" ", -1)] * self.vocabulary.word_length
            for _ in range(max_attempts)
        ])
        self.alphabet = {chr(i): -1 for i in range(97, 123)}
        self.solved = False
        self.failed = False

    def message(self, msg, style="bold yellow"):
        self.console.print(Panel(msg), justify="center", style=style)

    def guess(self, word):
        word = word.lower()
        if self.num_attempts == self.max_attempts:
            self.message("No more attempts left.", style="bold red")
        elif self.solved:
            self.message("Wordle is already solved!")
        elif not self.vocabulary.is_word(word):
            self.message(f"'{word}' is not a valid word.", style="bold red")
        else:
            result = []
            total_score = 0
            for position, letter in enumerate(word):
                score = sum([
                    letter in self.letter_position,
                    position in self.letter_position.get(letter, set())
                ])
                result.append((letter, score))
                self.alphabet[letter] = score
                total_score += score

            if total_score == 2 * len(word):
                self.solved = True
                self.message("Congratulations!", style="bold green")

            if result in self.attempts:
                self.message(f"Already attempted '{word}'.")
            else:
                self.attempts[self.num_attempts].clear()
                self.attempts[self.num_attempts].extend(result)
                self.num_attempts += 1

            if self.num_attempts == self.max_attempts:
                self.failed = True
                self.message("Oops.. No more attempts left!", style="bold red")

        self.show()

    def show(self, style=None):
        if style is None:
            style = {
                -1: "bold white underline",
                0: "bold black underline",
                1: "bold yellow underline",
                2: "bold green underline"
            }

        attempts_display = []
        for attempt in list(self.attempts):
            attempts_display.append(" ".join([
                f"[{style[score]}]{letter.upper()}[/{style[score]}]"
                for letter, score in attempt
            ]))

        alphabet_display = " ".join([
            f"[{style[score]}]{letter.upper()}[/{style[score]}]"
            for letter, score in self.alphabet.items()
        ])

        self.console.print(
            Panel(
                Padding("\n".join(attempts_display), (1, 3)),
                style="on black"
            ),
            "\n",
            Panel(
                Padding(alphabet_display, (0, 1)),
                style="on black"
            ),
            justify="center"
        )

###############################################################################


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Wordle on your terminal")
    wordle = Wordle()

    wordle.show()
    while not wordle.solved and not wordle.failed:
        guess = input("Guess: ")
        wordle.guess(guess)
