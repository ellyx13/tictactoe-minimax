import tkinter as tk
from tkinter import messagebox, PhotoImage


# Global variables
human = "O"
computer= "X"
current_player = human # Human player
board = ["", "", "", "", "", "", "", "", ""]
buttons = []

# Function to reset the game
def reset_game():
    global board, current_player
    board = ["", "", "", "", "", "", "", "", ""]
    current_player = human
    for button in buttons:
        button.config(text="")
        
# Function to switch the player
def switch_player():
    global current_player
    if current_player == human:
        current_player = computer
    else:
        current_player = human

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
    if current_player == computer:  # If it's the computer's turn
        best_move = find_best_move()
        on_click(best_move)


# Function to evaluate the board state
def evaluate():
    winner = check_winner()
    if winner == human:  # Human wins
        return -10
    elif winner == computer:  # Computer wins
        return 10
    elif winner == "Draw":
        return 0
    return None

# Helper function to print the current board state
def print_board(turn):
    tab_size = '\t' * turn
    print(f"{tab_size} Turn {turn}")
    for i in range(0, 9, 3):
        print(f"{tab_size} {board[i:i+3]}")
    print()

# Minimax algorithm
def minimax(is_maximizing, turn):
    turn += 1
    score = evaluate()
    print(f"Current board, is maximizing {is_maximizing}:")
    print_board(turn)

    # If a winner is found, return the score
    if score is not None:
        return score
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = computer  # Simulate the computer's move
                score = minimax(False, turn)
                board[i] = ""  # Undo the move
                best_score = max(best_score, score)
                print(f"Maximizing - Updated Best Score: {best_score}")
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = human  # Simulate the human's move
                score = minimax(True, turn)
                board[i] = ""  # Undo the move
                best_score = min(best_score, score)
                print(f"Minimizing - Updated Best Score: {best_score}")
        return best_score

# Find the best move for the computer
def find_best_move():
    best_score = -float('inf')
    best_move = None
    print("\n\n =========================== Current board ============================ \n\n")
    turn = 0
    print_board(turn)
    for i in range(9):
        if board[i] == "":
            board[i] = computer  # Simulate the computer's move
            score = minimax(False, turn)
            board[i] = ""  # Undo the move
            if score > best_score:
                best_score = score
                best_move = i
            if best_score == 1:
                return best_move
    return best_move    


# Setting up the Tkinter window
window = tk.Tk()
window.title("Tic Tac Toe")

# Create the buttons for the grid
for i in range(9):
    button = tk.Button(window, text="", width=20, height=6, font=("Arial", 30),
                       command=lambda i=i: on_click(i))
    button.grid(row=i // 3, column=i % 3)
    if board[i] != '':
        button.config(text=board[i])
    buttons.append(button)

# Start the Tkinter event loop
window.mainloop()
