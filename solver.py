#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wordle Solver

@author: Hrishikesh Terdalkar
"""

import os
import json
import logging
from collections import Counter
from functools import cached_property

import networkx as nx

from vocab import Vocabulary
from wordle import Wordle

###############################################################################

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

###############################################################################

COVERAGE_CACHE = "coverage.json"

###############################################################################


class WordleSolver:
    def __init__(
        self,
        wordle: Wordle = None,
        coverage_cache: str = COVERAGE_CACHE
    ):
        self.wordle = wordle
        self.vocabulary = Vocabulary()
        self.valid_words = set(self.vocabulary.vocab)
        self.num_attempts = 0
        self.guesses = {}

        self.known_letters = {}

        self.build_graph()

        if os.path.isfile(coverage_cache):
            with open(coverage_cache, mode="r") as f:
                self.coverage = json.load(f)
        else:
            with open(coverage_cache, mode="w") as f:
                json.dump(self.coverage, f, indent=2)

    def build_graph(self):
        self.graph = nx.DiGraph()
        self.markers = set()

        for source_dict in ['letter', 'letter_position']:
            for letter, words in self.vocabulary.index[source_dict].items():
                for word in words:
                    self.graph.add_edge(letter, word)
                    self.markers.add(letter)

    def calculate_coverage(self, letters):
        node_boundary = nx.algorithms.boundary.node_boundary(
            self.graph, set(letters)
        )
        graph_words_count = self.graph.number_of_nodes() - len(self.markers)
        return len(node_boundary) / graph_words_count * 100

    @cached_property
    def coverage(self):
        return {
            word: self.calculate_coverage(word)
            for word in self.vocabulary.vocab
        }

    def reset_coverage(self):
        if hasattr(self, 'coverage'):
            delattr(self, 'coverage')

    def eliminate(self, markers, words=None):
        # marker is one of the following,
        # - a letter, such as, 'a', 'e' etc.
        # - a letter_position, such as, 'e3', 'a1' etc.
        remove_words = words or set()
        for marker in markers:
            for source_dict in ['letter', 'letter_position']:
                for word in self.vocabulary.index[source_dict].get(marker, []):
                    remove_words.add(word)

        self.graph.remove_nodes_from(remove_words)
        count_before = len(self.valid_words)
        self.valid_words -= remove_words
        count_after = len(self.valid_words)

        LOGGER.info(f"Eliminated {count_before - count_after} options.")
        self.reset_coverage()

    def top_coverage(
        self,
        n: int = None,
        avoid_set: set = None,
        coverage_min: int = 0,
        coverage_max: int = 100
    ):
        if avoid_set is None:
            avoid_set = set()

        return Counter({
            k: v for k, v in self.coverage.items()
            if (
                not set(k).intersection(avoid_set)
                and coverage_min < v < coverage_max
            )
        }).most_common(n)

    def best_options(self):
        coverage_threshold = 50

        # if less valid words than number of attempts left
        # just guess them all
        attempts_left = self.wordle.max_attempts - self.wordle.num_attempts
        choose_from_valid_words = len(self.valid_words) <= attempts_left
        if choose_from_valid_words:
            return self.options_from_valid_words()

        avoid_set = {
            k
            for k, v in self.known_letters.items()
            if isinstance(v, int)
        }

        options = self.top_coverage(n=100, avoid_set=avoid_set)
        multiple_best_options = [
            option
            for option in options
            if option[1] == options[0][1]
        ]

        pruned_options = []
        for option in multiple_best_options:
            _word, _coverage = option
            if _word in self.guesses:
                continue

            for _position, _letter in enumerate(_word):
                if isinstance(self.known_letters.get(_letter), set):
                    if -_position in self.known_letters[_letter]:
                        break
            else:
                pruned_options.append(option)

        if not pruned_options or pruned_options[0][1] < coverage_threshold:
            return self.options_from_valid_words()
        else:
            return pruned_options

    def options_from_valid_words(self):
        return sorted([
            (word, self.calculate_coverage(word))
            for word in self.valid_words
            if word not in self.guesses
        ], key=lambda x: x[1], reverse=True)

    def handle_result(self, result):
        if not result:
            return

        self.num_attempts += 1
        eliminate_markers = set()
        remove_words = set()
        for idx, (letter, score) in enumerate(result):
            if score == 0:
                eliminate_markers.add(letter)
            if score == 1:
                if letter not in self.known_letters:
                    self.known_letters[letter] = set()
                if isinstance(self.known_letters[letter], set):
                    self.known_letters[letter].add(-idx)

                eliminate_markers.add(f"{letter}{idx}")
                for word in self.valid_words:
                    if letter not in word:
                        remove_words.add(word)
            if score == 2:
                self.known_letters[letter] = idx
                for other_letter in self.vocabulary.alphabet:
                    if other_letter != letter:
                        eliminate_markers.add(f"{other_letter}{idx}")
        self.eliminate(eliminate_markers, words=remove_words)

    def guess(self, option=None):
        if self.wordle is None:
            LOGGER.error("No Wordle is defined.")
            return False

        if option is None:
            options = self.best_options()
            option, coverage = options[0]
        else:
            coverage = self.calculate_coverage(option)

        LOGGER.info(f"Guessing '{option}' (Coverage: {coverage})")
        result = self.wordle.guess(option)

        if result:
            self.handle_result(result)
            if self.wordle.solved:
                LOGGER.info(f"Solved in {self.num_attempts} attempts.")

    def solve(self):
        if self.wordle is None:
            LOGGER.error("No Wordle is defined.")
            return False

        while not self.wordle.solved and not self.wordle.failed:
            self.guess()
