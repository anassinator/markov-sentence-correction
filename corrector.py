#!/usr/bin/env python3

import deserializer
import editdistance
from sentence import Sentence
from distribution import poisson_distribution


def consecutive(iterable, n=2):
    """Iterates through consecutive n-tuples from an iterable.

    Args:
        iterable: Iterable.
        n: Number of elements to take at a time.

    Yields:
        Tuple of n consecutive items.
    """
    for n_tuple in zip(*(iterable[x:] for x in range(n))):
        yield n_tuple


def correct(sentence, bigrams, distribution):
    trellis = [{Sentence.START: (1.0, None)}]

    observed_words = list(sentence)
    number_of_words = len(observed_words)

    for k in range(1, number_of_words - 1):
        observed_word = observed_words[k]
        trellis.append({})

        previous_states = trellis[k - 1]
        current_states = trellis[k]

        for previous_word in previous_states:
            future_states = bigrams.yield_future_states((previous_word,))

            for possible_word, prob in future_states:
                conditional_prob = previous_states[previous_word][0] * prob
                distance = editdistance.eval(observed_word, possible_word)
                total_prob = conditional_prob * distribution(distance)

                if possible_word in current_states:
                    if current_states[possible_word][0] >= total_prob:
                        continue

                current_states[possible_word] = (total_prob, previous_word)

    last_states = trellis[-1]
    most_probable_end  = max(((word, last_states[word])
                              for word in last_states), key=lambda x: x[1][0])
    last_word, (total_prob, previous_word) = most_probable_end

    corrected_words = []
    print(last_states)
    for k in range(number_of_words - 2, 0, -1):
        print(previous_word)
        corrected_words.insert(0, previous_word)
        previous_word = trellis[k][previous_word][1]

    corrected_sentence = Sentence()
    for word in corrected_words:
        corrected_sentence.add(word)

    return (corrected_sentence, total_prob, trellis)


if __name__ == "__main__":
    bigrams = deserializer.get_ngram(order=1)
    distribution = poisson_distribution(gamma=0.01)

    line = input()
    sentence = Sentence.from_line(line.strip())
    corrected, prob, trellis = correct(sentence, bigrams, distribution)
    print(corrected, prob)
