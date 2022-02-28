#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wordle Vocabulary"""

###############################################################################

import json
from pathlib import Path
from collections import defaultdict
from typing import Iterable

from .defaults import (
    ALPHABET,
    WORD_LENGTH,
    WORDS_FILE,
    VOCAB_CACHE,
    INDEX_CACHE
)

###############################################################################


class Vocabulary:
    def __init__(
        self,
        alphabet: Iterable = ALPHABET,
        words_file: str or Path = WORDS_FILE,
        word_length: int = WORD_LENGTH,
        vocab_cache: str or Path = VOCAB_CACHE,
        index_cache: str or Path = INDEX_CACHE
    ):
        self.alphabet = set(alphabet)
        self.word_length = word_length
        self.words_file = Path(words_file)
        self.vocab_cache = Path(vocab_cache)
        self.index_cache = Path(index_cache)

        self.build_vocabulary()      # creates self.vocab
        self.build_index()           # creates self.index

        self.frequency = {
            k: {
                k1: len(v1)
                for k1, v1 in v.items()
            }
            for k, v in self.index.items()
        }

    def build_vocabulary(self, use_cache=True):
        if use_cache and self.vocab_cache.is_file():
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
        if use_cache and self.index_cache.is_file():
            with open(self.index_cache, mode="r") as f:
                self.index = json.load(f)
        else:
            self.index = {
                "letter": defaultdict(dict),
                "letter_position": defaultdict(dict)
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

            with open(self.index_cache, mode="w") as f:
                json.dump(self.index, f)

            return True

    def is_word(self, text):
        return text in self.vocab

###############################################################################


if __name__ == '__main__':
    vocab = Vocabulary()

###############################################################################
