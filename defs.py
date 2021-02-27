import math
import numpy as np
import scipy.special
import random
import pygame
import math


DISPLAY_W = 960
DISPLAY_H = 540
FPS = 60
FONT_SIZE = 18
FONT_COLOR = (40, 40, 40)
BG = 'bg.png'
BIRD = 'bird.png'
PIPE = 'Pipe.png'

PIPE_SPEED = 100/1000
PIPE_DONE = 1
PIPE_MOVING = 0
PIPE_UPPER = 1
PIPE_LOWER = 0
PIPE_ADD_GAP = 160
PIPE_MIN = 80
PIPE_MAX = 500
PIPE_START_X = DISPLAY_W
PIPE_GAP_SIZE = 160
PIPE_FIRST = 400

BIRD_START_SPEED = -0.32
BIRD_START_X = 200
BIRD_START_Y = 200
BIRD_ALIVE = 1
BIRD_DEAD = 0
GRAVITY = 0.001
GENERATION_SIZE = 500

MAX_DISTANCE = abs(220-420)+abs(20-420)

MUTATION_CHANCE = 0.4
MUTATION_SIZE = 0.5
ELITISM = 0.6
EGAL = 0.3

HIDDEN_ACT = 1
OUTPUT_ACT = 1


def activationFunction(selection, vector):
    output_vec = vector
    if selection == 1:
        # sigmoid
        sigmoid = lambda x: scipy.special.expit(x)
        output_vec = np.array([sigmoid(t) for t in vector])
    if selection == 2:
        # relu
        output_vec[output_vec < 0] = 0
    if selection == 3:
        # gaussian
        gaussian = lambda x: math.exp(-(x**x))
        output_vec = np.array([gaussian(t) for t in vector])
    if selection == 4:
        # binary
        output_vec[output_vec<=0] = 0
        output_vec[output_vec>0] = 1

    return output_vec

def mutate(x):
    for y in np.nditer(x, op_flags = ['readwrite']):
        if random.random() < MUTATION_CHANCE:
            # random_sample() : half open interval [0.0, 1.0)
            y = np.random.random_sample() - MUTATION_SIZE
    return x

def crossOver(x,y,selection):
    num_elements = x.size
    num_rows = x.shape[0]
    num_cols = x.shape[1]

    x = x.flatten()
    y = y.flatten()

    x_list = x.tolist()
    y_list = y.tolist()

    return_list = [0] * num_elements

    if selection == 1:
        #one-point crossover
        random_split_point = random.randint(1, num_elements-1)

        for i in range(len(x_list)):
            if i < random_split_point:
                return_list[i] = x_list[i]
            else:
                return_list[i] = y_list[i]

    if selection == 2:
        #two-point crossover
        random_split_point1 = random.randint(1, num_elements - 1)
        random_split_point2 = random.randint(random_split_point1, num_elements - 1)
        while random_split_point1 == random_split_point2:
            random_split_point1 = random.randint(1, num_elements - 1)
            random_split_point2 = random.randint(random_split_point1, num_elements - 1)

        for i in range(len(x_list)):
            if i < random_split_point1:
                return_list[i] = x_list[i]
            if random_split_point1 <= i < random_split_point2:
                return_list[i] = y_list[i]
            if random_split_point2 <= i:
                return_list[i] = x_list[i]

    if selection == 3:
        #arithmetic crossover
        for i in range(len(x_list)):
            return_list[i] = (x_list[i] + y_list[i])/2

    if selection == 4:
        #uniform crossover
        for i in range(len(x_list)):
            if np.random.random_sample() < 0.5:
                return_list[i] = x_list[i]
            else:
                return_list[i] = y_list[i]

    return_arr = np.reshape(return_list, (num_rows, num_cols))
    return return_arr





