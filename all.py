from __future__ import annotations
from setting import *
import pygame
import random
from typing import Dict
import math

class View:
    def __init__(self, possible_colors: list[pygame.Color] = []):
        self.img_tree = pygame.image.load("Image/tree.png")
        self.img_jupiter = pygame.image.load("Image/jupiter.png")
        self.img_boy = pygame.image.load("Image/boy.png")
        self.img_girl = pygame.image.load("Image/girl.png")
        self.img_boy_body = pygame.image.load("Image/boy_body.png")
        self.img_girl_body = pygame.image.load("Image/girl_body.png")
        self.img_wings = pygame.image.load("Image/wings.png")
        self.img_arrow = pygame.image.load("Image/arrow.png")
        self.color_img_boy_body: Dict[pygame.Color, pygame.Surface] = self.precalculate_color_img(possible_colors, self.img_boy_body)
        self.color_img_girl_body: Dict[pygame.Color, pygame.Surface] = self.precalculate_color_img(possible_colors, self.img_girl_body)
        self.color_img_arrow: Dict[pygame.Color, pygame.Surface] = self.precalculate_color_img(possible_colors, self.img_arrow)
        self.color_img_wings: Dict[pygame.Color, pygame.Surface] = self.precalculate_color_img(possible_colors, self.img_wings)

        
        # 建立雪花列表
        self.snowflakes : list[Snowflake] = [
            Snowflake(
                x=random.randint(0, SCREEN_WIDTH),
                y=random.randint(0, SCREEN_HEIGHT),
                radius=random.randint(2, 5),
                speed=random.randint(1, 3)
            ) for _ in range(50)
        ]
    
    def precalculate_color_img(self, possible_colors: list[pygame.Color], img_to_calculate: list[pygame.Color]) -> Dict[pygame.Color, pygame.Surface]:
        color_img_dict = {}
        for color in possible_colors:
            img = self.apply_color_shift(img_to_calculate, color)
            color_img_dict[color] = img
        return color_img_dict

    def draw_background(self, screen: pygame.Surface):
        screen.fill(BLACK)
        pygame.draw.rect(screen, SNOW,  pygame.Rect(0, CHARACTER_HEIGHT+100, SCREEN_WIDTH, 300))
        for snowflake in self.snowflakes:
            snowflake.fall(SCREEN_HEIGHT)
            snowflake.draw(screen)

    def draw_tree(self, tree : Tree, screen : pygame.Surface):
        image = pygame.transform.scale(self.img_tree, (200, 400))  # 調整圖片大小
        screen.blit(image, (tree.position, 200))

    def draw_jupiter(self, jupiter : Jupiter, screen : pygame.Surface):
        image = pygame.transform.scale(self.img_jupiter, (200, 200))  # 調整圖片大小
        screen.blit(image, (jupiter.x, jupiter.y))

    def draw_character(self, character : Character, screen : pygame.Surface):
        color = character.color
        if character.color == None: color = WHITE
        character_img : pygame.Surface
        body_img : pygame.Surface
        if character.sex == 0:
            character_img = self.img_girl
            if color in self.color_img_girl_body.keys():
                body_img = self.color_img_girl_body[color]
            else:
                body_img = self.img_girl_body
                body_img = self.apply_color_shift(body_img, color)
                self.color_img_girl_body[color] = body_img
        elif character.sex == 1:
            character_img = self.img_boy
            if color in self.color_img_boy_body.keys():
                body_img = self.color_img_boy_body[color]
            else:
                body_img = self.img_boy_body
                body_img = self.apply_color_shift(body_img, color)
                self.color_img_boy_body[color] = body_img

        character_img = pygame.transform.scale(character_img, (character.width, character.height))  # 調整圖片大小
        screen.blit(character_img, (character.x, character.y))

        body_img = pygame.transform.scale(body_img, (character.width, character.height))  # 調整圖片大小
        screen.blit(body_img, (character.x, character.y))

    def draw_character_with_wings(self, character : Character, screen : pygame.Surface):
        color = character.color
        if character.color == None: color = WHITE
        img_wings = self.color_img_wings[color]
        img_wings = pygame.transform.scale(img_wings, (character.width*2, 100))  # 調整圖片大小
        screen.blit(img_wings, (character.x - character.width * 0.5, character.y+30))

        self.draw_character(character, screen)

    def draw_arrow(self, arrow : Arrow, screen : pygame.Surface):
        image_arrow = self.color_img_arrow[arrow.color]        
        image_arrow = pygame.transform.scale(image_arrow, (120, 20))
        image_arrow = pygame.transform.rotate(image_arrow, -arrow.rotation)
        image_rect = image_arrow.get_rect(center=(arrow.x, arrow.y))
        screen.blit(image_arrow, image_rect.topleft)


