import sys
import math

def flatten_list_of_list(lol):
    return [item for sublist in lol for item in sublist]

def prob_unigram(normalized_tok, freq_of_unigram, total_unigrams):
    return freq_of_unigram[normalized_tok] / total_unigrams



# BKRMK
def prob_of_sentence_unigram(sentence, freq_of_unigram, total_unigrams):

    log_prob_sum = 0.0
    for tok in sentence:
        normalized_tok = tok.lower()
        prob_tok = prob_unigram(normalized_tok, freq_of_unigram, total_unigrams);

        # don't plug in 0 to log
        if prob_tok != 0:
            log_prob_sum += math.log2(prob_tok)
    return log_prob_sum



"""
The main entry point of this program.
"""
def main():

    '''
    Parse CLI args
    '''
    training_file_path = sys.argv[1]
    cli_flag = sys.argv[2] # Expects "-test"
    test_file_path = sys.argv[3]

    '''
    Parse training file into tokens
    '''
    training_file_tokens = []
    with open(training_file_path) as training_file:
        for line in training_file:
            training_file_tokens.append(line.split())

    '''
    Parse test file into tokens
    '''
    test_file_tokens = []
    with open(test_file_path) as test_file:
        for line in test_file:
            test_file_tokens.append(line.split())



    '''
    Generate unigram frequency table
    '''
    unsmoothed_freq_of_unigram = {}
    for sentence in training_file_tokens:
        for tok in sentence:
            normalized_tok = tok.lower()
            if unsmoothed_freq_of_unigram.get(normalized_tok) is None:
                # Haven't seen key yet => init count to 0
                unsmoothed_freq_of_unigram[normalized_tok] = 1
            else:
                # Increment unigram count
                unsmoothed_freq_of_unigram[normalized_tok] += 1
    #print('freq_table: %s' % unsmoothed_freq_of_unigram)


    """
    Calculate probability for each sentence
    """
    '''
    [['this', 'is', 'the', 'structure', '.']
     ['it', 'looks', 'like', 'this', '.']]
    '''
    sentence_to_prob = {}
    for sentence in test_file_tokens:
        sentence_to_prob[' '.join(sentence)] = prob_of_sentence_unigram(sentence, unsmoothed_freq_of_unigram, len(flatten_list_of_list(training_file_tokens)))

    print(sentence_to_prob)



if __name__ == "__main__":
    main()

