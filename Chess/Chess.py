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
                coord_x = self.start_x + y * CASE_SIZE + (CASE_SIZE - IMG_SIZE)/2
                coord_y = self.start_y + x * CASE_SIZE + (CASE_SIZE - IMG_SIZE)/2

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
                        piece = Piece(f"assets/{color}/knight.png", color, "knight", (coord_x,coord_y))
                        self.piece_list.append(piece)
                        row.append(piece)
                    # bishop
                    elif y == 2 or y == 5:
                        piece = Piece(f"assets/{color}/bishop.png", color, "bishop", (coord_x,coord_y))
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
                    # click on nothing
                    if selection is None:
                        self.selected_piece = None
                        continue
                    # click on own piece
                    if selection.color == self.turn:
                        # click on a possible move
                        for move in self.possible_move:
                            if move.end == (x,y):
                                self.move(move)
                                break
                        # click on a new piece
                        if selection != self.selected_piece:
                            self.selected_piece = selection
                    # click on nothing or an ennemy piece
                    else:
                        self.selected_piece = None
                    # print(self.selected_piece.name)
                        
                    
    def update_data(self):
        
        # verifier si le roi est en échec
            # si oui trier les mouvements possible
        # verifier si selected_piece is pinned
            # si oui trier les mouvements possible
        # recuperer les deplacements absolus de selected_piece
        # verifier qu'ils soient dans le plateau
        # verifier qu'ils ne soient pas occupés par un pion de meme couleur
        # verifier les déplacements relatifs (prise en passant - pion diagonale - castling - pion doublestep)
        # set position_move_possible en fonction des points précédents
        pass

    def run(self):
        while self.running:
            self.handle_event()

            self.update_data()
            
            self.draw_board()
            
            pygame.display.flip()

            self.clock.tick(30)
        
        pygame.quit()

    def draw_board(self):
        self.screen.fill((255,255,255))
        
        for row in range(8):
            for case in range(8):
                bg_color = WHITE if (row+case)%2==0 else GRAYLIGHT
                if self.selected_piece and (self.start_x + row * CASE_SIZE + (CASE_SIZE - IMG_SIZE)/2, self.start_y + case * CASE_SIZE + (CASE_SIZE - IMG_SIZE)/2) == self.selected_piece.get_position():
                        pygame.draw.rect(self.screen, GREENLIGHT, (self.start_x + CASE_SIZE * row, self.start_y + CASE_SIZE * case, CASE_SIZE, CASE_SIZE))
                else:
                    pygame.draw.rect(self.screen, bg_color, (self.start_x + CASE_SIZE * row, self.start_y + CASE_SIZE * case, CASE_SIZE, CASE_SIZE))
                
                elt = self.board[case][row]
                if elt != None:
                    self.screen.blit(elt.image, (elt.get_x(), elt.get_y()))
    
    def get_king(self, color:str) -> Piece|None:
        for elt in self.piece_list:
            if elt.name == "king" and elt.color == color:
                return elt
        return None
    
    def get_black_piece(self):
        pieces = []
        for elt in self.piece_list:
            if elt.color == "black":
                pieces.append(elt)
            
        return pieces
    
    def get_white_piece(self):
        pieces = []
        for elt in self.piece_list:
            if elt.color == "white":
                pieces.append(elt)
            
        return pieces
    
    def get_piece_at(self,pos:tuple[int,int]):
        if 0 <= pos[0] < 8 and 0 <= pos[1] < 8:
            return self.board[pos[1]][pos[0]]
        return None

    def is_same_line(self, target_piece:Piece, second_piece:Piece):
        return (target_piece.get_x() == second_piece.get_x()) or (target_piece.get_y() == second_piece.get_y())

    def is_same_diagonal(self, target_piece:Piece, second_piece:Piece):
        x1, y1 = target_piece.get_pos()
        x2, y2 = second_piece.get_pos()

        return abs(x1-x2) == abs(y1 - y2)
    
    def is_align(self, target_piece:Piece, second_piece:Piece):
        return self.is_same_line(target_piece, second_piece) or self.is_same_diagonal(target_piece, second_piece)
    
    def get_squares_between(self, piece1:Piece, piece2:Piece) -> list[tuple[int,int]]:
        squares_between = []
    
        x1, y1 = piece1.get_pos()
        x2, y2 = piece2.get_pos()
        
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
        while (current_x, current_y) != piece2.get_pos():
            squares_between.append((current_x, current_y))
            current_x += step_x
            current_y += step_y
        
        return squares_between
    
    def set(self, pos:tuple[int,int], val:Piece|None):
        if 0 <= pos[0] < 8 and 0 <= pos[1] <8:
            self.board[pos[1]][pos[0]] = val
        
    def move(self, move:Move):
        self.set(move.start, None)

        # eating
        if move.eat_piece:
            self.set(move.eat_piece.get_position(), None)
        
        # castling
        if move.second_target:
            self.set(move.second_end, move.second_target)

        # main move
        self.set(move.end, move.target_piece)
