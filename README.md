# N-gram Language Model

This NLP project uses training text to create, unigram (no smoothing), bigram (no smoothing), and bigram (add-one smoothing) language models. The program allows the user to estimate the probability of any given string string under the language model.

## How to Run

```
$ python3 langmodels.py <training.txt> -test <test.txt>
```

```
$ bash langmodels.sh # to print the outputs of tests 1 and 2 to langmodels-output.txt
```

## Resources

- I learned about the math behind unigram/bigram models from the textbook "Speech and Language Processing" by Daniel Jurafsky & James H. Martin.(https://web.stanford.edu/~jurafsky/slp3/3.pdf)
