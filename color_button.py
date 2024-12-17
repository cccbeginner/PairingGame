from __future__ import annotations
import pygame

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

    def draw(self, screen: pygame.Surface) -> None:
        """
        繪製按鈕到畫面上
        :param screen: Pygame 的畫布 (surface)
        """
        pygame.draw.rect(screen, self.color, self.rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """
        判斷按鈕是否被按下
        :param event: Pygame 的事件
        :return: 如果被按下回傳顏色，否則回傳 None
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左鍵
            if self.rect.collidepoint(event.pos):
                return True
        return False