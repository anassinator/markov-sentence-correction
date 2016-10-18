# -*- coding: utf-8 -*-


def evaluate(source, target):
    """Evaluates the edit distance or Levenshtein distance between two strings
    using the Wagner–Fischer algorithm.

    Note: This was adapted from the pseudo-code on Wikipedia.

    Args:
        source: Source string.
        target: Target string.

    Returns:
        The edit distance between the source and target strings.
    """
    source_length = len(source)
    target_length = len(target)

    d = [[0 for j in range(target_length)] for i in range(source_length)]

    for i in range(source_length):
        d[i][0] = i

    for j in range(target_length):
        d[0][j] = j

    for j in range(target_length):
        for i in range(source_length):
            if source[i] == target[j]:
                # No operation required.
                d[i][j] = d[i - 1][j - 1]
            else:
                # Find the minimal operation required.
                deletion = d[i - 1][j] + 1
                insertion = d[i][j - 1] + 1
                substitution = d[i - 1][j - 1] + 1
                d[i][j] = min(deletion, insertion, substitution)

    return d[-1][-1]
