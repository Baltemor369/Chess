import pygame
from Move import Move

class Piece:
    def __init__(self, path:str, color:str, type:str, position:tuple[int, int]) -> None:
        self.name:str = type
        self.color:str = color
        self.step = 0
        
        # create a Rect with the image
        self.image:pygame.Surface = pygame.image.load(path)
        self.rect:pygame.Rect = self.image.get_rect()
        
        # set the position of the image
        self.rect.x, self.rect.y = position[0], position[1]
    
    def __repr__(self) -> str:
        return f"{self.name} {self.color} {self.get_position()}"
        
    def move(self,new_position:tuple[int,int]):
        self.rect.x, self.rect.y = new_position
        self.step += 1
    
    def get_position(self):
        return (self.rect.x, self.rect.y)
    def get_x(self):
        return self.rect.x
    def get_y(self):
        return self.rect.y
    def get_opposite_color(self):
         return "black" if self.color == "white" else "white"

    def get_possible_moves(self, board)->list[Move]:
        raise NotImplementedError("Subclasses should implement this method")

class Pawn(Piece):
    def __init__(self, path: str, color: str, type: str, position: tuple[int, int], direction:int) -> None:
        super().__init__(path, color, type, position)
        self.move_direction = direction
        self.spawn_position = position
    
    def get_possible_moves(self, board):
        possible_moves = []
        coef = self.move_direction * -1 # 1 if pawn has to go down, -1 if pawn has to go up
        # front move
        if not board.get_piece_at((self.get_x(), self.get_y()+1*coef)):
            m = Move(self.get_position(),(self.get_x(), self.get_y()+1*coef), self)
            possible_moves.append(m)
            if self.step == 0 and board.get_piece_at((self.get_x(), self.get_y()+2*coef)) is None:
                m = Move(self.get_position(),(self.get_x(), self.get_y()+2*coef), self)
                possible_moves.append(m)

        # left diagonal move
        p = board.get_piece_at((self.get_x()-1*coef, self.get_y()+1*coef))
        if p and p.color != self.color:
            m = Move(self.get_position(),(self.get_x()-1*coef, self.get_y()+1*coef), self, p)
            possible_moves.append(m)

        # right diagonal move
        p = board.get_piece_at((self.get_x()+1*coef, self.get_y()+1*coef))
        if p and p.color != self.color:
            m = Move(self.get_position(),(self.get_x()+1*coef, self.get_y()+1*coef), self, p)
            possible_moves.append(m)

        # "en passant" left
        p = board.get_piece_at((self.get_x()-1*coef, self.get_y()))
        if p and p.name == "pawn" and p.color != self.color:
            if p.get_x() - p.spawn_position[0] == 2 and p.step==1*coef:
                m = Move(self.get_position(),(self.get_x()-1*coef, self.get_y()+1*coef), self, p)
                possible_moves.append(m)
        
        # "en passant" right
        p = board.get_piece_at((self.get_x()+1*coef, self.get_y()))
        if p and p.name == "pawn" and p.color != self.color:
            if p.get_x() - p.spawn_position[0] == 2 and p.step==1*coef:
                m = Move(self.get_position(),(self.get_x()+1*coef, self.get_y()+1*coef), self, p)
                possible_moves.append(m)
        
        return possible_moves


class Rook(Piece):
    def __init__(self, path: str, color: str, type: str, position: tuple[int, int]) -> None:
        super().__init__(path, color, type, position)

    def get_possible_moves(self, board):
        possible_moves = []

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            
            for i in range(1, 8): 
                x, y = self.get_x() + dx * i, self.get_y() + dy * i
                p = board.get_piece_at((x, y))
                
                #  find a piece
                if p:
                    # ennemy piece
                    if p.color != self.color:
                        m = Move(self.get_position(), p.get_position(), self, p)
                        possible_moves.append(m)
                    # find a ally piece just stop the loop
                    # finally
                    break
                
                # empty case
                else:
                    m = Move(self.get_position(), (x, y), self)
                    possible_moves.append(m)
        
        return possible_moves

class Bishop(Piece):
    def __init__(self, path: str, color: str, type: str, position: tuple[int, int]) -> None:
        super().__init__(path, color, type, position)

    def get_possible_moves(self, board):
        possible_moves = []

        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dx, dy in directions:
            
            for i in range(1, 8): 
                x, y = self.get_x() + dx * i, self.get_y() + dy * i
                p = board.get_piece_at((x, y))
                
                #  find a piece
                if p:
                    # ennemy piece
                    if p.color != self.color:
                        m = Move(self.get_position(), p.get_position(), self, p)
                        possible_moves.append(m)
                    # find a ally piece just stop the loop
                    # finally
                    break
                
                # empty case
                else:
                    m = Move(self.get_position(), (x, y), self)
                    possible_moves.append(m)
        return possible_moves

class Knight(Piece):
    def __init__(self, path: str, color: str, type: str, position: tuple[int, int]) -> None:
        super().__init__(path, color, type, position)

    def get_possible_moves(self, board):
        possible_moves = []

        cases = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        for x, y in cases:
            p = board.get_piece_at((self.get_x()+x, self.get_y()+y))
            
            # find a piece
            if p:
                # ennemy piece
                if p.color != self.color:
                    m = Move(self.get_position(), p.get_position(), self, p)
                    possible_moves.append(m)
                
                continue
            # empty case
            else:
                m = Move(self.get_position(), (self.get_x() + x, self.get_y() + y), self)
                possible_moves.append(m)
            
        return possible_moves

class Queen(Piece):
    def __init__(self, path: str, color: str, type: str, position: tuple[int, int]) -> None:
        super().__init__(path, color, type, position)

    def get_possible_moves(self, board):
        possible_moves = []

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),(1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dx, dy in directions:
            
            for i in range(1, 8): 
                x, y = self.get_x() + dx * i, self.get_y() + dy * i
                p = board.get_piece_at((x, y))
                
                #  find a piece
                if p:
                    # ennemy piece
                    if p.color != self.color:
                        m = Move(self.get_position(), p.get_position(), self, p)
                        possible_moves.append(m)
                    # find a ally piece just stop the loop
                    # finally
                    break
                
                # empty case
                else:
                    m = Move(self.get_position(), (x, y), self)
                    possible_moves.append(m)

        return possible_moves

class King(Piece):
    def __init__(self, path: str, color: str, type: str, position: tuple[int, int]) -> None:
        super().__init__(path, color, type, position)

    def get_possible_moves(self, board):
        possible_moves = []

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),(1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dx, dy in directions: 
            x, y = self.get_x() + dx , self.get_y() + dy
            p = board.get_piece_at((x, y))
            
            #  find a piece
            if p:
                # ennemy piece
                if p.color != self.color:
                    m = Move(self.get_position(), p.get_position(), self, p)
                    possible_moves.append(m)
                # find a ally piece just stop the loop
                # finally
                break
            
            # empty case
            else:
                m = Move(self.get_position(), (x, y), self)
                possible_moves.append(m)
        
        # castling check
        pieces = board.get_pieces(self.color)
        for piece in pieces:
            
            if piece.name == "rook" and piece.step == 0:
            
                if len(board.get_pieces_between(self, piece)) == 0:
                    sens = 1 if self.get_y()-piece.get_y() < 0 else -1
                    m = Move(self.get_position(), (self.get_x(), self.get_y() + 2 * sens), self, second_target=piece, second_end=(piece.get_x(),self.get_y() - 1 * sens))
                    possible_moves.append(m)

        return possible_moves