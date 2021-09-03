# CS50's Introduction to Artificial Intelligence - Course's Description
This course explores the concepts and algorithms at the foundation of modern artificial intelligence, diving into the ideas that give rise to technologies like game-playing engines, handwriting recognition, and machine translation. Through hands-on projects, students gain exposure to the theory behind graph search algorithms, classification, optimization, reinforcement learning, and other topics in artificial intelligence and machine learning as they incorporate them into their own Python programs. By course's end, students emerge with experience in libraries for machine learning as well as knowledge of artificial intelligence principles that enable them to design intelligent systems of their own.

# Projects' Description
## Search
* [Degrees](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Search/degrees):
According to the Six Degrees of Kevin Bacon game, anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that two actors both starred in. In this problem, Breadth First Search algorithm was used in finding the shortest path between any two actors by choosing a sequence of movies that connects them.

* [Tic-Tac-Toe](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Search/tictactoe):
An AI agent was implemented to play Tic-Tac-Toe optimally using Minimax algorithm.

## Knowledge
* [Knights](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Knowledge/knights):
In 1978, logician Raymond Smullyan published “What is the name of this book?”, a book of logical puzzles. Among the puzzles in the book were a class of puzzles that Smullyan called “Knights and Knaves” puzzles. In a Knights and Knaves puzzle, the following information is given: Each character is either a knight or a knave. A knight will always tell the truth: if knight states a sentence, then that sentence is true. Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false. The objective of the puzzle is, given a set of sentences spoken by each of the characters, determine, for each character, whether that character is a knight or a knave. In this project, the puzzles were represented using propositional logic, and an AI running a model-checking algorithm was implemented to solve these puzzles.

* [Minesweeper](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Knowledge/minesweeper):
An AI agent was implemented to play Minesweeper.

## Uncertainty
* [PageRank](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Uncertainty/pagerank):
An AI was implemented to rank web pages by importance using Markov Chain model.

* [Heredity](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Uncertainty/heredity):
An AI was implemented to assess the likelihood that a person will have a particular genetic trait. The famlily tree and associated variables was modeled by by forming a Bayesian Network.

## Optimization
* [Crossword](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Optimization/crossword):
An AI was implemented to generate crossword puzzles. The problem was modeled as a constraint satisfaction problem.

## Learning
* [Shopping](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Learning/shopping):
An AI was implemented using k-nearest neighbor classification algorithm to predict whether online shopping customers will complete a purchase.

* [Nim](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Learning/nim):
An AI that teaches itself to play Nim through reinforcement learning was implemented.

## Neural Networks
* [Traffic](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Neural_Networks/traffic):
An AI was implemented to identify which traffic sign appears in a photograp. In this project, a neural network to classify road signs based on an image of those signs was built by using Tensorflow. The [German Traffic Sign Recognition Benchmark](https://benchmark.ini.rub.de/?section=gtsrb&subsection=news) (GTSRB) dataset was used as training data for the neural network.

## Language (Natural Language Processing)
* [Parser](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Language/parser):
A common task in natural language processing is parsing, the process of determining the structure of a sentence. In this project, an AI was implemented to use the context-free grammar formalism and [nltk](https://www.nltk.org/index.html) library to parse English sentences to determine their structure and extract noun phrases.
* [Questions](https://github.com/tuanna52/CS50-Introduction-to-Artificial-Intelligence/tree/main/Language/questions):
Question Answering is a field within natural language processing focused on designing systems that can answer questions. In this project, an AI was implemented to answer questions using TF-IDF (Term Frequency – Inverse Document Frequency) algoritm and [nltk](https://www.nltk.org/index.html) library.
