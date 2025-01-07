from __future__ import annotations
import pygame
from setting import *

class ColorButtonList:
    def __init__(self):
        self._color_buttons = []

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
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int], 
                 text: str = "", text_color: tuple[int, int, int] = (0, 0, 0), cooldown = 2) -> None:
        """
        初始化 Button 類別
        :param x: 按鈕的 X 座標
        :param y: 按鈕的 Y 座標
        :param width: 按鈕的寬度
        :param height: 按鈕的高度
        :param color: 按鈕的顏色 (RGB 格式)
        :param text: 按鈕上的文字
        :param text_color: 按鈕文字的顏色 (RGB 格式)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont("Arial", 24)
        self.text_color = text_color
        self.cooldown = cooldown * 1000
        if self.cooldown == 0:
            self.cooldown = 1
        self.last_clicked_time = pygame.time.get_ticks()  # 確保開始時可以立即點擊

    def draw(self, screen: pygame.Surface) -> None:
        """
        繪製按鈕到畫面上
        :param screen: Pygame 的畫布 (surface)
        """
        # 計算冷卻比例
        elapsed_time = pygame.time.get_ticks() - self.last_clicked_time
        cooldown_ratio = max(0, min(1, elapsed_time / self.cooldown))

        # 繪製按鈕
        if cooldown_ratio == 1:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            # 繪製冷卻進度圓環
            center = self.rect.center
            radius = self.rect.width // 2
            end_angle = -90 + 360 * cooldown_ratio  # Pygame 的角度從 -90 開始
            pygame.draw.arc(screen, self.color, self.rect.inflate(-10, -10), -90 * (3.14159 / 180), end_angle * (3.14159 / 180), self.rect.width)

        # 繪製文字
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """
        判斷按鈕是否被按下
        :param event: Pygame 的事件
        :return: 如果被按下回傳 True，否則回傳 False
        """
        current_time = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左鍵
            if self.rect.collidepoint(event.pos) and (current_time - self.last_clicked_time >= self.cooldown):
                self.last_clicked_time = current_time
                return True
        return False
