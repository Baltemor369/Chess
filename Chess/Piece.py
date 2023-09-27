import pygame
from Coord import Coord

class Piece:
    def __init__(self, path:str, color:str, type:str, position:Coord, relative_possible_move:list[tuple[int,int]]) -> None:
        self.name:str = type
        self.color:str = color if color == "white" else "black"
        
        # list of relative possible move
        self.possible_move:list[tuple[int,int]] = relative_possible_move
        
        # create a Rect with the image
        self.image:pygame.Surface = pygame.image.load(path)
        self.rect:pygame.Rect = self.image.get_rect()
        
        # set the position of the image
        self.rect.x, self.rect.y = position.x, position.y
        
        # save all position moved
        self.position_log:list[Coord] = [position]

    def get_opposite_color(self):
         return "black" if self.color == "white" else "white"

    def set_position(self,x:int, y:int):
        self.coord = (x,y)
    
    def get_pos(self):
        return (self.rect.x, self.rect.y)
    def get_x(self):
        return self.rect.x
    def get_y(self):
        return self.rect.y
    
    def get_squares_between(self, __o) -> list[tuple[int,int]]:
        squares_between = []
    
        x1, y1 = self.get_pos()
        x2, y2 = __o.get_pos()
        
        # Calculez les différences entre les coordonnées x et y
        dx = x2 - x1
        dy = y2 - y1
        
        # Vérifiez si les cases sont sur la même ligne ou diagonale
        if dx == 0 and dy == 0:
            return []  # Les cases sont identiques, pas de cases intermédiaires
        
        # Calculez les pas pour se déplacer le long de la ligne ou de la diagonale
        step_x = 1 if dx > 0 else -1 if dx < 0 else 0
        step_y = 1 if dy > 0 else -1 if dy < 0 else 0
        
        # Initialisez les coordonnées de la première case intermédiaire
        current_x = x1 + step_x
        current_y = y1 + step_y
        
        # Parcourez les cases intermédiaires jusqu'à atteindre la case finale (non incluse)
        while (current_x, current_y) != __o.get_pos():
            squares_between.append((current_x, current_y))
            current_x += step_x
            current_y += step_y
        
        return squares_between

    
    def __repr__(self) -> str:
        return f"{self.name}"