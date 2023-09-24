import pygame
from const import *
from Piece import Piece
from Coord import Coord

class Chess:
    def __init__(self,botside:str="white") -> None:
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Chess")

        self.running:bool = True
        self.board:list[list[Piece|None]] = []
        self.white_pieces:list[Piece] = []
        self.black_pieces:list[Piece] = []
        self.botside:str = botside if botside=="white" else "black"
        self.selected_piece:Piece|None = None
        
        self.init_pieces()
        

    def init_pieces(self):
        for x in range(8):
            row = []
            for y in range(8):
                if self.botside == "black":
                    # top side
                    if x == 1:
                        piece = Piece("assets/white/pawn.png","white","pawn",Coord(x,y),[(0,1)])
                        self.white_pieces.append(piece)
                        row.append(piece)
                    elif x == 0:
                        if y == 0 or y == 7:
                            piece = Piece("assets/white/rook.png", "white", "rook", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0)])
                            self.white_pieces.append(piece)
                            row.append(piece)
                        if y == 1 or y == 6:
                            piece = Piece("assets/white/knight.png", "white", "knight", Coord(x, y), [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)])
                            self.white_pieces.append(piece)
                            row.append(piece)
                        if y == 2 or y == 5:
                            piece = Piece("assets/white/bishop.png", "white", "bishop", Coord(x, y), [(1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.white_pieces.append(piece)
                            row.append(piece)
                        if y == 4:
                            piece =Piece("assets/white/queen.png", "white", "queen", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.white_pieces.append(piece)
                            row.append(piece)
                        if y == 3:
                            piece = Piece("assets/white/king.png", "white", "king", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.white_pieces.append(piece)
                            row.append(piece)
                    # bot side
                    elif x == 6:
                        # pawn row
                        piece = Piece("assets/black/pawn.png","black","pawn",Coord(x,y),[(0,1)])
                        self.black_pieces.append(piece)
                        row.append(piece)
                    elif x == 7:
                        # rook
                        if y == 0 or y == 7:
                            piece = Piece("assets/black/rook.png", "black", "rook", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0)])
                            self.black_pieces.append(piece)
                            row.append(piece)
                        # knight
                        if y == 1 or y == 6:
                            piece = Piece("assets/black/knight.png", "black", "knight", Coord(x, y), [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)])
                            self.black_pieces.append(piece)
                            row.append(piece)
                        # bishop
                        if y == 2 or y == 5:
                            piece = Piece("assets/black/bishop.png", "black", "bishop", Coord(x, y), [(1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.black_pieces.append(piece)
                            row.append(piece)
                        # queen
                        if y == 4:
                            piece = Piece("assets/black/queen.png", "black", "queen", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.black_pieces.append(piece)
                            row.append(piece)
                        # king
                        if y == 3:
                            piece = Piece("assets/black/king.png", "black", "king", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.black_pieces.append(piece)
                            row.append(piece)
                    else:
                        row.append(None)
                else:
                    # top side
                    if x == 6:
                        piece = Piece("assets/white/pawn.png","white","pawn",Coord(x,y),[(0,1)])
                        self.white_pieces.append(piece)
                        row.append(piece)
                    elif x == 7:
                        if y == 0 or y == 7:
                            piece = Piece("assets/white/rook.png", "white", "rook", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0)])
                            self.white_pieces.append(piece)
                            row.append(piece)
                        if y == 1 or y == 6:
                            piece = Piece("assets/white/knight.png", "white", "knight", Coord(x, y), [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)])
                            self.white_pieces.append(piece)
                            row.append(piece)
                        if y == 2 or y == 5:
                            piece = Piece("assets/white/bishop.png", "white", "bishop", Coord(x, y), [(1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.white_pieces.append(piece)
                            row.append(piece)
                        if y == 3:
                            piece = Piece("assets/white/queen.png", "white", "queen", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.white_pieces.append(piece)
                            row.append(piece)
                        if y == 4:
                            piece = Piece("assets/white/king.png", "white", "king", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.white_pieces.append(piece)
                            row.append(piece)
                    # bot side
                    elif x == 1:
                        # pawn row
                        piece = Piece("assets/black/pawn.png","black","pawn",Coord(x,y),[(0,1)])
                        self.black_pieces.append(piece)
                        row.append(piece)
                    elif x == 0:
                        # rook
                        if y == 0 or y == 7:
                            piece = Piece("assets/black/rook.png", "black", "rook", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0)])
                            self.black_pieces.append(piece)
                            row.append(piece)
                        # knight
                        if y == 1 or y == 6:
                            piece = Piece("assets/black/knight.png", "black", "knight", Coord(x, y), [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)])
                            self.black_pieces.append(piece)
                            row.append(piece)
                        # bishop
                        if y == 2 or y == 5:
                            piece = Piece("assets/black/bishop.png", "black", "bishop", Coord(x, y), [(1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.black_pieces.append(piece)
                            row.append(piece)
                        # queen
                        if y == 3:
                            piece = Piece("assets/black/queen.png", "black", "queen", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.black_pieces.append(piece)
                            row.append(piece)
                        # king
                        if y == 4:
                            piece = Piece("assets/black/king.png", "black", "king", Coord(x, y), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)])
                            self.black_pieces.append(piece)
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
                    for elt in self.black_pieces:
                        if elt.rect.collidepoint(mouse_x, mouse_y):
                            self.selected_piece = elt
                    for elt in self.white_pieces:
                        if elt.rect.collidepoint(mouse_x, mouse_y):
                            self.selected_piece = elt
    
    def run(self):
        while self.running:
            self.handle_event()
            
            self.draw_board()
            
            pygame.display.flip()
        
        pygame.quit()

    def draw_board(self):
        self.screen.fill((255,255,255))
        start_x = (SCREEN_W - (CASE_SIZE * 8)) // 2
        start_y = (SCREEN_H - (CASE_SIZE * 8)) // 2
        
        for row in range(8):
            for case in range(8):
                bg_color = WHITE if (row+case)%2==0 else GRAYLIGHT
                pygame.draw.rect(self.screen, bg_color, (start_x + CASE_SIZE * row, start_y + CASE_SIZE *case, CASE_SIZE, CASE_SIZE))
                elt = self.board[case][row]
                if elt != None:
                    self.screen.blit(elt.image, (start_x + CASE_SIZE * row + (CASE_SIZE - elt.rect.w)/2 , start_y + CASE_SIZE * case + (CASE_SIZE - elt.rect.h)/2))