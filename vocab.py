#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Inverted Word Index by Alphabets
"""

###############################################################################

import os
import json
import pickle
from collections import defaultdict

import networkx as nx

###############################################################################

WORD_LENGTH = 5
WORDS_FILE = "vocabulary.txt"
VOCAB_CACHE = "vocabulary.json"
INDEX_CACHE = "index.pickle"

###############################################################################


class Vocabulary:
    def __init__(
        self,
        words_file=WORDS_FILE,
        word_length=WORD_LENGTH,
        vocab_cache=VOCAB_CACHE,
        index_cache=INDEX_CACHE
    ):
        self.word_length = word_length
        self.words_file = words_file
        self.vocab_cache = vocab_cache
        self.index_cache = index_cache
        self.vocab_graph = nx.DiGraph()

        self.build_vocabulary()      # creates self.vocab
        self.build_index()           # creates self.index
        self.build_graph()

        self.frequency = {
            k: {
                k1: len(v1)
                for k1, v1 in v.items()
            }
            for k, v in self.index.items()
        }

        # self.score = {
        #     word: self.coverage(word) for word in self.vocab
        # }

    def build_vocabulary(self, use_cache=True):
        if use_cache and os.path.isfile(self.vocab_cache):
            with open(self.vocab_cache, encoding="utf-8") as f:
                self.vocab = json.load(f)
        else:
            with open(self.words_file, encoding="utf-8") as f:
                self.vocab = {
                    word.strip(): self.word_length
                    for word in f.read().split()
                    if len(word.strip()) == self.word_length
                }
            with open(self.vocab_cache, mode="w", encoding="utf-8") as f:
                json.dump(self.vocab, f, indent=2)

        return True

    def build_index(self, use_cache=True):
        if use_cache and os.path.isfile(self.index_cache):
            with open(self.index_cache, mode="rb") as f:
                self.index = pickle.load(f)
        else:
            self.index = {
                'letter': defaultdict(dict),
                'letter_position': defaultdict(dict)
            }

            for word in self.vocab:
                letter_position = [
                    f"{ltr}{pos}"
                    for ltr, pos in zip(word, range(self.word_length))
                ]
                letters = set(word)
                unique_letters = len(letters)
                for letter in letters:
                    self.index['letter'][letter][word] = unique_letters

                for l_p in letter_position:
                    self.index['letter_position'][l_p][word] = unique_letters

            with open(self.index_cache, mode="wb") as f:
                pickle.dump(self.index, f)

            return True

    def build_graph(self):
        for letter, words in self.index['letter'].items():
            for word in words:
                self.vocab_graph.add_edge(letter, word)

    def is_word(self, text):
        return text in self.vocab

    def coverage(self, word):
        node_boundary = nx.algorithms.boundary.node_boundary(
            self.vocab_graph, set(word)
        )
        return len(node_boundary) / len(self.vocab) * 100


###############################################################################


if __name__ == '__main__':
    vocab = Vocabulary()

###############################################################################
