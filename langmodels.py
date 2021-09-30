import sys
import math

PHI = '/phi/'

def flatten_list_of_list(lol):
    return [item for sublist in lol for item in sublist]

def prob_unigram(normalized_tok, freq_of_unigram, total_unigrams):
    return freq_of_unigram[normalized_tok] / total_unigrams

def prob_bigram(normalized_tok_1, normalized_tok_2, freq_of_bigram, freq_of_unigram, phi_count):
    #Pr(w{k}|w{k−1}) = Freq(w{k−1} w{k})/Freq(w{k−1}).
    #Pr(tok2|tok1)   = Freq(tok1 tok2) / Freq(tok1)


    if freq_of_bigram.get((normalized_tok_1, normalized_tok_2)) is None: # Happens for never before seen bigram
        return 0.0 # Probability of 0


    elif freq_of_unigram.get(normalized_tok_1) is None: # This happens when normalized_tok_1 == PHI. PHI == number of sentences
        return freq_of_bigram[(normalized_tok_1,
                               normalized_tok_2)] / phi_count
    else:
        return freq_of_bigram[(normalized_tok_1,
                               normalized_tok_2)] / freq_of_unigram[normalized_tok_1]



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

def prob_of_sentence_bigram(sentence, freq_of_bigram, freq_of_unigram, phi_count):

    log_prob_sum = 0.0
    for i in range(len(sentence)-1):
        j = i+1
        normalized_tok_1 = sentence[i].lower()
        normalized_tok_2 = sentence[j].lower()
        pr_wk_given_wk_minus_1 = prob_bigram(normalized_tok_1,
                                             normalized_tok_2,
                                             freq_of_bigram,
                                             freq_of_unigram,
                                             phi_count)
        if  pr_wk_given_wk_minus_1 != 0:
            log_prob_sum += math.log2(pr_wk_given_wk_minus_1)
        else:
            return None # To mark as undefined
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
                # Haven't seen key yet => init count to 1
                unsmoothed_freq_of_unigram[normalized_tok] = 1
            else:
                # Increment count
                unsmoothed_freq_of_unigram[normalized_tok] += 1
    #print('freq_table: %s' % unsmoothed_freq_of_unigram)

    """
    Calculate unigram probability for each sentence
    """
    '''
    [['this', 'is', 'the', 'structure', '.']
     ['it', 'looks', 'like', 'this', '.']]
    '''
    unigram_sentence_to_prob = {}
    for sentence in test_file_tokens:
        unigram_sentence_to_prob[' '.join(sentence)] = prob_of_sentence_unigram(sentence, unsmoothed_freq_of_unigram, len(flatten_list_of_list(training_file_tokens)))

#    print(unigram_sentence_to_prob)


############## BIGRAM (UNSMOOTHED) =-------------------------------------------

    '''
    Generate unsmoothed bigram frequency table
    '''
    # Generate bigram token list with _PHI_ (sentence starter)
    for sentence in training_file_tokens:
        sentence.insert(0, PHI)  # Prepend PHI to every sentence
    #print(training_file_tokens)


    unsmoothed_freq_of_bigram = {}
    for sentence in training_file_tokens:
        for i in range(len(sentence)-1):
            j = i+1
            normalized_tok_1 = sentence[i].lower()
            normalized_tok_2 = sentence[j].lower()
            key = (normalized_tok_1, normalized_tok_2)
            if unsmoothed_freq_of_bigram.get(key) is None:
                # Haven't seen key yet => init count to 1
                unsmoothed_freq_of_bigram[key] = 1
            else:
                # Increment count
                unsmoothed_freq_of_bigram[key] += 1


    #print('unsmoothed_freq_of_bigram: %s' % unsmoothed_freq_of_bigram)

    """
    Calculate unsmoothed bigram probability for each sentence
    """
    for sentence in test_file_tokens:
        sentence.insert(0, PHI)  # Prepend PHI to every sentence

    '''
    [['/phi/', 'this', 'is', 'the', 'structure', '.']
     ['/phi/', it', 'looks', 'like', 'this', '.']]
    '''
    unsmoothed_bigram_sentence_to_prob = {}
    for sentence in test_file_tokens:
        prob_s = prob_of_sentence_bigram(sentence,
                                         unsmoothed_freq_of_bigram,
                                         unsmoothed_freq_of_unigram,
                                         len(training_file_tokens))

        if prob_s is None:
            unsmoothed_bigram_sentence_to_prob[' '.join(sentence)] = 'undefined'
        else:
            unsmoothed_bigram_sentence_to_prob[' '.join(sentence)] = prob_s
             # == phi_count
    print('unsmoothed_bigram_sentence_to_prob: %s' % unsmoothed_bigram_sentence_to_prob)








if __name__ == "__main__":
    main()

