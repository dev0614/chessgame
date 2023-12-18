import chess
import chess.svg
import tkinter as tk
from PIL import Image, ImageTk
import io
import cairosvg

# Initialize the board
board = chess.Board()
selected_piece = None  # Initialize the selected_piece variable

def update_board():
    svg_data = chess.svg.board(board=board)
    png_data = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"))
    img = Image.open(io.BytesIO(png_data))
    img = img.resize((400, 400), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    panel.configure(image=img)
    panel.image = img

# Function to handle user's move
def handle_click(event):
    global selected_piece
    rank = int(event.y / 50)  # Adjust the division factor according to your board size
    file = int(event.x / 50)  # Adjust the division factor according to your board size
    square = chess.square(file, rank)

    if selected_piece is None:
        piece_at_square = board.piece_at(square)
        if piece_at_square and piece_at_square.color == board.turn:
            selected_piece = square
    else:
        move = chess.Move(selected_piece, square)
        if move in board.legal_moves:
            board.push(move)
            selected_piece = None
            update_board()
            play_ai_move()

# AI Logic
def play_ai_move():
    # Implement your AI logic here
    pass

# Create the GUI window
root = tk.Tk()
root.title("Chess Game")

panel = tk.Label(root, image=None)
panel.pack()

# Display the initial board
update_board()

selected_piece = None
panel.bind("<Button-1>", handle_click)

root.mainloop()
