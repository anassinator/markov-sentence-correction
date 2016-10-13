# Data

This holds the vocabulary and the n-gram probability models.

## Vocabulary

`vocab.txt` holds an ordered list of words as follows:

```
n nth_word
```

where `n` is the index and `nth_word` is the word at that index.

## N-gram Probability Models

The n-gram probability models can be found in the following files. Note that
any missing conditional probabilities implies their probability is 0.

### `unigram_counts.txt`

This holds the unigram probability model as follows:

```
i log_10(P(x_t=i))
```

where `i` is the index of the word and `log_10(P(x_t=i))` is the logarithm of
the probability that the `i`-th word occurs.

### `bigram_counts.txt`

This holds the bigram probability model as follows:

```
i j log_10(P(x_t=j|x_{t-1}=i))
```

where `i` is the index of the first word, `j` is the index of the second word,
and `log_10(P(x_t=j|x_{t-1}=i))` is the logarithm of the probability that the
`j`-th word occurs if it's immediately preceded by the `i`-th word.

### `trigram_counts.txt`

This holds the trigram probability model as follows:

```
i j k log_10(P(x_t=k|x_{t-1}=j,x_{t-2}=i))
```

where `i` is the index of the first word, `j` is the index of the second word,
`k` is the index of the third word and `log_10(P(x_t=k|x_{t-1}=j,x_{t-2}=i))`
is the logarithm of the probability that the `k`-th word occurs if it's
immediately preceded by the sentence formed by the `i`-th and `j`-th words.
