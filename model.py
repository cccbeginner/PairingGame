from __future__ import annotations
import pygame
import random
from setting import *
    
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
        self.headPos = headPos
        self._characters = characters
        self._pointer = 0
        self._numCharactersWaiting = 0
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

