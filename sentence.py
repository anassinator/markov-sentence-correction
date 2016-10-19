# -*- coding: utf-8 -*-


class Sentence(object):

    """Sentence."""

    START = "<s>"
    STOP = "</s>"
    LEFT_SIDED_SYMBOLS = set('"\',.-/:;<>?!)]}$%')
    RIGHT_SIDED_SYMBOLS = set('"\'-/<>([{')
    SYMBOLS = LEFT_SIDED_SYMBOLS.union(RIGHT_SIDED_SYMBOLS)

    def __init__(self):
        "Constructs a Sentence."""
        self._word_list = [Sentence.START]
        self._sentence = ""

    def __str__(self):
        """Returns a string representation of the sentence."""
        return self._sentence

    def __len__(self):
        """Returns the number of words in a sentence."""
        return len(self._word_list)

    def __iter__(self):
        """Iterates through the sentence word by word."""
        return iter(self._word_list)

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

    @classmethod
    def from_line(self, line):
        """Constructs a Sentence from a line of text.

        Args:
            line: Line of text.

        Returns:
            Sentence.
        """
        sentence = Sentence()

        words = line.split(' ')
        sentence._word_list.extend(words)
        sentence._word_list.append(Sentence.STOP)
        sentence._sentence = line

        return sentence
