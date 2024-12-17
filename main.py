import pygame
import sys
from setting import *
from controller import Game


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My TD Game!!")

clock = pygame.time.Clock()


game = Game()

running = True


while running:
    # Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] and game.run == False:
            game.reset()

        # Trigger Event
        if game.run:
            game.event_trigger(event)

    # Update
    if game.run:
        game.update()

    # Drawing
    if game.run or game.wait:
        game.draw(screen)
    

    pygame.display.update()
    clock.tick(FPS)
