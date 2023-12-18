import chess
import chess.svg
import tkinter as tk
from PIL import Image, ImageTk
import io
import cairosvg

class ChessApp:
    def __init__(self, master):
        self.master = master
        master.title("Chess Game")

        self.board = chess.Board()
        self.selected_square = None

        self.panel = tk.Label(master, image=None)
        self.panel.pack()
        self.update_board()

        self.panel.bind("<Button-1>", self.on_square_click)
        self.panel.bind("<B1-Motion>", self.on_drag)
        self.panel.bind("<ButtonRelease-1>", self.on_drop)

    def update_board(self):
        svg_data = chess.svg.board(board=self.board)
        png_data = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"))
        img = Image.open(io.BytesIO(png_data))
        img = img.resize((400, 400), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        self.panel.configure(image=img)
        self.panel.image = img

    def square_from_xy(self, x, y):
        row = 7 - (y // 50)  # Assuming each square is 50x50 pixels
        col = x // 50
        return chess.square(col, row)

    def on_square_click(self, event):
        x, y = event.x, event.y
        self.selected_square = self.square_from_xy(x, y)

    def on_drag(self, event):
        if self.selected_square is not None:
            x, y = event.x, event.y
            self.update_board()
            self.draw_dragged_piece(x, y)

    def on_drop(self, event):
        if self.selected_square is not None:
            x, y = event.x, event.y
            target_square = self.square_from_xy(x, y)
            move = chess.Move(self.selected_square, target_square)

            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_board()

            self.selected_square = None

    def draw_dragged_piece(self, x, y):
        piece = self.board.piece_at(self.selected_square)
        if piece is not None:
            # img = ImageTk.PhotoImage(self.get_piece_image(piece))
            self.panel.create_image(x, y, anchor=tk.NW, image=img)
            self.panel.image = img

    # def get_piece_image(self, piece):
    #     piece_image_path = f"pieces/{piece.symbol()}.png"  # Adjust path accordingly
    #     img = Image.open(piece_image_path)
    #     img = img.resize((50, 50), Image.LANCZOS)
    #     return img

def main():
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