# 差值顏色函數
    def apply_color_shift(self, image, color):
        """
        將圖片的每個像素與指定顏色進行差值計算。
        """
        shifted_image = image.copy()
        width, height = image.get_size()
        p = 0.5
        for x in range(width):
            for y in range(height):
                original_color = image.get_at((x, y))
                shifted_color = (
                    max(0, min(255, p * original_color.r + (1-p) * color[0])),
                    max(0, min(255, p * original_color.g + (1-p) * color[1])),
                    max(0, min(255, p * original_color.b + (1-p) * color[2])),
                    original_color.a  # 保留透明度
                )
                shifted_image.set_at((x, y), shifted_color)
        return shifted_image
    
    def draw_color_image(self, screen: pygame.Surface, img_url: str, color: pygame.Color, x:int, y:int, width:int, height:int):
        image = pygame.image.load(img_url)
        image = pygame.transform.scale(image, (width, height))  # 調整圖片大小
        shifted_image = self.apply_color_shift(image, color)
        screen.blit(shifted_image, (x, y))

    
    def draw_text(self, surface, text, size, color, bold, x, y):
        font = pygame.font.SysFont("Arial", size=size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surface.blit(text_surface, text_rect)

    def draw_pointer(self, screen: pygame.Surface, _x, _y, color=(255, 0, 0), size=20, angle=0):
        # 箭頭主體線條的長度和寬度
        line_length = size * 2
        line_width = size // 5

        # 箭頭頭部的大小
        head_length = size
        head_width = size // 2

        # 計算箭頭的旋轉角度（弧度）
        angle_rad = math.radians(angle)

        # 算出箭頭主體的終點位置
        end_x = _x + line_length * math.cos(angle_rad)
        end_y = _y - line_length * math.sin(angle_rad)

        # 畫箭頭主體
        pygame.draw.line(screen, color, (_x, _y), (end_x, end_y), line_width)

        # 算出箭頭頭部的兩個角
        left_x = end_x - head_length * math.cos(angle_rad - math.radians(30))
        left_y = end_y + head_length * math.sin(angle_rad - math.radians(30))

        right_x = end_x - head_length * math.cos(angle_rad + math.radians(30))
        right_y = end_y + head_length * math.sin(angle_rad + math.radians(30))

        # 畫箭頭頭部
        pygame.draw.polygon(screen, color, [(end_x, end_y), (left_x, left_y), (right_x, right_y)])


class Snowflake:
    def __init__(self, x: int, y: int, radius: int, speed: int) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed

    def fall(self, screen_height: int) -> None:
        self.y += self.speed
        if self.y > screen_height:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, SNOW, (self.x, self.y), self.radius)


class ColorButtonList:
    def __init__(self, color_buttons: list[ColorButton] = []):
        self._color_buttons = color_buttons

    def add_button(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]):
        self._color_buttons.append(ColorButton(x, y, width, height, color))

    def get_color_clicked(self, event: pygame.event.Event) -> tuple[int, int, int] | None:
        for btn in self._color_buttons:
            if btn.is_clicked(event):
                return btn.color
        return None
    
    def draw(self, screen: pygame.Surface) -> None:
        for btn in self._color_buttons:
            btn.draw(screen)

