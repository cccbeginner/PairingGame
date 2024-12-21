import pygame
import random
from setting import *
from model import *
from typing import Dict

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
        self.snowflakes = [
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