import ChessBoard


class ChessPiece:

    selected = False
    is_king = False

    def __init__(self, is_red):
        self.is_red = is_red

    def count_pieces(self, board, x, y, dx, dy):
        sx = dx/abs(dx) if dx!=0 else 0
        sy = dy/abs(dy) if dy!=0 else 0
        nx, ny = x + dx, y + dy
        x, y = x + sx, y + sy
        cnt = 0
        while x != nx or y != ny:
            if board.pieces.get((x, y)):
                cnt += 1
            x += sx
            y += sy
        return cnt
