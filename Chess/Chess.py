import pygame
from const import *
from Piece import Piece
from Coord import Coord

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
        self.position_move_possible:list[Coord] = []
        self.special_case:dict = {}
        self.turn = "white"

        self.start_x = (SCREEN_W - (CASE_SIZE * 8)) // 2
        self.start_y = (SCREEN_H - (CASE_SIZE * 8)) // 2
        
        self.init_pieces()
        

    def init_pieces(self):

        move_list = {
            "pawn" : [(0,1)],
            "rook" : [(0, 1), (0, -1), (1, 0), (-1, 0)],
            "knight" : [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)],
            "bishop" : [(1, 1), (1, -1), (-1, -1), (-1, 1)],
            "queen" : [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)],
            "king" : [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        }

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
                    piece = Piece(f"assets/{color}/pawn.png",color,"pawn",Coord(coord_x,coord_y),move_list["pawn"])
                    self.piece_list.append(piece)
                    row.append(piece)
                elif x == 0:
                    # rook
                    if y == 0 or y == 7:
                        piece = Piece(f"assets/{color}/rook.png",color, "rook", Coord(coord_x,coord_y), move_list["rook"])
                        self.piece_list.append(piece)
                        row.append(piece)
                    # knight
                    elif y == 1 or y == 6:
                        piece = Piece(f"assets/{color}/knight.png",color, "knight", Coord(coord_x,coord_y), move_list["knight"])
                        self.piece_list.append(piece)
                        row.append(piece)
                    # bishop
                    elif y == 2 or y == 5:
                        piece = Piece(f"assets/{color}/bishop.png",color, "bishop", Coord(coord_x,coord_y), move_list["bishop"])
                        self.piece_list.append(piece)
                        row.append(piece)
                    elif y == 3:
                        piece = Piece(f"assets/{color}/{piece3}.png",color, piece3, Coord(coord_x,coord_y), move_list["king"])
                        self.piece_list.append(piece)
                        row.append(piece)
                    elif y == 4:
                        piece =Piece(f"assets/{color}/{piece4}.png",color, piece4, Coord(coord_x,coord_y), move_list["queen"])
                        self.piece_list.append(piece)
                        row.append(piece)
                
                # bot side
                elif x == 6:
                    color = "black" if color == "white" else "white"
                    # pawn row
                    piece = Piece(f"assets/{color}/pawn.png",color,"pawn",Coord(coord_x,coord_y),move_list["pawn"])
                    self.piece_list.append(piece)
                    row.append(piece)
                elif x == 7:
                    color = "black" if color == "white" else "white"
                    # rook
                    if y == 0 or y == 7:
                        piece = Piece(f"assets/{color}/rook.png", color, "rook", Coord(coord_x,coord_y), move_list["rook"])
                        self.piece_list.append(piece)
                        row.append(piece)
                    # knight
                    elif y == 1 or y == 6:
                        piece = Piece(f"assets/{color}/knight.png", color, "knight", Coord(coord_x,coord_y), move_list["knight"])
                        self.piece_list.append(piece)
                        row.append(piece)
                    # bishop
                    elif y == 2 or y == 5:
                        piece = Piece(f"assets/{color}/bishop.png", color, "bishop", Coord(coord_x,coord_y), move_list["bishop"])
                        self.piece_list.append(piece)
                        row.append(piece)
                    elif y == 3:
                        piece = Piece(f"assets/{color}/{piece3}.png", color, piece3, Coord(coord_x,coord_y), move_list["king"])
                        self.piece_list.append(piece)
                        row.append(piece)
                    elif y == 4:
                        piece = Piece(f"assets/{color}/{piece4}.png", color, piece4, Coord(coord_x,coord_y), move_list["queen"])
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
                    try:
                        new_piece_selection = self.get_piece_at((x,y))
                        self.selected_piece = new_piece_selection
                    except:
                        self.selected_piece = None
                    
    def update_data(self):
        if not self.is_in_check(self.turn):
            if self.selected_piece:
                # verifier si le roi est en échec
                # check if selected_piece is pinned
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
                if self.selected_piece and (self.start_x + row * CASE_SIZE + (CASE_SIZE - IMG_SIZE)/2, self.start_y + case * CASE_SIZE + (CASE_SIZE - IMG_SIZE)/2) == self.selected_piece.get_pos():
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
        return self.board[pos[1]][pos[0]]

    def is_same_line(self, target_piece:Piece, second_piece:Piece):
        return (target_piece.get_x() == second_piece.get_x()) or (target_piece.get_y() == second_piece.get_y())

    def is_same_diagonal(self, target_piece:Piece, second_piece:Piece):
        x1, y1 = target_piece.get_pos()
        x2, y2 = second_piece.get_pos()

        return abs(x1-x2) == abs(y1 - y2)
    
    def is_align(self, target_piece:Piece, second_piece:Piece):
        return self.is_same_line(target_piece, second_piece) or self.is_same_diagonal(target_piece, second_piece)
    
    def is_pinned(self):
        pass                        
    
    def is_in_check(self,color:str):
        king = self.get_king(color)
        for elt in self.piece_list:
            if elt.color != king.color:
                if (elt.name == "bishop" or elt.name == "queen") and self.is_same_diagonal(elt, king):
                    squares = king.get_squares_between(elt)
                    for square in squares:
                        if self.get_piece_at(square) is not None:
                            return False
                elif (elt.name == "rook" or elt.name == "queen") and self.is_same_line(elt, king):
                    squares = king.get_squares_between(elt)
                    for square in squares:
                        if self.get_piece_at(square) is not None:
                            return False
                # elif (elt.name == "knight")
        
        return True