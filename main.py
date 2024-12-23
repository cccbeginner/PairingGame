import pygame
import sys
from setting import *
from controller import Game


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My TD Game!!")

clock = pygame.time.Clock()
delta = -1

game = Game()

running = True


while running:
    # Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False

        # Trigger Event
        game.event_trigger(event)


    # Drawing
    game.update(delta/1000)
    game.draw(screen)
    

    pygame.display.update()

    if delta == -1: # game just start
        delta = clock.tick(FPS)
        delta = clock.tick(FPS)
    else:
        delta = clock.tick(FPS)
