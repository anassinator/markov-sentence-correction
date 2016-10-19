#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import verbose
import deserializer
import editdistance
from sentence import Sentence
from distribution import poisson_distribution


def _backtrack_path(trellis, last_word):
    """Finds the complete sentence and its probability from a Trellis graph.

    Args:
        trellis: Trallis graph.
        last_word: End word.

    Returns:
        Tuple of (sentence, probability).
    """
    total_prob, previous_word = trellis[-1][last_word]
    previous_prob = total_prob

    word_path = [last_word]
    individual_probabilities = []
    for state in reversed(trellis[:-1]):
        if previous_word and previous_word != Sentence.START:
            word_path.append(previous_word)
            individual_probabilities.insert(0, previous_prob)
        previous_prob, previous_word = state[previous_word]

    # Generate correct sentence.
    sentence_path = Sentence()
    for word in reversed(word_path):
        sentence_path.add(word)

    return (sentence_path, total_prob, individual_probabilities)


def _correct(observed_sentence, bigrams, distribution, max_error_rate):
    """Corrects a given sentence.

    Note: The lower the max_error_rate, the faster the algorithm, but the
          likelier it will fail.

    Args:
        observed_sentence: Observed sentence.
        bigrams: First-order Markov chain of likely word sequences.
        distribution: Error probability distribution function.
        max_error_rate: Maximum number of errors in a word to consider.

    Returns:
        Ordered list of tuples of (corrected sentence, its probability).
        Most likely interpretations come first.
    """
    trellis = [{Sentence.START: (1.0, None)}]

    observed_words = list(observed_sentence)
    number_of_words = len(observed_words)

    for k in range(1, number_of_words):
        observed_word = observed_words[k]
        max_errors = int(len(observed_word) * max_error_rate) + 1

        current_states = {}
        previous_states = trellis[k - 1]
        trellis.append(current_states)

        for previous_word in previous_states:
            previous_prob = previous_states[previous_word][0]

            future_states = bigrams.yield_future_states((previous_word,))
            for possible_word, conditional_prob in future_states:
                # Conditional probability: P(X_k | X_k-1) * previous
                # probability.
                total_prob = conditional_prob * previous_prob

                # Emission probability: P(E_k | X_k).
                distance = editdistance.eval(observed_word, possible_word)
                total_prob *= distribution(distance)

                # Ignore states that have too many mistakes.
                if distance > max_errors:
                    continue

                # Only keep link of max probability.
                if possible_word in current_states:
                    if current_states[possible_word][0] >= total_prob:
                        continue

                current_states[possible_word] = (total_prob, previous_word)

    # Find most likely ending.
    interpretations = list(_backtrack_path(trellis, x) for x in trellis[-1])
    interpretations.sort(key=lambda x: x[1], reverse=True)

    return interpretations


def correct(observed_sentence, bigrams, distribution):
    """Corrects a given sentence.

    Note: This keeps trying to correct the sentence with an increasingly large
          max error rate until it succeeds.

    Args:
        observed_sentence: Observed sentence.
        bigrams: First-order Markov chain of likely word sequences.
        distribution: Error probability distribution function.

    Returns:
        Ordered list of tuples of (corrected sentence, its probability).
        Most likely interpretations come first.
    """
    rate = 0.1
    while True:
        try:
            results = _correct(observed_sentence, bigrams, distribution, rate)
        except ValueError:
            pass
        if results:
            return results
        rate += 0.1
        if rate >= 3.0:
            return []


def total_distance(observed_sentence, corrected_sentence):
    """Calculates the total distance between the two given sentences.

    Args:
        observed_sentence: Observed sentence.
        corrected_sentence: Corrected sentence.

    Returns:
        Total Levenshtein distance between the two sentences.
    """
    total_distance = 0

    observed_words = list(observed_sentence)
    corrected_words = list(corrected_sentence)

    for i in range(len(observed_words)):
        comparable_words = observed_words[i], corrected_words[i]
        total_distance += editdistance.eval(*comparable_words)

    return total_distance


if __name__ == "__main__":
    bigrams = deserializer.get_ngram(order=1)
    distribution = poisson_distribution(gamma=0.01)

    verbose_output = verbose.is_verbose()
    while True:
        try:
            line = input()
        except (KeyboardInterrupt, EOFError):
            break

        sentence = Sentence.from_line(line.strip())
        interpretations = correct(sentence, bigrams, distribution)
        (corrected, total_prob, individual_prob), *others = interpretations
        print(corrected)

        if verbose_output:
            distance = total_distance(sentence, corrected)
            print("total distance:", distance)
            print("total probability:", total_prob)
            print("word-by-word probabilities:", *individual_prob)

            if others:
                print("other possible interpretations:")
            for i, (possibility, prob, _) in enumerate(others):
                # Only print out the top 3 possibilities.
                if i >= 3:
                    break

                distance = total_distance(sentence, possibility)
                print(str(possibility),
                      "(probability: {}, distance: {})".format(prob, distance))