class ColorButton:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]) -> None:
        """
        初始化 Button 類別
        :param x: 按鈕的 X 座標
        :param y: 按鈕的 Y 座標
        :param width: 按鈕的寬度
        :param height: 按鈕的高度
        :param color: 按鈕的顏色 (RGB 格式)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.cooldown = COLOR_BTN_CD * 1000
        self.last_clicked_time = pygame.time.get_ticks()  # 確保開始時可以立即點擊

    def draw(self, screen: pygame.Surface) -> None:
        """
        繪製按鈕到畫面上
        :param screen: Pygame 的畫布 (surface)
        """

        # 計算冷卻比例
        elapsed_time = pygame.time.get_ticks() - self.last_clicked_time
        cooldown_ratio = max(0, min(1, elapsed_time / self.cooldown))
        if cooldown_ratio == 1:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            # 繪製冷卻進度圓環
            center = self.rect.center
            radius = self.rect.width // 2
            end_angle = -90 + 360 * cooldown_ratio  # Pygame 的角度從 -90 開始
            pygame.draw.arc(screen, self.color, self.rect.inflate(-10, -10), -90 * (3.14159 / 180), end_angle * (3.14159 / 180), self.rect.width)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """
        判斷按鈕是否被按下
        :param event: Pygame 的事件
        :return: 如果被按下回傳顏色，否則回傳 None
        """
        current_time = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左鍵
            if self.rect.collidepoint(event.pos) and (current_time - self.last_clicked_time >= self.cooldown):
                self.last_clicked_time = current_time
                return True
        return False
    
class ColorButtonList:
    def __init__(self, color_buttons: list[ColorButton] = []):
        self._color_buttons = color_buttons

    def add_button(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]):
        self._color_buttons.append(ColorButton(x, y, width, height, color))

    def get_color_clicked(self, event: pygame.event.Event) -> tuple[int, int, int] | None:
        for btn in self._color_buttons:
            if btn.is_clicked(event):
                return btn.color
        return None
    
    def draw(self, screen: pygame.Surface) -> None:
        for btn in self._color_buttons:
            btn.draw(screen)

class ColorButton:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]) -> None:
        """
        初始化 Button 類別
        :param x: 按鈕的 X 座標
        :param y: 按鈕的 Y 座標
        :param width: 按鈕的寬度
        :param height: 按鈕的高度
        :param color: 按鈕的顏色 (RGB 格式)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.cooldown = COLOR_BTN_CD * 1000
        self.last_clicked_time = pygame.time.get_ticks()  # 確保開始時可以立即點擊

    def draw(self, screen: pygame.Surface) -> None:
        """
        繪製按鈕到畫面上
        :param screen: Pygame 的畫布 (surface)
        """

        # 計算冷卻比例
        elapsed_time = pygame.time.get_ticks() - self.last_clicked_time
        cooldown_ratio = max(0, min(1, elapsed_time / self.cooldown))
        if cooldown_ratio == 1:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            # 繪製冷卻進度圓環
            center = self.rect.center
            radius = self.rect.width // 2
            end_angle = -90 + 360 * cooldown_ratio  # Pygame 的角度從 -90 開始
            pygame.draw.arc(screen, self.color, self.rect.inflate(-10, -10), -90 * (3.14159 / 180), end_angle * (3.14159 / 180), self.rect.width)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """
        判斷按鈕是否被按下
        :param event: Pygame 的事件
        :return: 如果被按下回傳顏色，否則回傳 None
        """
        current_time = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左鍵
            if self.rect.collidepoint(event.pos) and (current_time - self.last_clicked_time >= self.cooldown):
                self.last_clicked_time = current_time
                return True
        return False


