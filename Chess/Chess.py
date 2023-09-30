import pygame
from const import *
from Piece import *
from Move import Move

class Chess:
    def __init__(self,botside:str="white") -> None:
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Chess")

        self.clock = pygame.time.Clock()

        self.running:bool = True
        self.board:list[list[Piece|None]] = []
        self.piece_list:list[Piece] = []
        self.botside:str = botside if botside=="white" else "black"
        self.selected_piece:Piece|None = None
        self.possible_move:list[Move] = []
        self.special_case:dict = {}
        self.turn = "white"

        self.start_x = (SCREEN_W - (CASE_SIZE * 8)) // 2
        self.start_y = (SCREEN_H - (CASE_SIZE * 8)) // 2
        
        self.init_pieces()
        

    def init_pieces(self):

        for x in range(8):
            row = []
            for y in range(8):
                coord_x = y # self.start_x + y * CASE_SIZE + (CASE_SIZE - IMG_SIZE)/2
                coord_y = x # self.start_y + x * CASE_SIZE + (CASE_SIZE - IMG_SIZE)/2

                color = "white" if self.botside == "black" else "black"
                piece3 = "queen" if self.botside == "white" else "king"
                piece4 = "king" if self.botside == "white" else "queen"

                # top side
                if x == 1:
                    piece = Pawn(f"assets/{color}/pawn.png",color,"pawn",(coord_x,coord_y),-1)
                    self.piece_list.append(piece)
                    row.append(piece)
                elif x == 0:
                    # rook
                    if y == 0 or y == 7:
                        piece = Rook(f"assets/{color}/rook.png",color, "rook", (coord_x,coord_y))
                        self.piece_list.append(piece)
                        row.append(piece)
                    # knight
                    elif y == 1 or y == 6:
                        piece = Knight(f"assets/{color}/knight.png",color, "knight", (coord_x,coord_y))
                        self.piece_list.append(piece)
                        row.append(piece)
                    # bishop
                    elif y == 2 or y == 5:
                        piece = Bishop(f"assets/{color}/bishop.png",color, "bishop", (coord_x,coord_y))
                        self.piece_list.append(piece)
                        row.append(piece)
                    elif y == 3:
                        if piece3 == "king":
                            piece = King(f"assets/{color}/king.png",color, piece3, (coord_x,coord_y))
                        else:
                            piece = Queen(f"assets/{color}/queen.png",color, piece3, (coord_x,coord_y))
                        self.piece_list.append(piece)
                        row.append(piece)
                    elif y == 4:
                        if piece4 == "king":
                            piece = King(f"assets/{color}/king.png",color, piece4, (coord_x,coord_y))
                        else:
                            piece = Queen(f"assets/{color}/queen.png",color, piece4, (coord_x,coord_y))
                        self.piece_list.append(piece)
                        row.append(piece)
                
                # bot side
                elif x == 6:
                    color = "black" if color == "white" else "white"
                    piece = Pawn(f"assets/{color}/pawn.png",color,"pawn",(coord_x,coord_y),1)
                    self.piece_list.append(piece)
                    row.append(piece)
                elif x == 7:
                    color = "black" if color == "white" else "white"
                    # rook
                    if y == 0 or y == 7:
                        piece = Rook(f"assets/{color}/rook.png", color, "rook", (coord_x,coord_y))
                        self.piece_list.append(piece)
                        row.append(piece)
                    # knight
                    elif y == 1 or y == 6:
                        piece = Knight(f"assets/{color}/knight.png", color, "knight", (coord_x,coord_y))
                        self.piece_list.append(piece)
                        row.append(piece)
                    # bishop
                    elif y == 2 or y == 5:
                        piece = Bishop(f"assets/{color}/bishop.png", color, "bishop", (coord_x,coord_y))
                        self.piece_list.append(piece)
                        row.append(piece)
                    elif y == 3:
                        if piece3 == "king":
                            piece = King(f"assets/{color}/king.png",color, piece3, (coord_x,coord_y))
                        else:
                            piece = Queen(f"assets/{color}/queen.png",color, piece3, (coord_x,coord_y))
                        self.piece_list.append(piece)
                        row.append(piece)
                    elif y == 4:
                        if piece4 == "king":
                            piece = King(f"assets/{color}/king.png",color, piece4, (coord_x,coord_y))
                        else:
                            piece = Queen(f"assets/{color}/queen.png",color, piece4, (coord_x,coord_y))
                        self.piece_list.append(piece)
                        row.append(piece)
                else:
                    row.append(None)
                        
            self.board.append(row)
    
    def handle_event(self):
        for evt in pygame.event.get():
            
            if evt.type == pygame.QUIT:
                self.running = False
            
            elif evt.type == pygame.MOUSEBUTTONDOWN:
                
                if evt.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    x = (mouse_x - self.start_x)//CASE_SIZE
                    y = (mouse_y -self.start_y)//CASE_SIZE
                    
                    selection = self.get_piece_at((x,y))
                    has_move = False

                    #verify if Click on a possible move
                    if self.selected_piece:
                        
                        for move in self.possible_move:
                            if move.end == (x, y):
                                self.move(move)
                                has_move = True
                                # clear selection
                                self.selected_piece = None
                                self.possible_move = None
                                self.turn = "black" if self.turn == "white" else "white"
                                break
                    
                    if not has_move:    
                        # verify if click on another of my pieces
                        if selection :
                            if selection.color == self.turn:
                                self.selected_piece = selection
                                self.possible_move = self.selected_piece.get_possible_moves(self)
                        
                            else:
                                self.selected_piece = None
                                self.possible_move = None
                        else:
                            self.selected_piece = None
                            self.possible_move = None
                    
    def update_data(self):
        possible_moves = []
        
        if self.selected_piece:
            # get the possible move of selected piece 
            possible_moves = self.selected_piece.get_possible_moves(self)
        

            # verify is our king is in check
            # tmp = self.is_in_check(self.turn)
            
            # if tmp != False:
                # get all position between our king and the attacking piece
                # cases_possible = set(self.get_squares_between(self.get_king(self.turn),tmp))
                # add the position of the attacking piece
                # cases_possible.add(tmp.get_position())
                
                # possible_moves = [move for move in possible_moves if move.end in cases_possible]
                    
            # verify if the selected piece is not pinned
            # tmp = self.is_pinned(self.selected_piece)
            
            # if tmp != False:
                # get all position between the pinning piece and our king
                # cases_possible = set(self.get_squares_between(tmp, self.get_king(self.turn)))

                # possible_moves = [move for move in possible_moves if move.end in cases_possible]

            new = []
            # verify if moves are in the board
            for move in possible_moves:
                if  0 <= move.end[0] < 8 and 0 <= move.end[1] < 8:
                    new.append(move)
            possible_moves = new
            
        self.possible_move = possible_moves.copy()

    def run(self):
        while self.running:
            self.handle_event()

            self.update_data()
            
            self.draw_board()
            
            pygame.display.flip()

            self.clock.tick(25)
        
        pygame.quit()

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        moves = [move.end for move in self.possible_move]
        for row in range(8):
            for col in range(8):
                bg_color = WHITE if (row + col) % 2 == 0 else GRAYLIGHT
                case_rect = pygame.Rect(
                    self.start_x + CASE_SIZE * row,
                    self.start_y + CASE_SIZE * col,
                    CASE_SIZE,
                    CASE_SIZE,
                )

                # highlight the selected piece
                if self.selected_piece and (row,col) == self.selected_piece.get_position():
                    pygame.draw.rect(self.screen, GREENLIGHT, case_rect)
                # classic draw
                else:
                    pygame.draw.rect(self.screen, bg_color, case_rect)

                # highlight possible moves
                if (row,col) in moves:
                    pygame.draw.rect(self.screen, BLUELIGHT, case_rect)
                
                # highlight the king who is in check
                if self.is_in_check(self.turn):
                    king = self.get_king(self.turn)
                    x = self.start_x + CASE_SIZE * king.get_x() + (CASE_SIZE - IMG_SIZE)/2
                    y = self.start_y + CASE_SIZE * king.get_y() + (CASE_SIZE - IMG_SIZE)/2
                    pygame.draw.rect(self.screen, REDLIGHT, case_rect)
                
                # put the piece image on the Surface
                elt = self.get_piece_at((row,col))
                if isinstance(elt,Piece):
                    x = self.start_x + CASE_SIZE * elt.get_x() + (CASE_SIZE - IMG_SIZE)/2
                    y = self.start_y + CASE_SIZE * elt.get_y() + (CASE_SIZE - IMG_SIZE)/2
                    self.screen.blit(elt.image, (x,y))
    
    def get_king(self, color:str) -> Piece|None:
        for elt in self.piece_list:
            if elt.name == "king" and elt.color == color:
                return elt
        return None
    
    def get_pieces(self, color:str) -> list[Piece]:
        pieces = []
        for elt in self.piece_list:
            if elt.color == color:
                pieces.append(elt)
            
        return pieces
    
    def get_piece_at(self,pos:tuple[int,int]):
        if 0 <= pos[0] < 8 and 0 <= pos[1] < 8:
            return self.board[pos[1]][pos[0]]
        return None

    def is_same_line(self, target_piece:Piece, second_piece:Piece):
        return (target_piece.get_x() == second_piece.get_x()) or (target_piece.get_y() == second_piece.get_y())

    def is_same_diagonal(self, target_piece:Piece, second_piece:Piece):
        x1, y1 = target_piece.get_position()
        x2, y2 = second_piece.get_position()

        return abs(x1-x2) == abs(y1 - y2)
    
    def is_align(self, target_piece:Piece, second_piece:Piece):
        return self.is_same_line(target_piece, second_piece) or self.is_same_diagonal(target_piece, second_piece)
    
    def get_squares_between(self, piece1:Piece, piece2:Piece) -> list[tuple[int,int]]:
        squares_between = []
    
        x1, y1 = piece1.get_position()
        x2, y2 = piece2.get_position()
        
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
        while (current_x, current_y) != piece2.get_position():
            squares_between.append((current_x, current_y))
            current_x += step_x
            current_y += step_y
        
        return squares_between

    def get_pieces_between(self, piece1: Piece, piece2: Piece):
        return [self.get_piece_at(pos) for pos in self.get_squares_between(piece1, piece2) if isinstance(self.get_piece_at(pos),Piece)]

    
    def set(self, pos:tuple[int,int], val:Piece|None):
        if 0 <= pos[0] < 8 and 0 <= pos[1] <8:
            self.board[pos[1]][pos[0]] = val
        
    def move(self, move:Move):
        # actualize the position in the piece class
        move.target_piece.move(move.end)
        self.set(move.start,None)

        if move.eat_piece:
            move.eat_piece.set_position((-1,-1))
            self.set(move.eat_piece.get_position(), None)
        
        elif move.second_target:
            move.second_target.move(move.second_end)
            self.set(move.second_end, move.second_target)
        
        self.set(move.end, move.target_piece)


    def is_in_check(self, color:str) -> Piece|bool:
        king = self.get_king(color)
        king_position = king.get_position()

        for p in self.get_pieces(king.get_opposite_color()):
            if king_position in p.get_possible_moves(self):
                return p

        return False
    
    def is_pinned(self, piece:Piece) -> Piece|bool:
        king = self.get_king(piece.color)
        buffer = 0
        piece_pinning = None
        is_surrounded = False
        for p in self.get_pieces(piece.get_opposite_color()):
            
            if p.name not in ["pawn","king"]:
                position_between = self.get_squares_between(p, king)
            
                for pos in position_between:
            
                    if isinstance(self.get_piece_at(pos),Piece):
                        buffer += 1
                    
                    if self.get_piece_at(pos) == piece:
                        is_surrounded = True
                        piece_pinning = p

        if buffer == 1 and is_surrounded:
            return piece_pinning
        
        return False