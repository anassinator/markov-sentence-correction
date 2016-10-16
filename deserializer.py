# -*- coding: utf-8 -*-

import os
import pickle


class Vocabulary(object):

    """Vocabulary."""

    @classmethod
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

    def __init__(self, n):
        """Constructs a MarkovChain.

        Args:
            n: Order of the Markov chain.
        """
        self._chain = {}
        self._n = n

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
    def n(self):
        """Order of the Markov chain."""
        return self._n

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
    def from_file(cls, fname, n):
        """Constructs a MarkovModel from a file.

        Args:
            fname: File name.
            n: Order of the Markov chain.

        Returns:
            MarkovModel.
        """
        with open(fname) as f:
            lines = f.readlines()

        chain = MarkovChain(n)
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


def get_vocabulary():
    """Returns vocabulary to use."""
    return Vocabulary("data/vocab.txt")


def get_ngrams():
    ngrams_file = "data/ngrams.p"
    if not os.path.isfile(ngrams_file):
        ngrams = [
            MarkovChain.from_file("data/unigram_counts.txt", 1),
            MarkovChain.from_file("data/bigram_counts.txt", 2),
            MarkovChain.from_file("data/trigram_counts.txt", 3)
        ]
        pickle.dump(ngrams, open(ngrams_file, "wb"))
    else:
        ngrams = pickle.load(open(ngrams_file, "rb"))
    return ngrams
