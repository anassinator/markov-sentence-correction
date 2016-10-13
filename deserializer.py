# -*- coding: utf-8 -*-

from abc import ABCMeta


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


class NGramModel(object, metaclass=ABCMeta):

    """N-gram model."""

    def __init__(self, fname, n):
        """Constructs an NGramModel from a file.

        Args:
            fname: File name.
            n: Number of items.
        """
        self._n = n

        with open(fname) as f:
            lines = f.readlines()

        self._model = {}
        for l in lines:
            if l:
                try:
                    *key, prob = l.split(' ')
                    key = tuple(map(int, key))
                    prob = 10 ** float(prob)
                except ValueError:
                    continue

                self._model[key] = prob

        self._keys = self._model.keys()

    @property
    def n(self):
        """Returns the number of items in the n-gram."""
        return self._n

    def get(self, *key):
        """Gets the probability of a certain n-gram.

        Args:
            key: Elements of the n-gram.

        Returns:
            Conditional probability of the given n-gram.
        """
        return self._model[key]

    def yield_keys(self, *prefix):
        """Yields keys that are prefixed by a given sequence.

        Args:
            prefix: Sequence of word indices.

        Yields:
            Key that starts with given sequence.
        """
        keys = self._keys

        if prefix:
            prefix_length = len(prefix)
            keys = filter(lambda x: x[:prefix_length] == prefix, self._keys)

        for k in keys:
            yield k


class UnigramModel(NGramModel):

    """Unigram model."""

    def __init__(self, fname):
        """Constructs a UnigramModel from a file.

        Args:
            fname: File name.
        """
        super().__init__(fname, 1)


class BigramModel(NGramModel):

    """Bigram model."""

    def __init__(self, fname):
        """Constructs a BigramModel from a file.

        Args:
            fname: File name.
        """
        super().__init__(fname, 2)


class TrigramModel(NGramModel):

    """Trigram model."""

    def __init__(self, fname):
        """Constructs a TrigramModel from a file.

        Args:
            fname: File name.
        """
        super().__init__(fname, 3)


vocabulary = Vocabulary("data/vocab.txt")
unigrams = UnigramModel("data/unigram_counts.txt")
bigrams = BigramModel("data/bigram_counts.txt")
trigrams = TrigramModel("data/trigram_counts.txt")
