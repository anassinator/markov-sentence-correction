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

        self._set = set()
        self._list = ['' for i in range(len(lines))]
        for l in lines:
            if l:
                try:
                    index, word = l.split(' ')
                    index = int(index)
                    word = word.strip()
                except ValueError:
                    continue

                self._list[index - 1] = word
                self._set.add(word)

    def __iter__(self):
        """Iterates through vocabulary."""
        return iter(self._list)

    def __contains__(self, word):
        """Returns whether the current vocabulary contains a given word or not.

        Args:
            word: Word.

        Returns:
            Whether the given word exists in this vocabulary or not.
        """
        return word in self._set

    def get(self, i):
        """Gets the i-th word in the vocabulary.

        Args:
            i: Index.

        Returns:
            Word.
        """
        return self._list[i - 1]


class MarkovChain(object):

    """Markov chain."""

    def __init__(self, order, vocabulary):
        """Constructs a MarkovChain.

        Args:
            order: Order of the Markov chain.
            vocabulary: Vocabulary to use.
        """
        self._chain = {}
        self._order = order
        self._vocab = vocabulary

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

    def _set(self, present_state, future_state, prob):
        """Adds a new link in the Markov chain.

        Args:
            present_state: Tuple of present states.
            future_state: Future state.
            prob: Probability of future state given present state.
        """
        present_words = tuple(map(self._vocab.get, present_state))
        if present_words not in self._chain:
            self._chain[present_words] = {}

        future_word = self._vocab.get(future_state)
        self._chain[present_words][future_word] = prob

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
    def from_file(cls, fname, order, vocabulary):
        """Constructs a MarkovModel from a file.

        Args:
            fname: File name.
            order: Order of the Markov chain.
            vocabulary: Vocabulary to use.

        Returns:
            MarkovModel.
        """
        with open(fname) as f:
            lines = f.readlines()

        chain = MarkovChain(order, vocabulary)
        for l in lines:
            if l:
                try:
                    *present_state, future_state, prob = l.split(' ')
                    present_state = tuple(map(int, present_state))
                    future_state = int(future_state)
                    prob = 10 ** float(prob)
                except ValueError:
                    continue

                chain._set(present_state, future_state, prob)

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

    Note: The order of an n-gram is n - 1.

    Args:
        order: Order of the corresponding Markov chain.

    Returns:
        MarkovChain.
    """
    serialized_file, raw_file = _ngram_paths[order]
    if not os.path.isfile(serialized_file):
        vocabulary = get_vocabulary()
        chain = MarkovChain.from_file(raw_file, order, vocabulary)
        pickle.dump(chain, open(serialized_file, "wb"))
    else:
        chain = pickle.load(open(serialized_file, "rb"))
    return chain


def get_all_ngrams():
    """Returns a list of all available n-grams."""
    ngrams = list(get_ngram(i) for i in range(len(_ngram_paths)))
    return ngrams
