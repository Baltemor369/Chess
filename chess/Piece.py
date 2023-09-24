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
        self.rect.topleft = (position.x, position.y)
        
        # save all position moved
        self.position_log:list[Coord] = [position]
    
    def set_position(self,x:int, y:int):
        self.coord = (x,y)
    
    def get_x(self):
        return self.coord[0]
    def get_y(self):
        return self.coord[1]
    
    def __repr__(self) -> str:
        return f"{self.name}"