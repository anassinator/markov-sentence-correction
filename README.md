# Sentence Generation and Correction

This is a submission to the second assignment of McGill University's ECSE 526 -
Artificial Intelligence course. Details can be found
[here](https://github.com/anassinator/markov-sentence-correction/files/1595010/as2.pdf).

# Setup

To run this, all one needs is Python 3.4 or above and `pip3`.

To install dependencies, simply run:

```bash
pip3 install -r requirements.txt
```

# Details

This assignment has two parts:

## Sentence Generation

Sentence are randomly generated using Markov models defined in [`data`](data).

To run, simply execute:

```bash
python3 generator.py
```

More detailed output can be displayed using th e `-v` or `--verbose` flags.

## Sentence Correction

Sentence are corrected using a Hidden Markov Model (HMM) and Viterbi's
algorithm. The intput is read from `stdin`, and the output is the most likely
sentence based on a first-order Markov chain and the Levenshtein distance.

To run, simply execute:

```bash
python3 corrector.py
```

Input can also be piped in as follows:

```bash
echo "Tell moi" | python3 corrector.py
# Tell me
```

More detailed output can be displayed using th e `-v` or `--verbose` flags.

## Accuracy

Note that the accuracy of both the sentences generated and the corrections is
only dependent on the data set used. Valid English words will be "corrected"
if they are not found in the data set. Take a look [here](data) for details on
how to use your own dataset.
