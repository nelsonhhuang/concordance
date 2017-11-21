# Using a dictionary with the key being each word 
# and the value being a tuple with word count and a list of the sentence location
# 
# Steps of approach:
# 1. Split the string into sentences. I used the punkt tokenizer.
# 2. Split the sentences into lower case words to use in the dictionary using the treebank tokenizer
#    I used another generalized regular expression to trim non alphanumerics
# 3. For each cleaned word, I put it into a dictionary with the word being the key, updating the word count
#    and appending the location of the word into the list. O(n)
# 4. I used python's sort method to return a list of ordered words. O(k log k) where k is the number of keys -> bound by O(n log n)
# 5. I created a method to create a list of alphabetical labels based on the size of the dictionary.
# 6. Finally, I created a method to print the results.

# Overall, the time complexity of this O(n log n) because of the worst case of all words being unique due to sorting.

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.tokenize.treebank import TreebankWordTokenizer
import re
import sys

sample = 'Given an arbitrary text document written in English, write a program that will generate \
a concordance, i.e. an alphabetical list of all word occurrences, labeled with word \
frequencies. Bonus: label each word with the sentence numbers in which each occurrence appeared.'


def split_sentences(s):
    # init custom parameters
    punkt_params = PunktParameters()
    
    # adding custom exceptions. many standard abbreviations are taken care of.
    # 'i.e' is standard but 'i.e.' is not
    punkt_params.abbrev_types = set(['i.e'])
    
    # init tokenizer and tokenize into list of sentences
    punkt_tokenizer = PunktSentenceTokenizer(punkt_params)
    sentences = punkt_tokenizer.tokenize(s)
    
    return sentences
    
def concordance(sentences):
    # init word tokenizer
    treebank_tokenizer = TreebankWordTokenizer()
    
    # general regex to match string that starts with a alphanumeric
    # for unmatching punctuation
    alphanumeric_pattern = '^\w+.*'
    
    # initialize empty dictionary
    word_count = {}
    
    sentence_num = 0
    for s in sentences:
        sentence_num += 1
        
        # tokenize into list of words
        words = treebank_tokenizer.tokenize(s)
        
        for w in words:
            w_lower = w.lower()
            
            # match to regex
            alpha_word = re.match(alphanumeric_pattern, w_lower)
            
            if alpha_word:
                # if word not in dict initialize tuple 
                if w_lower not in word_count:
                    word_count[w_lower] = (1, [sentence_num])
                # else update tuple. increment count and add location
                else:
                    current_word = word_count[w_lower]
                    word_count[w_lower] = (current_word[0]+1, current_word[1]+[sentence_num])

    return word_count
        

def pretty_print_concordance(word_obj): 
    # loop through and print
    for i in range(len(word_obj)):
        item = word_obj[i]
        print('{}\t{{{}:{}}}'.format(item[0], item[1][0], ','.join(map(str, item[1][1]))))

def parse_file_to_string(infile):
    # read in file and convert to string
    with open(infile, 'r') as file_obj:
        s = file_obj.read().replace('\n', '')
        
    return s


if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = parse_file_to_string(sys.argv[1])
    else:
        data = sample
        
    sentences = split_sentences(data)
    unsorted_count = concordance(sentences)
    sorted_count = sorted(unsorted_count.items())
    pretty_print_concordance(sorted_count)