class Game:
    deltaTime = 0

    def __init__(self):
        self.status = 1 # 0->wait, 1->run, 2->pause in tutorial
        self.status_tutorial = 0 # -1->run but in tutorial, 0->no-tutorial, 1->shoot arrow, 2->shoot again, 3-> make pair
        self.finish_tutorial = False
        self.possible_colors : pygame.Color = [RED, GREEN, YELLOW, BLUE, PURPLE]
        self.view : View = View(self.possible_colors + [WHITE])

        self.jupiter : Jupiter = None
        self.tree : Tree = None
        self.character_line : CharacterLine = None
        self.character_pairs : list[CharacterPair] = []
        self.arrows : list[Arrow] = []
        self.success = False
        self.level = 0
        self.remain_pairs = 1
        self.init_model()

        self.color_btn_list : ColorButtonList = ColorButtonList()
        for i in range(0, len(self.possible_colors)):
            color = self.possible_colors[i]
            self.color_btn_list.add_button(SCREEN_WIDTH//2 - 120 +i*60, SCREEN_HEIGHT - 80, 40, 40, color)

        self._timers : list[Timer]
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
        self.view.draw_background(screen)
        self.color_btn_list.draw(screen)
        
        self.view.draw_jupiter(self.jupiter, screen)
        self.view.draw_tree(self.tree, screen)
        for character in self.character_line.characters:
            self.view.draw_character(character, screen)
        for character_pair in self.character_pairs:
            self.view.draw_character_with_wings(character_pair.character1, screen)
            self.view.draw_character_with_wings(character_pair.character2, screen)

        for arrow in self.arrows:
            self.view.draw_arrow(arrow, screen)
        
        self.view.draw_text(screen, f"Level {self.level+1}", 50, WHITE, False, SCREEN_WIDTH-150, 50)

        if self.status == 0:
            if self.remain_pairs > 0:
                self.view.draw_text(screen, f"Oops your tree got attack!", 50, RED, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2-50)
                self.view.draw_text(screen, "Press R to continue!", 50, YELLOW, False, SCREEN_WIDTH/2-25, SCREEN_HEIGHT/2+50)
            elif self.level+1 < len(LEVEL):
                self.view.draw_text(screen, f"You successfully pass Level {self.level+1}!", 50, WHITE, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50)
                self.view.draw_text(screen, "Press R to continue!", 50, YELLOW, False, SCREEN_WIDTH/2-25, SCREEN_HEIGHT/2+50)
            else:
                self.view.draw_text(screen, f"OMG you successfully pass All Levels!", 50, WHITE, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50)
                self.view.draw_text(screen, "Press R to restart from 0!", 50, YELLOW, False, SCREEN_WIDTH/2-25, SCREEN_HEIGHT/2+50)
        elif self.status == 2:
            if self.status_tutorial == 1:
                self.view.draw_text(screen, f"Those are color buttons.", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2-50)
                self.view.draw_text(screen, f"Press the button to color the first character.", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2+40)
                self.view.draw_pointer(screen, 540, 520, RED, 50, -90)
            elif self.status_tutorial == 2:
                self.view.draw_text(screen, f"A girl and a boy could make a couple.", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2-50)
                self.view.draw_text(screen, f"Press the same button to color the boy", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2+40)
                self.view.draw_pointer(screen, 540, 520, RED, 50, -90)
            elif self.status_tutorial == 3:
                self.view.draw_text(screen, f"If a boy and a girl has same color cloth,", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2-50)
                self.view.draw_text(screen, f"they will flying high. Have fun!", 50, WHITE, False, SCREEN_WIDTH/2+30, SCREEN_HEIGHT/2+40)
                self.view.draw_pointer(screen, 800, 300, RED, 50, 60)


    def event_trigger(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
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
            self.level = 0
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


class Tree:
    def __init__(self, stability: int, position: int):
        self.stability = stability
        self.position = position
        self.alive = True
    
    def shake(self, strength: int = 1) -> bool:
        self.stability -= strength
        if self.stability <= 0:
            self.alive = False
        return self.alive
    
class Jupiter:
    def __init__(self, x: int, y:int):
        self.x = x
        self.y = y
        self.alive = True

class CharacterPair:
    def __init__(self, character1: Character, character2: Character):
        self.character1 = character1
        self.character2 = character2
    
    def moveUp(self):
        self.character1.flyUp()
        self.character2.flyUp()

    def isTooHigh(self):
        return self.character1.y < 0 and self.character2.y < 0

class CharacterLine:
    def __init__(self, headPos: int, characters : list[Character] = []):
        self.headPos : int = headPos
        self._characters : list[Character] = characters
        self._pointer : int = 0
        self._numCharactersWaiting : int = 0
        self._arrangeCharacters()

    @property
    def characters(self) -> list[Character]:
        return self._characters
    
    @property
    def current_character(self) -> Character | None:
        if self._pointer < self.size:
            return self._characters[self._pointer]
        return None

    @property
    def reset_pointer(self) -> None:
        self._pointer = 0
    
    @property
    def size(self) -> int:
        return len(self._characters)
    
    @property
    def numCharactersWaiting(self) -> int:
        return self._numCharactersWaiting
    
    def addCharacter(self, sex : int, sameSex: bool, width:int, height:int, speed:int) -> None:
        self._characters.append(Character(sex, sameSex, SCREEN_WIDTH, CHARACTER_HEIGHT, width, height, speed))
        self._arrangeCharacters()
    
    def moveAllCharacter(self) -> None:
        for character in self._characters:
            character.move()
        self._arrangeCharacters()
    
    def movePointer(self) -> None:
        if self._pointer < len(self._characters):
            self._pointer += 1
        

    def setCharacterColor(self, color:pygame.Color) -> CharacterPair | None:
        cur_character = self.current_character
        if cur_character != None:
            self.current_character.color = color
            for i in range(0, self._pointer):
                if cur_character.color == self.characters[i].color:
                    if cur_character.can_paired_with(self.characters[i]):
                        newCharacterPair = CharacterPair(self.characters[i], cur_character)
                        self._characters.pop(self._pointer)
                        self._characters.pop(i)
                        self._pointer -= 2
                        return newCharacterPair
                    else:
                        cur_character.angry = True
                        self.characters[i].angry = True

        return None


    def _arrangeCharacters(self) -> None:
        self._numCharactersWaiting = 0
        original_sz = self.size
        self._characters = [ch for ch in self._characters if ch.x > -200]
        self._pointer -= original_sz - self.size
        if self._pointer < 0:
            self._pointer = 0
        if self.size > 0:
            if self._characters[0].x <= self.headPos:
                self._characters[0].x = self.headPos
                self._numCharactersWaiting = 1
        if self.size > 1:
            for i in range(1, self.size):
                cur_ch = self._characters[i]
                prev_ch = self._characters[i-1]
                if cur_ch.x <= prev_ch.x + prev_ch.width+10:
                    cur_ch.x = prev_ch.x + prev_ch.width+10
                    if i == self._numCharactersWaiting:
                        self._numCharactersWaiting += 1

        

class Character:
    def __init__(self, sex : int, sameSex: bool, x:int, y:int, width:int, height:int, speed:float):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.sex = sex
        self.sameSex = sameSex
        self.paired = False
        self.angry = False
        self.color:pygame.Color = None

    def move(self) -> None:
        if self.angry:
            self.x -= self.speed * 10
        else:
            self.x -= self.speed

    def flyUp(self) -> None:
        self.y -= 10
    
    def can_paired_with(self, other : Character) -> bool:
        if self.color == other.color:
            if self.sameSex == True and self.sex == other.sex:
                return True
            elif self.sameSex == False and self.sex != other.sex:
                return True
        return False


class Arrow():
    def __init__(self, x, y, target : Character, color, speed : int = 40):
        self.x = x
        self.y = y
        self.target = target
        self.color = color
        self.speed = speed
        self.rotation = 0
        self._arrive_target = False

    def has_arrive_target(self):
        return self._arrive_target

    def update(self):
        vec = pygame.Vector2(self.target.x - self.x, self.target.y - self.y)
        self.rotation = vec.as_polar()[1]
        magnitude = vec.magnitude()
        if magnitude < self.speed:
            vec = vec.normalize() * magnitude
            self._arrive_target = True
        else:
            vec = vec.normalize() * self.speed
        self.x += vec.x
        self.y += vec.y



class Timer:
    def __init__(self, seconds, callback, loop=False):
        """
        Initialize the Timer.

        :param seconds: Time in seconds after which the callback is triggered.
        :param callback: Function to execute when the timer ends.
        :param loop: Whether the timer should restart after finishing.
        """
        self.seconds = seconds
        self.callback = callback
        self.loop = loop
        self.elapsed_time = 0
        self.running = True

    def update(self, delta):
        """
        Update the timer. Should be called every frame in the game loop.
        Executes the callback if the timer completes.
        """
        if self.running:
            self.elapsed_time += delta
            if self.elapsed_time >= self.seconds:
                self.callback()
                if self.loop:
                    self.elapsed_time = 0
                else:
                    self.running = False