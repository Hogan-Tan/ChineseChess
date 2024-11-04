import tkinter as Tkinter


def board_coord(x):
    return 30 + 40*x


class ChessView:
    root = Tkinter.Tk()
    root.title("Chinese Chess")
    root.resizable(None, None)
    can = Tkinter.Canvas(root, width=373, height=410)
    can.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)
    img = Tkinter.PhotoImage(file="images/WHITE.gif")
    can.create_image(0, 0, image=img, anchor=Tkinter.NW)
    piece_images = dict()
    move_images = []

    def draw_board(self, board):
        self.piece_images.clear()
        self.move_images = []
        pieces = board.pieces
        for (x, y) in pieces.keys():
            self.piece_images[x, y] = Tkinter.PhotoImage(file=pieces[x, y].get_image_file_name())
            self.can.create_image(board_coord(x), board_coord(y), image=self.piece_images[x, y])
        if board.selected_piece:
            (ox, oy), piece = board.selected_piece
            for (x, y) in board.get_move_locs(board, ox, oy):
                self.move_images.append(Tkinter.PhotoImage(file="images/OOS.gif"))
                self.can.create_image(board_coord(x), board_coord(y), image=self.move_images[-1])
        else:
            last_move = list(pieces.keys())[-1]
            self.move_images.append(Tkinter.PhotoImage(file="images/OOS.gif"))
            self.can.create_image(board_coord(last_move[0]), board_coord(last_move[1]), image=self.move_images[-1])


    def showMsg(self, msg):
        self.root.title(msg)

    def __init__(self, control):
        self.control = control
        self.root.bind('<KeyPress-a>', self.control.press_a)
        self.root.bind('<KeyPress-b>', self.control.press_b)
        self.root.bind('<KeyPress-c>', self.control.press_c)
        self.can.bind('<Button-1>', self.control.callback)

    @staticmethod
    def start():
        Tkinter.mainloop()
