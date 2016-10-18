#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import deserializer
from sentence import Sentence


class NoWordFound(Exception):

    """No word was found."""

    pass


class SentenceGenerator(object):

    """Sentence generator."""

    def __init__(self, chains):
        """Constructs a SentenceGenerator.

        Args:
            chains: Ordered list of n-grams. Unigram should be at index 0,
                    followed by bigram at index 1, and so on.
        """
        self._chains = chains
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
        for chain in reversed(self._chains):
            present_states_required = chain.order
            if word_count >= present_states_required:
                present_states = sentence.get_last(present_states_required)
                try:
                    return word_generator(present_states, chain)
                except NoWordFound:
                    continue

        # Should not be reached.
        raise NoWordFound

    def _get_random_word(self, present_states, chain):
        """Gets a random word given the current state and n-gram using the
        specified conditional probabilities.

        Args:
            present_states: List of present states.
            chain: Markov chain.

        Returns:
            Tuple of (random word, probability of it occuring).
        """
        if present_states not in chain:
            raise NoWordFound("Markov chain has no possible outcome")

        # Normalize since the conditional probabilities are not guaranteed to
        # sum up to 1.
        possible_outcomes = list(chain.yield_future_states(present_states))
        normalization_factor = sum(prob for _, prob in possible_outcomes)
        rand = self.__generator.uniform(0, normalization_factor)
        for outcome, prob in possible_outcomes:
            if rand <= prob:
                return (outcome, prob / normalization_factor)
            rand -= prob

        # This should not be possible.
        raise RuntimeError("Could not generate any word from the given set...")


def generate(generator):
    """Generates a sentence given a sentence generator.

    Args:
        generator: Sentence generator.

    Returns:
        Tuple of (generated sentence, total probability).
    """
    sentence = Sentence()

    total_prob = 1.0
    while not sentence.complete:
        word, prob = generator.generate_random_word(sentence)
        sentence.add(word)
        total_prob *= prob

    return (sentence, total_prob)


if __name__ == "__main__":
    generator = SentenceGenerator(deserializer.get_all_ngrams())

    sentence, total_prob = generate(generator)
    print(sentence)
    print("Probability: ", total_prob)
