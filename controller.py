from __future__ import annotations
import pygame
import random
from setting import *
from view import *
from tools import *
from color_button import *

class Game:
    instance : Game = None
    def __init__(self):
        self.scene_stack : list[Scene] = [StartScene()]
        if Game.instance == None:
            Game.instance = self

        # Add background sound
        pygame.mixer.init()
        sound1 = pygame.mixer.Sound("Sound/bg-music.wav")  # 替換為第一個 WAV 文件名稱
        sound2 = pygame.mixer.Sound("Sound/bg-snow.mp3")  # 替換為第二個 WAV 文件名稱
        sound1.play(loops=-1, fade_ms=2000)
        sound2.play(loops=-1, fade_ms=2000)

    @property
    def active_scene(self) -> Scene | None:
        if len(self.scene_stack) == 0:
            return None
        return self.scene_stack[-1]

    def update(self, delta:float):
        scene = self.active_scene
        if scene != None:
            scene.update(delta)

    def draw(self, screen:pygame.Surface):
        scene = self.active_scene
        if scene != None:
            scene.draw(screen)

    def event_trigger(self, event: pygame.event.Event):
        scene = self.active_scene
        if scene != None:
            scene.event_trigger(event)

    def load_prev_scene(self):
        self.scene_stack.pop()
    
    def load_scene(self, new_scene: Scene):
        self.scene_stack.append(new_scene)


# this should be abstract, but python don't have abstract class
class Scene:
    def __init__(self):
        self.prev_scene : Scene = None
    
    def load_prev_scene(self):
        Game.instance.load_prev_scene()
    
    def load_scene(self, scene: Scene):
        Game.instance.load_scene(scene)
    
    def update(self, delta:float):
        pass

    def draw(self, screen:pygame.Surface):
        pass

    def event_trigger(self, event:pygame.event.Event):
        pass
        

