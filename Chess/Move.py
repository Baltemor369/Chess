class Move:
    def __init__(self, start:tuple[int,int], end:tuple[int,int], target, eat_piece=None, second_target=None, second_end:tuple[int,int]=None) -> None:
        self.start:tuple[int,int] = start
        self.end:tuple[int,int] = end
        self.target_piece = target
        self.eat_piece = eat_piece
        # for castling
        self.second_target = second_target
        self.second_end:tuple[int,int] = second_end
    
    def __repr__(self) -> str:
        return f"{self.target_piece} {self.start}->{self.end} || {self.eat_piece} || {self.second_end} || {self.second_target}"