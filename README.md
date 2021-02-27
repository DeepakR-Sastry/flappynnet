# flappynnet
Implemented a bot that learns to play flappy bird using the genetic algorithm and a neural net implementation. 

Description of the neural network:
The neural network's structure comprises of one input layer, one hidden layer and an output layer with the number of hidden nodes being 2, 10, 1 respectively.
That is, the number of features of the neural network is 2: distance from the center of the gap of the pipes and the height from the bottom. 
Several activation functions have been added but the sigmoid function seems to be the most promising one.
Fitness of a bird is determined by how close it was to the gap of the pipes.
Evolution is a combination of selection, crossovers and mutation. Several types of crossovers are also implemented (single-point, double-point, arithmetic and uniform crossover)
whilst mutation is completely random.


Credit:(game code) Bluefever Software: https://www.youtube.com/channel/UCFkfibjxPzrP0e2WIa8aJCg 
