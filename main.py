# import pygame
from defs import *
from pipe import PipeCollection
from bird import BirdCollection

def label(data, title, font, x, y, gameDisplay):
    label = font.render('{} {}'.format(title, data), 1, FONT_COLOR)
    gameDisplay.blit(label, (x, y))
    return y

def update_label(gameDisplay, dt, time,num_iter,num_alive, font):
    y = 10
    gap = 20
    x = 20
    y = label(round(1000/dt,2), 'FPS', font, x, y + gap, gameDisplay)
    y = label(round(time/1000,2), 'Game Time', font, x, y + gap, gameDisplay)
    y = label(num_iter, 'Iteration', font, x, y + gap, gameDisplay)
    y = label(num_alive, 'Birds alive', font, x, y + gap, gameDisplay)


def run_game():
    pygame.init()
    gameDisplay = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
    pygame.display.set_caption('Flappy Bird')

    running = True
    bg = pygame.image.load(BG)
    label_font = pygame.font.SysFont("arial", FONT_SIZE)


    pipes = PipeCollection(gameDisplay)
    pipes.create_new_set()
    birds = BirdCollection(gameDisplay)


    clock = pygame.time.Clock()
    dt = 0
    game_time = 0

    num_iter = 0


    while running:
        dt = clock.tick(FPS)
        game_time += dt
        gameDisplay.blit(bg, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False

        pipes.update(dt)
        num_alive = birds.update(dt, pipes.pipes)

        if num_alive == 0:
            pipes.create_new_set()
            game_time = 0
            birds.evolve_population()
            num_iter += 1
        update_label(gameDisplay, dt, game_time,num_iter, num_alive, label_font)
        pygame.display.update()



if __name__ == '__main__':
    run_game()
