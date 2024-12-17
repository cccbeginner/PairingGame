import pygame
import random
from setting import *
from view import *
from tools import *
from color_button import *

class Game:
    deltaTime = 0

    def __init__(self):
        self.run = True
        self.wait = False

        self.possible_colors : pygame.Color = [RED, GREEN, YELLOW, BLUE, PURPLE]
        self.view = View(self.possible_colors + [WHITE])

        self.jupiter : Jupiter = None
        self.tree : Tree = None
        self.character_line : CharacterLine = None
        self.character_pairs : list[CharacterPair] = []
        self.arrows : list[Arrow] = []
        self.init_model()

        self.color_btn = ColorButtonList()
        for i in range(0, len(self.possible_colors)):
            color = self.possible_colors[i]
            self.color_btn.add_button(SCREEN_WIDTH//2 - 120 +i*60, SCREEN_HEIGHT - 80, 40, 40, color)

        self._addCharacterTimer = Timer(1.5, self.addRandomCharacter, True)
        self._addCharacterTimer.start()

        self.cnt_successful_pair = 0

    def addRandomCharacter(self):
        boy_cnt = len([ch for ch in self.character_line.characters if ch.sex == 1])
        girl_cnt = len(self.character_line.characters) - boy_cnt
        speed = random.uniform(0.5, 1) * (1 + 0.15 * self.cnt_successful_pair)
        if boy_cnt - girl_cnt >= 3:
            self.addCharacter(0, False, 70, 160, speed)
        elif girl_cnt - boy_cnt >= 3:
            self.addCharacter(1, False, 70, 160, speed)
        else:
            self.addCharacter(random.randint(0,1), False, 70, 160, speed)

    def update(self):
        self.moveCharacterLine()
        self.moveUpCharacterPairs()
        self._addCharacterTimer.update()
        self.tree.shake(self.character_line.numCharactersWaiting*0.1)
        if not self.tree.alive:
            self.wait = True
            self.run = False
        
        for arrow in self.arrows:
            arrow.update()
            if arrow.has_arrive_target():
                self.setCharacterColor(arrow.color)
        self.arrows = [arrow for arrow in self.arrows if not arrow.has_arrive_target()]

    def draw(self, screen : pygame.Surface):
        screen.fill(BLACK)
        self.color_btn.draw(screen)
        
        self.view.draw_jupiter(self.jupiter, screen)
        self.view.draw_tree(self.tree, screen)
        for character in self.character_line.characters:
            self.view.draw_character(character, screen)
        for character_pair in self.character_pairs:
            self.view.draw_character_with_wings(character_pair.character1, screen)
            self.view.draw_character_with_wings(character_pair.character2, screen)

        for arrow in self.arrows:
            self.view.draw_arrow(arrow, screen)
        
        
        self.draw_text(screen, f"{self.cnt_successful_pair}", 50, WHITE, False, SCREEN_WIDTH-100, 100)

        if self.run == False:
            self.draw_text(screen, f"Game Over! You successfully make {self.cnt_successful_pair} pairs!", 50, RED, False, SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2)
            self.draw_text(screen, "Press R to Restart", 50, RED, False, SCREEN_WIDTH/2-25, SCREEN_HEIGHT/2+100)

    def draw_text(self, surface, text, size, color, bold, x, y):
        font = pygame.font.SysFont("Arial", size=size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surface.blit(text_surface, text_rect)

    def event_trigger(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            color = self.color_btn.get_color_clicked(event)
            if color != None:
                cur_ch = self.character_line.current_character
                if cur_ch != None:
                    self.addArrow(self.jupiter.x, self.jupiter.y, cur_ch, color)

    def reset(self):
        self.wait = False
        self.run = True
        self.init_model()
    
    def init_model(self):
        self.jupiter = Jupiter(100, 100)
        self.tree = Tree(1, 100)
        self.character_line = CharacterLine(220)
        self.character_pairs : list[CharacterPair] = []
        self.arrows : list[Arrow] = []

    def addArrow(self, x, y, target: Character, color : pygame.Color) -> None:
        self.arrows.append(Arrow(x+100, y+120, target, color))
    
    def addCharacter(self, sex : int, sameSex: bool, width:int, height:int, speed:int) -> None:
        self.character_line.addCharacter(sex, sameSex, width, height, speed)
    
    def moveCharacterLine(self) -> None:
        self.character_line.moveAllCharacter()
    
    def setCharacterColor(self, color: pygame.Color) -> None:
        newCharacterPair = self.character_line.setCharacterColor(color)
        self.character_line.movePointer()
        if newCharacterPair != None:
            self.character_pairs.append(newCharacterPair)
            self.cnt_successful_pair += 1
    
    def moveUpCharacterPairs(self) -> None:
        for i in range(len(self.character_pairs)-1, -1, -1):
            self.character_pairs[i].moveUp()
            if self.character_pairs[i].isTooHigh():
                self.character_pairs.pop(i)