#!/usr/bin/env python3

import deserializer
import editdistance
from sentence import Sentence
from distribution import poisson_distribution


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
        Tuple of (corrected sentence, its probability).
    """
    trellis = [{Sentence.START: (1.0, None)}]

    observed_words = list(observed_sentence)
    number_of_words = len(observed_words)

    for k in range(1, number_of_words):
        observed_word = observed_words[k]
        max_errors = len(observed_word) * max_error_rate

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
    last_states = trellis[-1]
    end = max(((word, last_states[word])for word in last_states),
              key=lambda x: x[1][0])
    last_word, (total_prob, previous_word) = end

    # Backtrack to find path.
    corrected_words = [last_word]
    for state in reversed(trellis[:-1]):
        if previous_word and previous_word != Sentence.START:
            corrected_words.append(previous_word)
        previous_word = state[previous_word][1]

    # Generate correct sentence.
    corrected_sentence = Sentence()
    for word in reversed(corrected_words):
        corrected_sentence.add(word)

    return (corrected_sentence, total_prob)


def correct(observed_sentence, bigrams, distribution):
    """Corrects a given sentence.

    Note: This keeps trying to correct the sentence with an increasingly large
          max error rate until it succeeds.

    Args:
        observed_sentence: Observed sentence.
        bigrams: First-order Markov chain of likely word sequences.
        distribution: Error probability distribution function.

    Returns:
        Tuple of (corrected sentence, its probability).
    """
    rate = 0.1
    while True:
        try:
            return _correct(observed_sentence, bigrams, distribution, rate)
        except ValueError:
            rate += 0.1
            if rate >= 3.0:
                raise


if __name__ == "__main__":
    bigrams = deserializer.get_ngram(order=1)
    distribution = poisson_distribution(gamma=0.01)

    while True:
        try:
            line = input()
        except (KeyboardInterrupt, EOFError):
            break

        sentence = Sentence.from_line(line.strip())
        corrected_sentence, prob = correct(sentence, bigrams, distribution)
        print(corrected_sentence)
        print("Probability:", prob)
