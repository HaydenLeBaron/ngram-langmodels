# N-gram Language Model

This NLP project uses training text to create, unigram (no smoothing), bigram (no smoothing), and bigram (add-one smoothing) language models. The program allows the user to estimate the probability of any given string string under the language model(s) generated by the training data.

## How to Run

```
$ python3 langmodels.py <training_file> -test <test_file>
```
OR
```
$ bash langmodels.sh # to print the outputs of tests 1 and 2 to langmodels-output.txt
```

## Input file Format

The *training_file* should consist of sentences, with exactly one sentence per line. For example:

```txt
Hello world .
My name is C3P0 !
I have a bad feeling about this .
```

Each sentence will be divided into unigrams based solely on white space. For better results, punctuation marks should be isolated, surrounded on both sides by whitespace. This way, punctuation marks are solitary unigrams.

The *test_file* should have the same format as the *training file*.

## Output Format

The program will print the following information to standard output in the following format:
```txt

S = <sentence>

Unsmoothed Unigrams, logprob(S) = #
Unsmoothed Bigrams, logprob(S) = #
Smoothed Bigrams, logprob(S) = #

...(continues for each sentence in the testing file)
```


## Resources

- I learned about the math behind unigram/bigram models from the textbook "Speech and Language Processing" by Daniel Jurafsky & James H. Martin.(https://web.stanford.edu/~jurafsky/slp3/3.pdf)
