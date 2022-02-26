# Wordle

## Setup

```console
$ pip install -r requirements.txt
```
## Quickstart

Start playing Wordle

```console
$ python cli.py
```

## Usage

```console
usage: cli.py [-h] [--random] [--seed SEED] [--solve]

Wordle on your terminal

optional arguments:
  -h, --help   show this help message and exit
  --random     Show a random Wordle
  --seed SEED  Seed the RNG
  --solve      Simulate WordleSolver
```

## Terminology

All of the following terms are valid in the context of a specific Wordle.

* A set of **known letters** is a set of letters which are known to be present in the Wordle's word based on clues obtained from the previous attempts.
* A set of **valid words** at any given point refers to a set of words from vocabulary that are possible solutions to the Wordle at that point based on the clues obtained till then.
* A letter is said to **cover** a word if the letter belongs to that word.
* **Coverage** *(absolute)* of a word refers to the percentage of valid words (at that point) covered by the letters in that word.
* **Coverage** *(relative)* of a word refers to the percentage of valid words (at that point) covered by the set of

## Solver

The Solver roughly uses the following strategy,

* Guess a word with highest (relative) coverage.
* After each guess, eliminate words based on the clues, e.g.,
    * Remove all words that contain an `incorrect-letter`
    * Remove all words that do not contain the identified `(correct-letter, correct-position)` combinations
    * Remove all words that contain the identified `(correct-letter, incorrect-position)` combinations
    * Remove all words that do not contain a `correct-letter`
    * Re-calculate (relative) coverage and guess again
* If at any point, number of valid words drops below number of attempts left, guess the valid words one-by-one.
* Additionally, there are heuristics to choose a word if multiple words with best coverage-score exist.

## Evaluation

Solver has been evaluated on the entire vocabulary.

### Setup

* Word Size: 5
* Vocabulary Size: 15918
* Maximum Attempts: 6

### Performance

* Success Count: 15263
* Success Rate: 95.89
* Average Attempts: 4.61
