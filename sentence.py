# -*- coding: utf-8 -*-


class Sentence(object):

    """Sentence."""

    START = "<s>"
    STOP = "</s>"
    LEFT_SIDED_SYMBOLS = set('"\',.-/:;<>?!)]}$%')
    RIGHT_SIDED_SYMBOLS = set('"\'-/<>([{')

    def __init__(self):
        "Constructs a Sentence."""
        self._word_list = [Sentence.START]
        self._sentence = ""

    @property
    def complete(self):
        """Whether the sentence is complete or not."""
        return self._word_list[-1] == Sentence.STOP

    def add(self, word):
        """Adds a word to the sentence.

        Args:
            word: Word.
        """
        self._word_list.append(word)
        if word != Sentence.STOP:
            if (word[0] not in Sentence.LEFT_SIDED_SYMBOLS and
                    self._sentence and
                    self._sentence[-1] not in Sentence.RIGHT_SIDED_SYMBOLS):
                self._sentence += ' '
            self._sentence += word

    def get_last(self, n):
        """Returns the indices of the last n words in the sentence.

        Args:
            n: Number of last words to get from the sentence.
        """
        return tuple(self._word_list[-n:])

    def __str__(self):
        """Returns a string representation of the sentence."""
        return self._sentence

    def __len__(self):
        """Returns the number of words in a sentence."""
        return len(self._word_list)
