# Rock Paper Scissors

This is my solution to https://www.freecodecamp.org/learn/machine-learning-with-python/machine-learning-with-python-projects/rock-paper-scissors challenge.

The [algorithm](/RPS.py) here is built on the idea of markov chains and markov decision process. An introduction to markov chains and decision process can be accessed [here](https://towardsdatascience.com/introduction-to-reinforcement-learning-markov-decision-process-44c533ebf8da).
This algorithm is a traditional statistical analysis and sequence modeling approach designed to play a game of Rock-Paper-Scissors (RPS). It aims to predict the opponent's next move in the RPS game by leveraging patterns in the opponent's play history.

#### How it works:

1. Data Collection: It builds a history of the opponent's plays for sequences of different lengths (orders). Eg, given the state "RP", it might track and observe that the opponent plays "S" 20% of the time, "P" 40% of the time and "R" 40% of the time.

2. Pattern Recognition: It analyzes these sequences to determine the most likely next move the opponent will make. This is done by counting the occurrences of each possible next move following a given sequence.

3. Decision Making: Based on the recognized patterns, it predicts the opponent's next move and selects the best counter-move (Rock beats Scissors, Paper beats Rock, Scissors beat Paper).

#### Example

In this algorithm:
If the opponent's previous plays are "RP", the algorithm updates the play list to reflect what usually follows "RP" (e.g., "S" most of the time).
It then uses this historical data to predict the opponent's next move and decides the best counter-move (e.g., if "S" is predicted, the best counter-move is "R")

#### A little more explanation

The `order` in the algorithm corresponds to the number of previous plays considered, similar to the concept of the order in a Markov chain, where a first-order Markov chain depends only on the current state, a second-order chain depends on the current state and the previous state, and so on.
`samples_to_use` is the focus length. Only recent previous plays within this focus length are considered when making predictions.
The `play_list` is used to track how frequently certain sequences are followed by specific plays, similar to how a Markov chain would use transition probabilities to predict the next state.

#### To Do

- Write better comments and docstrings to explain the functions.
- The algorithm updates its predictions based on a fixed rule (most frequent next move) without exploring or exploiting different strategies to maximize long-term rewards. This is where a reinforcement learning approach can be explored.
- The current implementation might become less efficient as the `order` increases because the number of possible sequences grows exponentially. Optimizations could be considered to handle large datasets more efficiently.

#### Possible Tip if you're working on something similar:

You can make multiple algorithms that play concurrently with the opponent then, using a focus length, select an algorithm with the most scores within the focus length to keep playing with the opponent. [see here](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7431549/#CR10).
