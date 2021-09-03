import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()

    print("Loading files and their content...")
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), encoding="utf8") as f:

            # Extract file's content
            contents = f.read()

            files[filename] = contents

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = [
        word.lower() for word in
        nltk.word_tokenize(document)
        #Filter out words that are punctuation, stopwords, and not alphabets or digits
        if ((word not in string.punctuation) and (word.lower() not in nltk.corpus.stopwords.words("english")) and word.isalnum())
    ]

    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()

    # Get all words in corpus
    words = set()
    for filename in documents:
        words.update(documents[filename])

    # Calculate IDFs
    idfs = dict()
    for word in words:
        f = sum(word in documents[filename] for filename in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    list_top_files = list()

    # Calculate total TF-IDFs of each file
    tfidfs = dict()
    for filename in files:
        tfidfs[filename] = 0
        for q_word in query:
            #Words in the query that do not appear in the file will not contribute to the file’s score:
            if q_word not in files[filename]:
                continue

            tf = files[filename].count(q_word)
            tfidfs[filename] += tf * idfs[q_word]

    sorted_files_tfidfs  = [k for k, v in sorted(tfidfs.items(), key=lambda item: item[1], reverse=True)]
    
    list_top_files = sorted_files_tfidfs[:n]

    print(list_top_files)

    return list_top_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    list_top_sentences = list()

    #This is a dictionary to store matching word measure value and query team density value of each sentency.
    sentences_dict = dict()

    for sentence in sentences:
        matching_word_measure = 0
        query_term_density = 0

        for q_word in query:
            if q_word in sentences[sentence]:
                matching_word_measure += idfs[q_word]
            query_term_density += sentences[sentence].count(q_word)/len(sentences[sentence])

        sentences_dict[sentence] = (matching_word_measure, query_term_density)

    sorted_sentences = [k for k, v in sorted(sentences_dict.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True)]

    list_top_sentences = sorted_sentences[:n]

    return list_top_sentences


if __name__ == "__main__":
    main()
