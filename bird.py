# import pygame
# import random
from defs import *
from nnet import Nnet

class Bird:

    def __init__(self, gameDisplay):
        self.nnet = Nnet(10)
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.time_lived = 0
        self.set_position(BIRD_START_X, BIRD_START_Y)
        self.fitness = 0

    def reset(self):
        self.state = BIRD_ALIVE
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.set_position(BIRD_START_X, BIRD_START_Y)

    def fitnessFunc(self, pipe):
        dist_to_gap = 0
        if pipe.pipe_type == PIPE_UPPER:
            dist_to_gap = pipe.rect.bottom + PIPE_GAP_SIZE / 2
        else:
            dist_to_gap = pipe.rect.top - PIPE_GAP_SIZE / 2

        self.fitness = -(abs(self.rect.centery-dist_to_gap))


    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, dt):
        distance = 0
        new_speed = 0
        distance = (self.speed*dt) + (0.5 * GRAVITY * dt * dt)
        new_speed = self.speed + (GRAVITY * dt)

        self.rect.centery += distance
        self.speed = new_speed

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0


    def jump(self, pipes):
        input = self.input(pipes)
        y_or_n = self.nnet.getMove(input,HIDDEN_ACT,OUTPUT_ACT)
        if y_or_n:
            self.speed = BIRD_START_SPEED

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self, pipes):
        if self.rect.bottom > DISPLAY_H:
            self.state = BIRD_DEAD
        else:
            self.check_hits(pipes)

    def check_hits(self, pipes):
        for p in pipes:
            if p.rect.colliderect(self.rect):
                self.state = BIRD_DEAD
                self.fitnessFunc(p)
                break

    def update(self, dt, pipes):
        if self.state == BIRD_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.jump(pipes)
            self.draw()
            self.check_status(pipes)

    def input(self, pipes):
        # debug
        # x = 99999
        # y = 0
        # height = 9999
        # for p in pipes:
        #     if p.pipe_type == PIPE_UPPER and y > p.rect.right > self.rect.left:
        #         x = p.rect.centerx
        #         y = p.rect.top
        #         height = p.rect.height

        closest_x = DISPLAY_W*2
        closest_y = 0
        for p in pipes:
            if p.pipe_type == PIPE_UPPER and closest_x > p.rect.right > self.rect.left:
                closest_x = p.rect.right
                closest_y = p.rect.bottom

        # distance = abs(self.rect.centerx - (closest_x-20))+abs(self.rect.centery - (closest_y + PIPE_GAP_SIZE/2))
        # input = [(distance/MAX_DISTANCE)]
        vertical = self.rect.centery - closest_y+PIPE_GAP_SIZE/2
        input = [(((closest_x-self.rect.centerx)/DISPLAY_W)*0.99) + 0.01,
                 (((vertical+420)/800)*0.99) + 0.01
                 ]
        return input

    @staticmethod
    def crossover(b1,b2,gameDisplay):
        new = Bird(gameDisplay)
        new.nnet.wih = b1.nnet.wih
        new.nnet.who = b1.nnet.who
        new.nnet.crossoverWeights(b2.nnet,2)
        return new



class BirdCollection:

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.birds = []
        self.create_new_generation()

    def create_new_generation(self):
        self.birds = []
        for i in range(0, GENERATION_SIZE):
            self.birds.append(Bird(self.gameDisplay))

    def update(self, dt, pipes):
        num_alive = 0
        for b in self.birds:
            b.update(dt, pipes)
            if b.state == BIRD_ALIVE:
                num_alive += 1
        return num_alive

    def evolve_population(self):
        for b in self.birds[0:GENERATION_SIZE]:
            b.fitness += b.time_lived * PIPE_SPEED

        self.birds.sort(key=lambda x: x.fitness, reverse=True)
        elite_num = int(len(self.birds)*ELITISM)
        elite_birds = self.birds[0:elite_num]
        egal_birds = self.birds[elite_num:]
        egal_num = int(len(self.birds)*EGAL)

        for b in egal_birds:
            b.nnet.mutateWeights()

        evolved_birds = []

        ind = np.random.choice(np.arange(len(egal_birds)), egal_num, replace=False)
        for i in ind:
            evolved_birds.append(egal_birds[i])

        evolved_birds.extend(elite_birds)
        extra = len(self.birds)-len(evolved_birds)

        while len(evolved_birds) < len(self.birds):
            indx = np.random.choice(np.arange(len(elite_birds)), 2, replace=False)
            new_bird = Bird.crossover(elite_birds[indx[0]], elite_birds[indx[1]], self.gameDisplay)
            if random.random() < 0.3:
                new_bird.nnet.mutateWeights()

            evolved_birds.append(new_bird)

        for i in evolved_birds:
            i.reset()

        self.birds = evolved_birds
















