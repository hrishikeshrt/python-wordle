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

## Usage:

```console
usage: cli.py [-h] [--random] [--seed SEED] [--solve]

Wordle on your terminal

optional arguments:
  -h, --help   show this help message and exit
  --random     Show a random Wordle
  --seed SEED  Seed the RNG
  --solve      Simulate WordleSolver
```
## Solver

```
valid words at any given point := words from vocabulary that are possible solutions to the Wordle at that point
```

```
coverage of a word := percentage of valid words that contain at least one letter from the word
```

Solver roughly uses the following strategy,

* Guess a word with highest coverage.
* After each guess, eliminate words based on the clues, e.g.,
    * Remove all words that contain an `incorrect-letter`
    * Remove all words that do not contain the identified `(correct-letter, correct-position)` combinations
    * Remove all words that contain the identified `(correct-letter, incorrect-position)` combinations
    * Remove all words that do not contain a `correct-letter`
    * Re-calculate coverage and guess again
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