class StartScene(Scene):
    def __init__(self):
        super().__init__()
        self.button_load_level = ColorButton(SCREEN_WIDTH//2-100, 320, 200, 80, (200,200,200), "Stage Mode", cooldown=0)
        self.button_load_score = ColorButton(SCREEN_WIDTH//2-100, 420, 200, 80, (200,200,200), "Challenge Mode", cooldown=0)
        self.jupiter = Jupiter(100, 100)
        self.tree = Tree(1, 100)
    
    def update(self, delta: float):
        pass

    def draw(self, screen: pygame.Surface):
        View.instance.draw_background(screen)
        View.instance.draw_text(screen, "Welcome to Cupid's", 90, (220, 180, 0), False, SCREEN_WIDTH//2, 80)
        View.instance.draw_text(screen, "Christmas Quest!", 90, (220, 180, 0), False, SCREEN_WIDTH//2, 190)
        self.button_load_level.draw(screen)
        self.button_load_score.draw(screen)
        View.instance.draw_jupiter(self.jupiter, screen)
        View.instance.draw_tree(self.tree, screen)

    def event_trigger(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_load_level.is_clicked(event):
                self.load_scene(LevelScene())
            elif self.button_load_score.is_clicked(event):
                self.load_scene(ScoreScene())
        

class LevelScene(Scene):
    deltaTime = 0

    def __init__(self):
        self.status = 1 # 0->wait, 1->run, 2->pause in tutorial
        self.status_tutorial = 0 # -1->run but in tutorial, 0->no-tutorial, 1->shoot arrow, 2->shoot again, 3-> make pair
        self.finish_tutorial = False

        self.jupiter : Jupiter = None
        self.tree : Tree = None
        self.character_line : CharacterLine = None
        self.character_pairs : list[CharacterPair] = []
        self.arrows : list[Arrow] = []
        self.success = False
        self.level = 0
        self.remain_pairs = 1
        self.init_model()

        self.back_btn = ColorButton(50, 50, 70, 50, (200, 200, 200), "Back", cooldown=0)
        self.color_btn_list = ColorButtonList()
        for i in range(0, len(BTN_COLORS)):
            color = BTN_COLORS[i]
            self.color_btn_list.add_button(SCREEN_WIDTH//2 - 120 +i*60, SCREEN_HEIGHT - 80, 40, 40, color)

        self._timers = list[Timer]
        self.init_level()


        # Load sound effects
        self.sound_shoot = pygame.mixer.Sound("Sound/shoot.mp3")
        self.sound_shoot.set_volume(0.8)
        self.sound_pair = pygame.mixer.Sound("Sound/pair.mp3")
        self.sound_game_over = pygame.mixer.Sound("Sound/game-over.mp3")

    def init_level(self):
        self.remain_pairs = len(LEVEL[self.level]) // 2
        self._timers = []
        for spawn_time, sex, speed in LEVEL[self.level]:
            f = lambda sex=sex, speed=speed : self.addCharacter(sex, speed)
            self._timers.append(Timer(spawn_time, f, False))

        # init tutorial timer
        if self.level == 0 and not self.finish_tutorial:
            f1 = lambda t_status=1 : self.use_tutorial(t_status)
            f2 = lambda t_status=2 : self.use_tutorial(t_status)
            f3 = lambda t_status=3 : self.use_tutorial(t_status)
            self._timers.append(Timer(5, f1, False))
            self._timers.append(Timer(8, f2, False))
            self._timers.append(Timer(9, f3, False))
            self.status_tutorial = -1
        else:
            self.status_tutorial = 0

    def check_if_done(self):
        if not self.tree.alive:
            self.status = 0
            self.sound_game_over.play()
        if self.remain_pairs == 0:
            self.status = 0
            self.sound_game_over.play()

    def update(self, delta: float):
        if self.status == 0:
            self.moveCharacterLine()
            self.moveUpCharacterPairs()
            for timer in self._timers:
                timer.update(delta)
            for arrow in self.arrows:
                arrow.update()
                if arrow.has_arrive_target():
                    self.setCharacterColor(arrow.color)
            self.arrows = [arrow for arrow in self.arrows if not arrow.has_arrive_target()]

        elif self.status == 1:
            self.moveCharacterLine()
            self.moveUpCharacterPairs()
            for timer in self._timers:
                timer.update(delta)
            self.tree.shake(self.character_line.numCharactersWaiting*0.1)
            
            for arrow in self.arrows:
                arrow.update()
                if arrow.has_arrive_target():
                    self.setCharacterColor(arrow.color)
                    self.sound_shoot.play()
            self.arrows = [arrow for arrow in self.arrows if not arrow.has_arrive_target()]

            self.check_if_done()
        elif self.status == 2:
            pass

    def draw(self, screen : pygame.Surface):
        View.instance.draw_background(screen)
        self.color_btn_list.draw(screen)
        self.back_btn.draw(screen)
        
        View.instance.draw_jupiter(self.jupiter, screen)
        View.instance.draw_tree(self.tree, screen)
        for character in self.character_line.characters:
            View.instance.draw_character(character, screen)
        for character_pair in self.character_pairs:
            View.instance.draw_character_with_wings(character_pair.character1, screen)
            View.instance.draw_character_with_wings(character_pair.character2, screen)

        for arrow in self.arrows:
            View.instance.draw_arrow(arrow, screen)
        
        View.instance.draw_text(screen, f"Level {self.level+1}", 50, WHITE, False, SCREEN_WIDTH-150, 50)

        if self.status == 0:
            if self.remain_pairs > 0:
                View.instance.draw_text(screen, f"Oops your tree got attack!", 50, RED, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2-50)
                View.instance.draw_text(screen, "Press R to continue!", 50, YELLOW, False, SCREEN_WIDTH/2-25, SCREEN_HEIGHT/2+50)
            elif self.level+1 < len(LEVEL):
                View.instance.draw_text(screen, f"You successfully pass Level {self.level+1}!", 50, WHITE, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50)
                View.instance.draw_text(screen, "Press R to continue!", 50, YELLOW, False, SCREEN_WIDTH/2-25, SCREEN_HEIGHT/2+50)
            else:
                View.instance.draw_text(screen, f"OMG you successfully pass All Levels!", 50, WHITE, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50)
                View.instance.draw_text(screen, "Press R back to home page!", 50, YELLOW, False, SCREEN_WIDTH/2-25, SCREEN_HEIGHT/2+50)
        elif self.status == 2:
            if self.status_tutorial == 1:
                View.instance.draw_text(screen, f"Those are color buttons.", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2-50)
                View.instance.draw_text(screen, f"Press the button to color the first character.", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2+40)
                View.instance.draw_pointer(screen, 540, 520, RED, 50, -90)
            elif self.status_tutorial == 2:
                View.instance.draw_text(screen, f"A girl and a boy could make a couple.", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2-50)
                View.instance.draw_text(screen, f"Press the same button to color the boy", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2+40)
                View.instance.draw_pointer(screen, 540, 520, RED, 50, -90)
            elif self.status_tutorial == 3:
                View.instance.draw_text(screen, f"If a boy and a girl has same color cloth,", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2-50)
                View.instance.draw_text(screen, f"they will flying high. Have fun!", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2+40)
                View.instance.draw_pointer(screen, 800, 300, RED, 50, 60)


    def event_trigger(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_btn.is_clicked(event):
                self.load_prev_scene()
            if self.status == 0:
                pass
            elif self.status == 1:
                if self.status_tutorial == -1:
                    pass
                else:
                    color = self.color_btn_list.get_color_clicked(event)
                    if color != None:
                        cur_ch = self.character_line.current_character
                        if cur_ch != None:
                            self.addArrow(self.jupiter.x, self.jupiter.y, cur_ch, color)
            elif self.status == 2:
                if self.status_tutorial == 1 or self.status_tutorial == 2:
                    color = self.color_btn_list.get_color_clicked(event)
                    if color == RED:
                        cur_ch = self.character_line.current_character
                        self.addArrow(self.jupiter.x, self.jupiter.y, cur_ch, color)
                        self.next_tutorial()
                elif self.status_tutorial == 3:
                    self.next_tutorial()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.reset()

    def reset(self):
        self.status = 1
        if self.remain_pairs == 0:
            self.level += 1
        if self.level == len(LEVEL):
            self.load_prev_scene()
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

    def use_tutorial(self, tutor_status):
        self.status = 2
        self.status_tutorial = tutor_status

    def next_tutorial(self):
        if self.status_tutorial == 1 or self.status_tutorial == 2:
            self.status = 1
            self.status_tutorial = -1
        elif self.status_tutorial == 3:
            self.status = 1
            self.status_tutorial = 0
            self.finish_tutorial = True
        

class ScoreScene(Scene):
    deltaTime = 0

    def __init__(self):
        self.status = 1 # 0->wait, 1->run
        self.finish_tutorial = False

        self.jupiter : Jupiter = None
        self.tree : Tree = None
        self.character_line : CharacterLine = None
        self.character_pairs : list[CharacterPair] = []
        self.arrows : list[Arrow] = []
        self.success = False
        self.pairs = 0
        self.init_model()

        self.back_btn = ColorButton(50, 50, 70, 50, (200, 200, 200), "Back", cooldown=0)
        self.color_btn_list = ColorButtonList()
        for i in range(0, len(BTN_COLORS)):
            color = BTN_COLORS[i]
            self.color_btn_list.add_button(SCREEN_WIDTH//2 - 120 +i*60, SCREEN_HEIGHT - 80, 40, 40, color)

        self._gen_charcter_timer = Timer(2, self.gen_random_character, True)

        # Load sound effects
        self.sound_shoot = pygame.mixer.Sound("Sound/shoot.mp3")
        self.sound_shoot.set_volume(0.8)
        self.sound_pair = pygame.mixer.Sound("Sound/pair.mp3")
        self.sound_game_over = pygame.mixer.Sound("Sound/game-over.mp3")
    
    def gen_random_character(self):
        sex = random.randint(0,1)
        boyCnt = len([ch for ch in self.character_line.characters if ch.sex == 1])
        girlCnt = len([ch for ch in self.character_line.characters if ch.sex == 0])
        if boyCnt - girlCnt >= 3:
            sex = 0
        elif girlCnt - boyCnt >= 3:
            sex = 1

        speed = random.uniform(0.5, 1) * (self.pairs*0.15 + 1)
        self.addCharacter(sex, speed)

    def check_if_done(self):
        if not self.tree.alive:
            self.status = 0
            self.sound_game_over.play()

    def update(self, delta: float):
        if self.status == 0:
            self.moveCharacterLine()
            self.moveUpCharacterPairs()
            for arrow in self.arrows:
                arrow.update()
                if arrow.has_arrive_target():
                    self.setCharacterColor(arrow.color)
            self.arrows = [arrow for arrow in self.arrows if not arrow.has_arrive_target()]

        elif self.status == 1:
            self.moveCharacterLine()
            self.moveUpCharacterPairs()
            self._gen_charcter_timer.update(delta)
            self.tree.shake(self.character_line.numCharactersWaiting*0.1)
            
            for arrow in self.arrows:
                arrow.update()
                if arrow.has_arrive_target():
                    self.setCharacterColor(arrow.color)
                    self.sound_shoot.play()
            self.arrows = [arrow for arrow in self.arrows if not arrow.has_arrive_target()]

            self.check_if_done()
        elif self.status == 2:
            pass

    def draw(self, screen : pygame.Surface):
        View.instance.draw_background(screen)
        self.color_btn_list.draw(screen)
        self.back_btn.draw(screen)
        
        View.instance.draw_jupiter(self.jupiter, screen)
        View.instance.draw_tree(self.tree, screen)
        for character in self.character_line.characters:
            View.instance.draw_character(character, screen)
        for character_pair in self.character_pairs:
            View.instance.draw_character_with_wings(character_pair.character1, screen)
            View.instance.draw_character_with_wings(character_pair.character2, screen)

        for arrow in self.arrows:
            View.instance.draw_arrow(arrow, screen)
        
        View.instance.draw_text(screen, f"Pairs: {self.pairs}", 50, WHITE, False, SCREEN_WIDTH-120, 50)

        if self.status == 0:
            View.instance.draw_text(screen, f"You have successfully make {self.pairs} pairs!", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2-50)
            View.instance.draw_text(screen, "Press R to continue!", 50, WHITE, False, SCREEN_WIDTH/2-25, SCREEN_HEIGHT/2+50)

    def event_trigger(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_btn.is_clicked(event):
                self.load_prev_scene()
            if self.status == 0:
                pass
            elif self.status == 1:
                color = self.color_btn_list.get_color_clicked(event)
                if color != None:
                    cur_ch = self.character_line.current_character
                    if cur_ch != None:
                        self.addArrow(self.jupiter.x, self.jupiter.y, cur_ch, color)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.reset()

    def reset(self):
        self.status = 1
        self.init_model()
    
    def init_model(self):
        self.pairs = 0
        self.jupiter = Jupiter(100, 100)
        self.tree = Tree(1, 100)
        self.character_line = CharacterLine(220)
        self.character_pairs : list[CharacterPair] = []
        self.arrows : list[Arrow] = []

    def addArrow(self, x, y, target: Character, color : pygame.Color) -> None:
        self.arrows.append(Arrow(x+100, y+120, target, color))
    
    def addCharacter(self, sex: int, speed:int):
        self.character_line.addCharacter(sex, False, 70, 160, speed)

    def moveCharacterLine(self) -> None:
        self.character_line.moveAllCharacter()
    
    def setCharacterColor(self, color: pygame.Color) -> None:
        newCharacterPair = self.character_line.setCharacterColor(color)
        self.character_line.movePointer()
        if newCharacterPair != None:
            self.character_pairs.append(newCharacterPair)
            self.pairs += 1
            self.sound_pair.play()
    
    def moveUpCharacterPairs(self) -> None:
        for i in range(len(self.character_pairs)-1, -1, -1):
            self.character_pairs[i].moveUp()
            if self.character_pairs[i].isTooHigh():
                self.character_pairs.pop(i)
