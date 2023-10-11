import pygame
import pygame.freetype
from const import *
from Piece import *
from Move import Move
from function import move_to_chess

background_image = pygame.image.load('assets/wood_bg.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_W, SCREEN_H))


class Chess:
    def __init__(self) -> None:
        self.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Chess")
        ico = pygame.image.load("assets/chess_icon.ico")
        pygame.display.set_icon(ico)

        self.clock = pygame.time.Clock()
        
        self.app_running:bool = True

        self.start_x = (SCREEN_W - (CASE_SIZE * 8)) // 2
        self.start_y = (SCREEN_H - (CASE_SIZE * 8)) // 2
    
    def init(self):
        pygame.init()
        pygame.font.init()

    def init_var(self):
        self.game_running = True
        self.promotion = False
        self.turn:str = "white"
        self.checkmate:str = None
        self.selected_piece:Piece|None = None
        self.end_message:str = ""

        self.board:list[list[Piece|None]] = []
        self.piece_list:list[Piece] = []
        self.possible_move:list[Move] = []
        self.log_move:list[Move] = []       
        
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
    
    def run(self):
        while self.app_running:
            
            # handle event
            self.menu_handle_event()

            # refresh_graphic
            self.menu_refresh_graphic()
        
        pygame.quit()
    
    def menu_handle_event(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.app_running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self.game()
                elif e.key == pygame.K_ESCAPE:
                    self.app_running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.white_B.collidepoint(mouse_x, mouse_y):
                        self.botside = "white"
                        self.game()
                    elif self.black_B.collidepoint(mouse_x, mouse_y):
                        self.botside = "black"
                        self.game()
    
    def menu_refresh_graphic(self):
        self.screen.fill((0,0,0))
        self.screen.blit(background_image,(0,0))

        width = 150
        height = 100
        x = (SCREEN_W - width) // 2
        y = (SCREEN_H - height) // 2 - height - 10
        self.white_B = self.draw_button(x, y, width, height, "White", bg=WHITE, fg=BLACK, font_size=50)
        width = 150
        height = 100
        x = (SCREEN_W - width) // 2
        y = (SCREEN_H - height) // 2 + 10
        self.black_B = self.draw_button(x, y, width, height, "Black", bg=BLACK, fg=WHITE, font_size=50)
        
        pygame.display.flip()
    
    def game(self):
        self.init_var()
        self.init_pieces()

        while self.game_running:
            self.handle_event()

            self.update_data()
            
            self.draw_board()
            
            pygame.display.flip()

            self.clock.tick(25)

    def handle_event(self):
        for evt in pygame.event.get():
            
            if evt.type == pygame.QUIT:
                self.game_running = False
                self.app_running = False

            elif evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_ESCAPE:
                        self.game_running = False
                elif evt.key == pygame.K_RETURN:
                        if self.checkmate:
                            self.init_var()
                            self.init_pieces()
                elif not self.promotion and not self.checkmate and evt.key == pygame.K_SPACE and len(self.log_move)>0:
                    self.unmove(self.log_move[-1])
                    self.log_move.pop()
                    self.turn = "black" if self.turn == "white" else "white"
                    self.selected_piece = None
                    self.possible_move = []
            
            elif not self.checkmate and evt.type == pygame.MOUSEBUTTONDOWN:
                
                if evt.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    x = (mouse_x - self.start_x)//CASE_SIZE
                    y = (mouse_y -self.start_y)//CASE_SIZE
                    
                    if not self.promotion :
                        selection = self.get_piece_at((x,y))
                        has_move = False

                        #verify if Click on a possible move
                        if self.selected_piece:
                            
                            for move in self.possible_move:
                                if move.end == (x, y):
                                    self.move(move)
                                    self.log_move.append(move)
                                    
                                    # pawn promotion
                                    if self.selected_piece.name == "pawn" and self.selected_piece.get_y() in [0,7]:
                                        self.promotion = True
                                        self.promote_piece = self.selected_piece
                                        
                                    has_move = True
                                    
                                    # clear selection
                                    self.selected_piece = None
                                    self.possible_move = []
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
                                    self.possible_move = []
                            else:
                                self.selected_piece = None
                                self.possible_move = []
                    else:
                        for elt in self.promote_choice:
                            if elt[0].collidepoint(mouse_x, mouse_y):
                                color = self.promote_piece.color
                                img = f"assets/{color}/{elt[1]}.png"
                                pos = (self.promote_piece.get_position())

                                match elt[1]:
                                    case "queen":
                                        obj = Queen(img, color, elt[1], pos)
                                    case "bishop":
                                        obj = Bishop(img, color, elt[1], pos)
                                    case "knight":
                                        obj = Knight(img, color, elt[1], pos)
                                    case "rook":
                                        obj = Rook(img, color, elt[1], pos)

                                self.piece_list.remove(self.promote_piece)
                                self.piece_list.append(obj)
                                self.set(self.promote_piece.get_position(), obj)
                                self.promotion = False
                                self.promote_choice.clear()
                    
    def update_data(self):
        
        # verify checkmate
        if self.is_in_checkmate(self.turn):
            self.checkmate = "white" if self.turn == "black" else "black"

        elif self.selected_piece:
            self.possible_move = self.filter_move(self.selected_piece)
        

    def draw_board(self):
        self.screen.fill(WOOD)
        self.screen.blit(background_image,(0,0))
        
        font = pygame.font.SysFont("Arial", 25)
        
        if self.promotion:
            self.display_pawn_promotion_choice(self.promote_piece)

        # display movement history        
        y_start = 200
        log_start = (len(self.log_move)-MAX_LOG) if len(self.log_move) >MAX_LOG else 0
        log_start = log_start - (log_start % 2)
        move_text = ""
        for i in range(log_start,len(self.log_move)):
            if (i+1) % 2 == 0:
                move_text += move_to_chess(self.log_move[i])
                text = font.render(move_text, True, WHITE)
                self.screen.blit(text, (650,y_start))
                move_text = ""
                y_start += 22
            else:
                move_text += move_to_chess(self.log_move[i]) + ' . '
                text = font.render(move_text, True, WHITE)
                self.screen.blit(text, (650,y_start))


        moves = [move.end for move in self.possible_move]
        for row in range(8):
            for col in range(8):
                bg_color = WHITEEGG if (row + col) % 2 == 0 else GREENLIGHT
                move_color = BLUELIGHT if (row + col) % 2 == 0 else BLUEDARK
                selected_color = YELLOWLIGHT if (row + col) % 2 == 0 else YELLOWDARK
                case_rect = pygame.Rect(
                    self.start_x + CASE_SIZE * row,
                    self.start_y + CASE_SIZE * col,
                    CASE_SIZE,
                    CASE_SIZE,
                )

                # highlight the selected piece
                if self.selected_piece and (row,col) == self.selected_piece.get_position():
                    pygame.draw.rect(self.screen, selected_color, case_rect)
                # highlight possible moves
                elif (row,col) in moves:
                    pygame.draw.rect(self.screen, move_color, case_rect)
                # highlight the king who is in check
                elif self.is_in_check(self.turn) and self.get_piece_at((row,col)) == self.get_king(self.turn):
                    pygame.draw.rect(self.screen, REDLIGHT, case_rect)
                # classic case draw
                else:
                    pygame.draw.rect(self.screen, bg_color, case_rect)

                # put the piece image on the Surface
                elt = self.get_piece_at((row,col))
                if isinstance(elt,Piece):
                    x = self.start_x + CASE_SIZE * elt.get_x() + (CASE_SIZE - IMG_SIZE)/2
                    y = self.start_y + CASE_SIZE * elt.get_y() + (CASE_SIZE - IMG_SIZE)/2
                    self.screen.blit(elt.image, (x,y))
        
        if self.checkmate:
            text1 = font.render(f"{self.checkmate} Player won !", True, BLACK, WHITE)
            text2 = font.render("Press \"Enter\" to start a new game", True, BLACK, WHITE)
            w1 = text1.get_width()
            w2 = text2.get_width()
            x1,y1 = (SCREEN_W - w1)//2, 30
            x2,y2 = (SCREEN_W - w2)//2, 70
            self.screen.blit(text1, (x1,y1))
            self.screen.blit(text2, (x2,y2))

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
        
        
    def is_in_check(self, color:str) -> Piece|bool:
        king = self.get_king(color)
        king_position = king.get_position()

        # go to check all ennemy pieces moves
        for p in self.get_pieces(king.get_opposite_color()):
            moves = [move.end for move in p.get_possible_moves(self)]
            if king_position in moves:
                return p

        return False
    
    def is_in_checkmate(self, color:str):

        if self.is_in_check(color) != False:
        
            # verify if a ally piece can move
            for piece in self.get_pieces(color):
        
                if len(self.filter_move(piece))>0:                
                    return False

            # if no one can move so checkmate
            return True

        return False
    
    def move(self, move:Move):
        move.target_piece.move(move.end)
        self.set(move.start,None)
        self.set(move.end, move.target_piece)

        if move.eat_piece:
            try:
                self.piece_list.remove(move.eat_piece)
            except:
                pass
        
        if move.second_target:
            move.second_target.move(move.second_end)
            self.set(move.second_start, None)
            self.set(move.second_end, move.second_target)

    def unmove(self, move:Move):
        move.target_piece.set_position(move.start)
        move.target_piece.step -= 1
        self.set(move.end,None)
        self.set(move.start,move.target_piece)

        if move.eat_piece:
            self.piece_list.append(move.eat_piece)
            self.set(move.eat_piece.get_position(), move.eat_piece)
        
        elif move.second_target:
            move.second_target.set_position(move.second_start)
            move.second_target.step -= 1
            self.set(move.second_end, None)
            self.set(move.second_start, move.second_target)
    
    def filter_move(self, piece:Piece):
        possible_moves = piece.get_possible_moves(self)
        
        legal_moves = []
        for move in possible_moves:
            # if the move is in the board
            if  0 <= move.end[0] < 8 and 0 <= move.end[1] < 8:
                # do the move
                self.move(move)

                # if the move doesn't get the player in check
                if self.is_in_check(self.turn) == False:

                    # So it's a legal move and add it
                    legal_moves.append(move)

                # cancel the move
                self.unmove(move)

        possible_moves = legal_moves
        return possible_moves

    def display_pawn_promotion_choice(self, pawn:Pawn):
        pieces = ["queen","rook","bishop","knight"]
        x,y = pawn.get_position()
        self.promote_choice:list[tuple[pygame.Rect,str]] = []
        coef = 1 if pawn.color == "black" else -1
        for i in range(len(pieces)):
            img = pygame.image.load(f"assets/{pawn.color}/full{pieces[i]}.png")
            rx = self.start_x + x * CASE_SIZE + img.get_width() * i
            ry = self.start_y + y + img.get_height() * coef
            self.screen.blit(img, (rx, ry))
            
            self.promote_choice.append((img.get_rect(x=rx,y=ry), pieces[i]))
    
    def draw_button(self, x:int, y:int, width:int, height:int, text:str, bg:tuple=WHITEEGG, fg:tuple=BLACK, font_size:int=15):
        r = pygame.draw.rect(self.screen, bg, (x, y, width, height))

        button_font = pygame.font.Font(None, font_size)
        text_surface = button_font.render(text, True, fg)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + width // 2, y + height // 2)

        self.screen.blit(text_surface, text_rect)

        return r