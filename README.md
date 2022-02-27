# Wordle in Python

Game, Solver and Helper!

## Features

* Comprehensive CLI Application
    * Play Wordle in your terminal!
    * Let the solver play it out for you!
    * Use the helper mode for solving Wordles provided by other platforms!
* New Wordle every day. 
    * **Disclaimer**: This has nothing to do with the NYTimes Wordle.
* Play more using `--random` option.
* Reproducible random Wordle by specifying `--seed`.
* `WordleSolver()` class for solving Wordle.
* `--solve` option to let `WordleSolver()` do its work in front of your eyes!
* `--helper` option to actiave the helper mode for help with solving Wordles provided by other platforms.

## Setup

Install the requirements by typing the following command,

```console
$ pip install -r requirements.txt
```
## Quickstart

Start playing Wordle by typing the following command,

```console
$ python cli.py
```

## Usage

```console
usage: cli.py [-h] [--random] [--seed SEED] [--solve] [--helper]

Wordle on your terminal

optional arguments:
  -h, --help   show this help message and exit
  --random     Show a random Wordle
  --seed SEED  Seed the RNG
  --solve      Simulate WordleSolver
  --helper     Take help from WordleSolver for a Wordle in a different platform

```

## Terminology

All of the following terms are valid in the context of a specific Wordle.

* A set of **known letters** is a set of letters which are known to be present in the Wordle's word based on clues obtained from the previous attempts.
* A set of **valid words** at any given point refers to a set of words from vocabulary that are possible solutions to the Wordle at that point based on the clues obtained till then.
* A letter is said to **cover** a word if the letter belongs to that word.
* **Coverage** *(absolute)* of a word refers to the percentage of valid words (at that point) covered by the letters in that word.
* **Coverage** *(relative)* of a word refers to the percentage of valid words (at that point) covered by the set of

## Solver

WordleSolver roughly uses the following strategy,

* Guess a word with highest (relative) coverage.
* After each guess, eliminate words based on the clues, e.g.,
    * Remove all words that contain an `incorrect-letter`
    * Remove all words that do not contain the identified `(correct-letter, correct-position)` combinations
    * Remove all words that contain the identified `(correct-letter, incorrect-position)` combinations
    * Remove all words that do not contain a `correct-letter`
    * Re-calculate (relative) coverage and guess again
* If at any point, number of valid words drops below number of attempts left, guess the valid words one-by-one.
* Additionally, there are heuristics to choose a word if multiple words with best coverage-score exist.

## Helper

WordleSolver will help you solve a third-party Wordle.

* Suggestions for words will be provided at each step.
* You may choose a word and obtain result.
* Enter the obtained result as a ternary string,
  i.e., a string made of 0, 1, and 2.
  - 0 : (grey)   : an incorrect letter.
  - 1 : (yellow) : a correct letter in wrong position.
  - 2 : (green)  : a correct letter in correct position.
  e.g., if the third letter turned green and fifth letter turned yellow in the third party Wordle, then you should input 00201 as the result obtained.

## Evaluation

WordleSolver has been evaluated on the entire vocabulary.

### Setup

* Word Size: 5
* Vocabulary Size: 15918
* Maximum Attempts: 6

### Performance

* Success Count: 15446
* Success Rate: 97.03 %
* Average Attempts: 4.58

## How to specify a custom vocabulary?

* Make a directory `custom/` in the base directory.
* Create a vocabulary file `vocabulary.txt` with one word on each line.
* Place a `vocabulary.txt` file in `custom/` directory
