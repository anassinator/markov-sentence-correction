# -*- coding: utf-8 -*-

import math


def poisson_distribution(gamma):
    """Computes the probability of events for a Poisson distribution.

    Args:
        gamma: The average number of events to occur in an interval.

    Returns:
        The probability distribution of k events occuring.
        This is a function taking one parameter (k) and returning the
        probability of k events occuring.
    """
    constant_factor = math.e ** (-gamma)

    def probability(k):
        """The probability of k events occuring for a Poisson distribution.

        Args:
            k: The number of the events occuring in an interval.

        Returns:
            The probability of k events occuring in the given distribution.
        """
        return (constant_factor * gamma ** k) / (math.factorial(k))

    return probability
