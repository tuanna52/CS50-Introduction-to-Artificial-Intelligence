import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj NP VP | NP VP Conj VP

AP -> Adj | Adj AP
NP -> N | Det NP | AP NP | N PP
PP -> P NP
VP -> V | VP NP | VP NP PP | V Adv | Adv V | VP PP | VP PP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    lowercased_words = list()

    word_tokens = nltk.tokenize.word_tokenize(sentence)

    for i in range(len(word_tokens)):
        if bool(re.match('[a-zA-Z]', word_tokens[i])):
            lowercased_words.append(word_tokens[i].lower())

    return lowercased_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    noun_phrase_chunks = list()

    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            count_np = 0
            for sst in subtree.subtrees():
                if sst.label() == "NP":
                    count_np += 1
            if count_np < 2:    #Check if NP contains any NP child. subtrees() function always returns parent's label then its children's label, thus we have to check if the number of NP label is smaller than 2.
                noun_phrase_chunks.append(subtree)

    return noun_phrase_chunks


if __name__ == "__main__":
    main()
