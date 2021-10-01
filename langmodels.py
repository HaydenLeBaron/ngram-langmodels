import sys
import math
import copy

# TODO: refactor / clean up

PHI = '/phi/'

def flatten_list_of_list(lol):
    return [item for sublist in lol for item in sublist]

def prob_unigram(normalized_tok, freq_of_unigram, total_unigrams):
    return freq_of_unigram[normalized_tok] / total_unigrams

def prob_bigram(normalized_tok_1, normalized_tok_2, freq_of_bigram, freq_of_unigram, phi_count, do_smooth):
    #Pr(w{k}|w{k−1}) = Freq(w{k−1} w{k})/Freq(w{k−1}).
    #Pr(tok2|tok1)   = Freq(tok1 tok2) / Freq(tok1)

    unigram_freq = None
    if normalized_tok_1 == PHI:
        unigram_1_freq = phi_count
    else:
        unigram_1_freq = freq_of_unigram[normalized_tok_1]

    if do_smooth:
        vocab_size = len(freq_of_unigram.keys())
        if freq_of_bigram.get((normalized_tok_1, normalized_tok_2)) is None: # Happens for never before seen bigram
            return 1 / (unigram_1_freq + vocab_size)
        else:
            return (freq_of_bigram[(normalized_tok_1,
                                    normalized_tok_2)] + 1) / (unigram_1_freq + vocab_size)
    else:
        if freq_of_bigram.get((normalized_tok_1, normalized_tok_2)) is None: # Happens for never before seen bigram
            return 0.0 # Probability of 0
        else:
            return freq_of_bigram[(normalized_tok_1,
                                   normalized_tok_2)] / unigram_1_freq 


def prob_of_sentence_unigram(sentence, freq_of_unigram, total_unigrams):

    log_prob_sum = 0.0
    for tok in sentence:
        normalized_tok = tok.lower()
        prob_tok = prob_unigram(normalized_tok, freq_of_unigram, total_unigrams);

        # don't plug in 0 to log
        if prob_tok != 0:
            log_prob_sum += math.log2(prob_tok)
    return log_prob_sum

def prob_of_sentence_bigram(sentence, freq_of_bigram, freq_of_unigram, phi_count, do_smooth):

    log_prob_sum = 0.0
    for i in range(len(sentence)-1):
        j = i+1
        normalized_tok_1 = sentence[i].lower()
        normalized_tok_2 = sentence[j].lower()
        pr_wk_given_wk_minus_1 = prob_bigram(normalized_tok_1,
                                             normalized_tok_2,
                                             freq_of_bigram,
                                             freq_of_unigram,
                                             phi_count,
                                             do_smooth)
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
    training_file_tokens_w_phi = copy.deepcopy(training_file_tokens)
    # Generate bigram token list with _PHI_ (sentence starter)
    for sentence in training_file_tokens_w_phi:
        sentence.insert(0, PHI)  # Prepend PHI to every sentence


    unsmoothed_freq_of_bigram = {}
    for sentence in training_file_tokens_w_phi:
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
    test_file_tokens_w_phi = copy.deepcopy(test_file_tokens)
    for sentence in test_file_tokens_w_phi:
        sentence.insert(0, PHI)  # Prepend PHI to every sentence

    '''
    [['/phi/', 'this', 'is', 'the', 'structure', '.']
     ['/phi/', it', 'looks', 'like', 'this', '.']]
    '''
    unsmoothed_bigram_sentence_to_prob = {}
    for sentence in test_file_tokens_w_phi:
        prob_s = prob_of_sentence_bigram(sentence,
                                         unsmoothed_freq_of_bigram,
                                         unsmoothed_freq_of_unigram,
                                         len(training_file_tokens),
                                         False)

        if prob_s is None:
            unsmoothed_bigram_sentence_to_prob[' '.join(sentence)] = 'undefined'
        else:
            unsmoothed_bigram_sentence_to_prob[' '.join(sentence)] = prob_s
             # == phi_count


    '''
    Smoothen bigram frequency table
    '''

    # TODO: add one to each bigram (but not unigram) freqency. Then recalculate probabilities
    """
    Calculate smoothed bigram probability for each sentence
    """
    '''
    [['/phi/', 'this', 'is', 'the', 'structure', '.']
     ['/phi/', it', 'looks', 'like', 'this', '.']]
    '''
    smoothed_bigram_sentence_to_prob = {}
    for sentence in test_file_tokens_w_phi:
        prob_s = prob_of_sentence_bigram(sentence,
                                         unsmoothed_freq_of_bigram,
                                         unsmoothed_freq_of_unigram,
                                         len(training_file_tokens_w_phi),
                                         True)

        if prob_s is None:
            smoothed_bigram_sentence_to_prob[' '.join(sentence)] = 'undefined'
        else:
            smoothed_bigram_sentence_to_prob[' '.join(sentence)] = prob_s
             # == phi_count



    '''
    Print output
    '''
    for sentence in test_file_tokens:
        sentence_w_phi = copy.deepcopy(sentence)
        sentence_w_phi.insert(0, PHI)
        key_no_phi = ' '.join(sentence)
        key_w_phi = ' '.join(sentence_w_phi)

        unigram_val = None; unsmoothed_bigram_val = None; smoothed_bigram_val = None
        if unigram_sentence_to_prob[key_no_phi] == 'undefined':
            unigram_val = 'undefined'
        else:
            unigram_val = round(float(unigram_sentence_to_prob[key_no_phi]), 4)
        if unsmoothed_bigram_sentence_to_prob[key_w_phi] == 'undefined':
            unsmoothed_bigram_val = 'undefined'
        else:
            unsmoothed_bigram_val = round(float(unsmoothed_bigram_sentence_to_prob[key_w_phi]), 4)
        if smoothed_bigram_sentence_to_prob[key_w_phi] == 'undefined':
            smoothed_bigram_val = 'undefined'
        else:
            smoothed_bigram_val = round(float(smoothed_bigram_sentence_to_prob[key_w_phi]), 4)

        print('S = %s\n' % key_no_phi)
        print('Unsmoothed Unigrams, logprob(S) = %s' % unigram_val)
        print('Unsmoothed Bigrams, logprob(S) = %s' % unsmoothed_bigram_val)
        print('Smoothed Bigrams, logprob(S) = %s' % smoothed_bigram_val)
        print('')
        # TODO: round off numbers as per spec



if __name__ == "__main__":
    main()

