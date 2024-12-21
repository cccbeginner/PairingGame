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
        self.success = False
        self.level = 0
        self.remain_pairs = 1
        self.init_model()

        self.color_btn = ColorButtonList()
        for i in range(0, len(self.possible_colors)):
            color = self.possible_colors[i]
            self.color_btn.add_button(SCREEN_WIDTH//2 - 120 +i*60, SCREEN_HEIGHT - 80, 40, 40, color)

        self._characterTimer = list[Timer]
        self.init_level()

        # Add background sound
        pygame.mixer.init()
        sound1 = pygame.mixer.Sound("Sound/bg-music.wav")  # 替換為第一個 WAV 文件名稱
        sound2 = pygame.mixer.Sound("Sound/bg-snow.mp3")  # 替換為第二個 WAV 文件名稱
        sound1.play(loops=-1, fade_ms=2000)
        sound2.play(loops=-1, fade_ms=2000)

        # Load sound effects
        self.sound_shoot = pygame.mixer.Sound("Sound/shoot.mp3")
        self.sound_shoot.set_volume(0.8)
        self.sound_pair = pygame.mixer.Sound("Sound/pair.mp3")
        self.sound_game_over = pygame.mixer.Sound("Sound/game-over.mp3")

    def init_level(self):
        self.remain_pairs = len(LEVEL[self.level]) // 2
        self._characterTimer = []
        for spawn_time, sex, speed in LEVEL[self.level]:
            f = lambda sex=sex, speed=speed : self.addCharacter(sex, speed)
            self._characterTimer.append(Timer(spawn_time, f, False))
            self._characterTimer[-1].start()

    def check_if_done(self):
        if not self.tree.alive:
            self.wait = True
            self.run = False
            self.sound_game_over.play()
        if self.remain_pairs == 0:
            self.wait = True
            self.run = False
            self.sound_game_over.play()

    def update(self):
        self.moveCharacterLine()
        self.moveUpCharacterPairs()
        for timer in self._characterTimer:
            timer.update()
        self.tree.shake(self.character_line.numCharactersWaiting*0.1)
        
        for arrow in self.arrows:
            arrow.update()
            if arrow.has_arrive_target():
                self.setCharacterColor(arrow.color)
                self.sound_shoot.play()
        self.arrows = [arrow for arrow in self.arrows if not arrow.has_arrive_target()]

        self.check_if_done()

    def draw(self, screen : pygame.Surface):
        self.view.draw_background(screen)
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
        
        self.draw_text(screen, f"Level {self.level+1}", 50, WHITE, False, SCREEN_WIDTH-150, 50)

        if self.run == False:
            if self.remain_pairs > 0:
                self.draw_text(screen, f"Oops your tree got attack!", 50, YELLOW, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2-50)
                self.draw_text(screen, "Press R to continue!", 50, RED, False, SCREEN_WIDTH/2-25, SCREEN_HEIGHT/2+50)
            else:
                self.draw_text(screen, f"You successfully pass Level {self.level+1}!", 50, RED, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50)
                self.draw_text(screen, "Press R to continue!", 50, RED, False, SCREEN_WIDTH/2-25, SCREEN_HEIGHT/2+50)

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
        if self.remain_pairs == 0:
            self.level += 1
        self.init_level()
        self.init_model()
    
    def init_model(self):
        self.jupiter = Jupiter(100, 100)
        self.tree = Tree(1, 100)
        self.character_line = CharacterLine(220)
        self.character_pairs : list[CharacterPair] = []
        self.arrows : list[Arrow] = []

    def addArrow(self, x, y, target: Character, color : pygame.Color) -> None:
        self.arrows.append(Arrow(x+100, y+120, target, color))
    
    def addCharacter(self, sex: int, speed:int):
        print(sex, speed)
        self.character_line.addCharacter(sex, False, 70, 160, speed)

    def moveCharacterLine(self) -> None:
        self.character_line.moveAllCharacter()
    
    def setCharacterColor(self, color: pygame.Color) -> None:
        newCharacterPair = self.character_line.setCharacterColor(color)
        self.character_line.movePointer()
        if newCharacterPair != None:
            self.character_pairs.append(newCharacterPair)
            self.remain_pairs -= 1
            self.sound_pair.play()
    
    def moveUpCharacterPairs(self) -> None:
        for i in range(len(self.character_pairs)-1, -1, -1):
            self.character_pairs[i].moveUp()
            if self.character_pairs[i].isTooHigh():
                self.character_pairs.pop(i)