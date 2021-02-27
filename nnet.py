# import numpy as np
# import scipy.special
# import math
from defs import *

class Nnet:

    def __init__(self, num_hidden):
        self.num_input = 2
        self.num_hidden = num_hidden
        self.num_output = 1

        self.wih = np.random.uniform(-0.5, 0.5, size=(self.num_hidden, self.num_input))
        self.who = np.random.uniform(-0.5, 0.5, size=(self.num_output, self.num_hidden))


    def output(self, input_vec, selection1, selection2):
        input_vec = np.array(input_vec, ndmin=2).T
        hidden_output1 = np.dot(self.wih, input_vec)
        hidden_output2 = activationFunction(selection1, hidden_output1)
        final_output1 = np.dot(self.who, hidden_output2)
        final_output2 = activationFunction(selection2, final_output1)

        return final_output2

    def mutateWeights(self):
        self.wih = mutate(self.wih)
        self.who = mutate(self.who)

    def crossoverWeights(self, nnet2,selection):
        # set crossover criteria
        self.wih = crossOver(self.wih, nnet2.wih, selection)
        self.who = crossOver(self.who, nnet2.who, selection)



    def getMove(self, input_vec, selection1, selection2):
        output_vec = self.output(input_vec, selection1, selection2)
        finalDec = np.max(output_vec)
        if finalDec >= 0.5:
            return True
        else:
            return False






