#!/usr/bin/env python2.7

# Source: https://gist.github.com/alexbowe/879414

import nltk
import fileinput
import unidecode
import re

# Used when tokenizing words
sentence_re = r'''(?x)      # set flag to allow verbose regexps
      ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*            # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                # ellipsis
    | [][.,;"'?():-_`]      # these are separate tokens
'''
 
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
 
#Taken from Su Nam Kim Paper...
grammar = r"""
    NBAR:
        {<DT><NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""
chunker = nltk.RegexpParser(grammar)

text = ''
for line in fileinput.input():
    # line = re.sub(r'[^\x00-\x7F]+', ' ', line)
    text += line
# text = unidecode.unidecode(text)

toks = nltk.regexp_tokenize(text, sentence_re)
postoks = nltk.tag.pos_tag(toks)
 
# print postoks
 
tree = chunker.parse(postoks)
 
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
 
 
def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()
 
def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    # word = word.lower()
    # word = stemmer.stem_word(word)
    # word = lemmatizer.lemmatize(word)
    return word
 
def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(len(word) <= 40)
    #    and word.lower() not in stopwords)
    return accepted
 
 
def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
        yield term
 
terms = get_terms(tree)
 
for term in terms:
    for word in term:
        print word,
    print
