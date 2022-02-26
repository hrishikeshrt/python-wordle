#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wordle Settings
"""

###############################################################################

from pathlib import Path

###############################################################################

WORD_LENGTH = 5
MAXIMUM_ATTEMPTS = 6

###############################################################################

BASE_DIR = Path(__file__).resolve().parent

DEFAULT_DIR = BASE_DIR / "default"
CUSTOM_DIR = BASE_DIR / "custom"
WORDS_FILENAME = "vocabulary.txt"

DATA_DIR = (
    CUSTOM_DIR
    if (CUSTOM_DIR / WORDS_FILENAME).exists()
    else DEFAULT_DIR
)

###############################################################################

WORDS_FILE = DATA_DIR / WORDS_FILENAME
VOCAB_CACHE = DATA_DIR / "vocabulary.json"
INDEX_CACHE = DATA_DIR / "index.json"

COVERAGE_CACHE = DATA_DIR / "coverage.json"
EVALUATION_FILE = DATA_DIR / "evaluation.json"

###############################################################################
