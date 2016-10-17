# -*- coding: utf-8 -*-

import os
import pickle


class Vocabulary(object):

    """Vocabulary."""

    def __init__(self, fname):
        """Constructs a Vocabulary from a file.

        Args:
            fname: File name.
        """
        with open(fname) as f:
            lines = f.readlines()

        self._dictionary = ['' for i in range(len(lines))]
        for l in lines:
            if l:
                try:
                    index, word = l.split(' ')
                    index = int(index)
                    word = word.strip()
                except ValueError:
                    continue

                self._dictionary[index - 1] = word

    def get(self, i):
        """Gets the i-th word in the vocabulary.

        Args:
            i: Index.

        Returns:
            Word.
        """
        return self._dictionary[i - 1]


class MarkovChain(object):

    """Markov chain."""

    def __init__(self, order):
        """Constructs a MarkovChain.

        Args:
            order: Order of the Markov chain.
        """
        self._chain = {}
        self._order = order

    def __contains__(self, present_state):
        """Returns whether the current state is modeled by this Markov chain or
        not.

        Args:
            present_state: Tuple of present states.

        Returns:
            Whether the present state is modeled by this chain or not.
        """
        return present_state in self._chain

    @property
    def order(self):
        """Order of the Markov chain."""
        return self._order

    def set(self, present_state, future_state, prob):
        """Adds a new link in the Markov chain.

        Args:
            present_state: Tuple of present states.
            future_state: Future state.
            prob: Probability of future state given present state.
        """
        if present_state not in self._chain:
            self._chain[present_state] = {}
        self._chain[present_state][future_state] = prob

    def yield_future_states(self, present_state):
        """Iterates through all possible future states given present state.

        Args:
            present_state: Tuple of present states.

        Yields:
            Tuple of (future state, its probability).
        """
        if present_state not in self._chain:
            return

        possible_outcomes = self._chain[present_state]
        for future_state in possible_outcomes:
            yield (future_state, possible_outcomes[future_state])

    @classmethod
    def from_file(cls, fname, order):
        """Constructs a MarkovModel from a file.

        Args:
            fname: File name.
            order: Order of the Markov chain.

        Returns:
            MarkovModel.
        """
        with open(fname) as f:
            lines = f.readlines()

        chain = MarkovChain(order)
        for l in lines:
            if l:
                try:
                    *present_state, future_state, prob = l.split(' ')
                    present_state = tuple(map(int, present_state))
                    future_state = int(future_state)
                    prob = 10 ** float(prob)
                except ValueError:
                    continue

                chain.set(present_state, future_state, prob)

        return chain


# File paths storing vocabulary and ngrams.
# Index is order of the Markov chain, and value is tuple of the serialized
# MarkovChain, and the raw data file.
_vocabulary_path = ("data/vocab.p", "data/vocab.txt")
_ngram_paths = [
    ("data/unigrams.p", "data/unigram_counts.txt"),
    ("data/bigrams.p", "data/bigram_counts.txt"),
    ("data/trigrams.p", "data/trigram_counts.txt")
]


def get_vocabulary():
    """Returns vocabulary to use."""
    serialized_file, raw_file = _vocabulary_path
    if not os.path.isfile(serialized_file):
        vocabulary = Vocabulary(raw_file)
        pickle.dump(vocabulary, open(serialized_file, "wb"))
    else:
        vocabulary = pickle.load(open(serialized_file, "rb"))
    return vocabulary


def get_ngram(order):
    """Returns deserialized n-gram of given order.

    Args:
        order: Order of the corresponding Markov chain.

    Returns:
        MarkovChain.
    """
    serialized_file, raw_file = _ngram_paths[order]
    if not os.path.isfile(serialized_file):
        chain = MarkovChain.from_file(raw_file, order)
        pickle.dump(chain, open(serialized_file, "wb"))
    else:
        chain = pickle.load(open(serialized_file, "rb"))
    return chain


def get_all_ngrams():
    """Returns a list of all available n-grams."""
    ngrams = list(get_ngram(i) for i in range(len(_ngram_paths)))
    return ngrams
