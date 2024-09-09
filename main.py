import tkinter as tk
from tkinter import messagebox, PhotoImage


# Global variables
current_player = "X"
board = ["", "", "", "", "", "", "", "", ""]
buttons = []

# Function to reset the game
def reset_game():
    global board, current_player
    board = ["", "", "", "", "", "", "", "", ""]
    current_player = "X"
    for button in buttons:
        button.config(text="")
        
# Function to switch the player
def switch_player():
    global current_player
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"

# Function to check for a winner
def check_winner():
    # Winning combinations
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "":
            return board[combo[0]]
    
    if "" not in board:  # If all cells are filled and no winner
        return "Draw"
    
    return None

# Function to handle button click
def on_click(index):
    global current_player
    if board[index] == "" and not check_winner():
        board[index] = current_player
        buttons[index].config(text = current_player)
        
        winner = check_winner()
        if winner:
            if winner == "Draw":
                messagebox.showinfo("Game Over", "It's a Draw!")
            else:
                messagebox.showinfo("Game Over", f"Player {winner} wins!")
            reset_game()
        else:
            switch_player()
    if current_player == "O":  # If it's the computer's turn
        best_move = find_best_move()
        on_click(best_move)


# Function to evaluate the board state
def evaluate():
    winner = check_winner()
    if winner == "X":  # Human wins
        return -1
    elif winner == "O":  # Computer wins
        return 1
    elif winner == "Draw":
        return 0
    return None

# Minimax algorithm
def minimax(is_maximizing):
    score = evaluate()
    
    # If a winner is found, return the score
    if score is not None:
        return score
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"  # Simulate the computer's move
                score = minimax(False)
                board[i] = ""  # Undo the move
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "X"  # Simulate the human's move
                score = minimax(True)
                board[i] = ""  # Undo the move
                best_score = min(best_score, score)
        return best_score

# Find the best move for the computer
def find_best_move():
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"  # Simulate the computer's move
            score = minimax(False)
            board[i] = ""  # Undo the move
            if score > best_score:
                best_score = score
                best_move = i
    return best_move


# Setting up the Tkinter window
window = tk.Tk()
window.title("Tic Tac Toe")

# Create the buttons for the grid
for i in range(9):
    button = tk.Button(window, text="", width=20, height=6, font=("Arial", 30),
                       command=lambda i=i: on_click(i))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

# Start the Tkinter event loop
window.mainloop()
