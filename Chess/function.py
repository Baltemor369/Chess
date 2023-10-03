def matrix_to_chess(pos:tuple[int,int]):
    return f"{chr(pos[0]+97)}{8-pos[1]}"

def move_to_chess(move):
    if not move.second_target:
        pos = matrix_to_chess(move.end)
        if move.target_piece.name == "king":
            piece = move.target_piece.name[0:1]
        elif move.target_piece.name == "pawn":
            piece = ""
        else:
            piece = move.target_piece.name[0]
    else:
        
        if move.target_piece.get_x() - move.second_target.get_x() == -1:
            piece = "0-0"
            pos = ""
        else:
            piece = "0-0-0"
            pos = ""
    return f"{piece.upper()}{pos}"