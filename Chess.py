import chess
import chess.svg
import tkinter as tk
from PIL import Image, ImageTk
import io
import cairosvg

# Initialize the board
board = chess.Board()


def update_board():
    svg_data = chess.svg.board(board=board)

    # Convert SVG to PNG format using cairosvg
    png_data = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"))

    # Open the PNG image from the converted data
    img = Image.open(io.BytesIO(png_data))
    img = img.resize((400, 400), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)

    panel.configure(image=img)
    panel.image = img

# Evaluation function (simple material count)
def evaluate_board(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # King value not used for this evaluation
    }

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            score += piece_values[piece.piece_type] * (1 if piece.color == chess.WHITE else -1)

    return score


# Minimax with alpha-beta pruning (adapted for GUI)
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# Function to make the AI move using minimax with alpha-beta pruning
def play_ai_move():
    best_move = None
    best_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    depth = 3  # Set the search depth (you can adjust this value)

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, alpha, beta, False)
        board.pop()
        if eval > best_eval:
            best_eval = eval
            best_move = move

    if best_move is not None:
        board.push(best_move)
        update_board()


# Function to handle user's move
def play_user_move():
    user_move = entry.get()
    try:
        board.push_uci(user_move)
        update_board()
        play_ai_move()  # After the user moves, let the AI respond
    except ValueError:
        print("Invalid move! Try again.")


# Create the GUI window
root = tk.Tk()
root.title("Chess Game")

panel = tk.Label(root, image=None)
panel.pack()
# Display the initial board
update_board()

# Entry for user's move
entry = tk.Entry(root)
entry.pack()

# Button to submit user's move
submit_button = tk.Button(root, text="Submit Move", command=play_user_move)
submit_button.pack()

root.mainloop()

# Function to check for checkmate or stalemate
def check_game_status():
    if board.is_checkmate():
        print("Checkmate! Game Over.")
        return True
    elif board.is_stalemate():
        print("Stalemate! Game Over.")
        return True
    return False

# Function to reset the game
def reset_game():
    board.reset()
    update_board()

# Function to handle user's move
def play_user_move():
    user_move = entry.get()
    try:
        board.push_uci(user_move)
        update_board()
        if not check_game_status():
            play_ai_move()  # After the user moves, let the AI respond
    except ValueError:
        print("Invalid move! Try again.")

# Create the GUI window
root = tk.Tk()
root.title("Chess Game")

panel = tk.Label(root, image=None)
panel.pack()

# Display the initial board
update_board()

# Entry for user's move
entry = tk.Entry(root)
entry.pack()

# Button to submit user's move
submit_button = tk.Button(root, text="Submit Move", command=play_user_move)
submit_button.pack()

# Button to reset the game
reset_button = tk.Button(root, text="Reset Game", command=reset_game)
reset_button.pack()
print("Hi, this is a chess game")
root.mainloop()