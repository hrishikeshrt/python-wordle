#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wordle Defaults"""

###############################################################################

from pathlib import Path

###############################################################################

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
WORD_LENGTH = 5
MAXIMUM_ATTEMPTS = 6

###############################################################################

BASE_DIR = Path(__file__).resolve().parent

###############################################################################

DATA_DIR = BASE_DIR / "data"

WORDS_FILE = DATA_DIR / "vocabulary.txt"

VOCAB_CACHE = DATA_DIR / "vocabulary.json"
INDEX_CACHE = DATA_DIR / "index.json"
COVERAGE_CACHE = DATA_DIR / "coverage.json"

EVALUATION_FILE = DATA_DIR / "evaluation.json"

###############################################################################
