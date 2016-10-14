#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import functools
import deserializer
from sentence import Sentence


class NoWordFound(Exception):

    """No word was found."""

    pass


class SentenceGenerator(object):

    """Sentence generator."""

    def __init__(self, *ngrams):
        """Constructs a SentenceGenerator.

        Args:
            ngrams: Ordered list of n-grams. Unigram should be at index 0,
                    followed by bigram at index 1, and so on.
        """
        self._ngrams = ngrams
        self.__generator = random.SystemRandom()

    def generate_random_word(self, sentence):
        """Generates the next word in a sentence at random.

        Args:
            sentence: Sentence.

        Returns:
            Tuple of (random word, probability of it occuring).
        """
        return self._generate_word(sentence, self._get_random_word)

    def generate_most_likely_word(self, sentence):
        """Generates the next most likely word in a sentence.

        Args:
            sentence: Sentence.

        Returns:
            Tuple of (most likely word, probability of it occuring).
        """
        return self._generate_word(sentence, self._get_most_likely_word)

    def _generate_word(self, sentence, word_generator):
        """Generates the next word in a sentence.

        Args:
            sentence: Sentence.
            word_generator: Function used to generate word.

        Returns:
            Tuple of (generated word, probability of it occuring).
        """
        word_count = len(sentence)
        for ngram in reversed(self._ngrams):
            past_states_required = ngram.n - 1
            if word_count >= past_states_required:
                past_states = sentence.get_last(past_states_required)
                try:
                    return word_generator(past_states, ngram)
                except NoWordFound:
                    continue

        # Should not be reached.
        raise NoWordFound

    def _get_most_likely_word(self, past_states, ngram):
        """Gets a random word given the current state and n-gram using the
        specified conditional probabilities.

        Args:
            past_states: List of past states.
            ngram: N-gram.

        Returns:
            Tuple of (random word, probability of it occuring).
        """
        possible_outcomes = ((state, ngram.get(*state))
                             for state in ngram.yield_keys(*past_states))
        if not possible_outcomes:
            raise NoWordFound("N-gram has no possible outcome")

        most_likely_outcome, prob = functools.reduce(
            lambda x, y: x if x[1] > y[1] else y,
            possible_outcomes)
        return (most_likely_outcome[-1], prob)

    def _get_random_word(self, past_states, ngram):
        """Gets a random word given the current state and n-gram using the
        specified conditional probabilities.

        Args:
            past_states: List of past states.
            ngram: N-gram.

        Returns:
            Tuple of (random word, probability of it occuring).
        """
        possible_outcomes = [(state, ngram.get(*state))
                             for state in ngram.yield_keys(*past_states)]
        if not possible_outcomes:
            raise NoWordFound("N-gram has no possible outcome")

        # Normalize since the conditional probabilities are not guaranteed to
        # sum up to 1.
        normalization_factor = sum(prob for _, prob in possible_outcomes)
        rand = self.__generator.random() * normalization_factor
        for outcome, prob in possible_outcomes:
            if rand <= prob:
                return (outcome[-1], prob)
            rand -= prob

        # This should not be possible.
        raise RuntimeError("Could not generate any word from the given set...")


if __name__ == "__main__":
    sentence = Sentence(deserializer.vocabulary)
    generator = SentenceGenerator(deserializer.unigrams,
                                  deserializer.bigrams,
                                  deserializer.trigrams)

    total_prob = 1.0
    while not sentence.complete:
        word, prob = generator.generate_random_word(sentence)
        sentence.add(word)
        total_prob *= prob

    print(sentence)
    print("Probability: ", total_prob)
