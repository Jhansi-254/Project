import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Tic Tac Toe AI")
root.configure(bg="#1e1e2e")
root.resizable(False, False)

board = [' ']*9
buttons = []
status = tk.StringVar(value="Your Turn (X)")

wins = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

# ---------- LOGIC ----------
def check_winner(player):
    for combo in wins:
        if all(board[i] == player for i in combo):
            return combo
    return None

def is_draw():
    return ' ' not in board

def minimax(is_max):
    if check_winner('O'): return 1
    if check_winner('X'): return -1
    if is_draw(): return 0

    if is_max:
        best = -100
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                best = max(best, minimax(False))
                board[i] = ' '
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                best = min(best, minimax(True))
                board[i] = ' '
        return best

# ---------- AI MOVE ----------
def ai_move():
    status.set("AI Thinking 🤖")
    root.update()

    best_score = -100
    move = 0
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i

    board[move] = 'O'
    buttons[move].config(text='O', fg="#ff4d4d", bg="#2a2a40", state="disabled")

    win = check_winner('O')
    if win:
        highlight(win, "#ff4d4d")
        show_popup("AI WINS 🤖", "#ff4d4d")
    elif is_draw():
        draw_effect()
        show_popup("DRAW 🤝", "#ffaa00")
    else:
        status.set("Your Turn (X)")

# ---------- PLAYER MOVE ----------
def click(i):
    if board[i] == ' ':
        board[i] = 'X'
        buttons[i].config(text='X', fg="#00d4ff", bg="#2a2a40", state="disabled")

        win = check_winner('X')
        if win:
            highlight(win, "#00d4ff")
            show_popup("YOU WIN 🎉", "#00d4ff")
            return
        if is_draw():
            draw_effect()
            show_popup("DRAW 🤝", "#ffaa00")
            return

        ai_move()

# ---------- VISUAL EFFECTS ----------
def highlight(combo, color):
    for i in combo:
        buttons[i].config(bg="#ffd700", fg=color)

def draw_effect():
    for b in buttons:
        b.config(bg="#ffcc66")

def show_popup(text, color):
    popup = tk.Toplevel(root)
    popup.configure(bg="#1e1e2e")
    popup.geometry("300x150")
    popup.title("Result")

    tk.Label(
        popup,
        text=text,
        font=("Arial", 20, "bold"),
        fg=color,
        bg="#1e1e2e"
    ).pack(expand=True)

    tk.Button(
        popup,
        text="Play Again",
        font=("Arial", 12),
        command=lambda: [popup.destroy(), restart()],
        bg=color,
        fg="black"
    ).pack(pady=10)

# ---------- RESTART ----------
def restart():
    global board
    board = [' ']*9
    status.set("Your Turn (X)")
    for b in buttons:
        b.config(text=' ', state='normal', bg="#3b3b5c", fg="white")

# ---------- UI ----------
tk.Label(
    root,
    textvariable=status,
    font=("Arial", 14),
    fg="#00d4ff",
    bg="#1e1e2e"
).grid(row=0, column=0, columnspan=3, pady=10)

for i in range(9):
    btn = tk.Button(
        root,
        text=' ',
        font=('Arial', 26, "bold"),
        width=5,
        height=2,
        bg="#3b3b5c",
        fg="white",
        command=lambda i=i: click(i)
    )
    btn.grid(row=1+i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

tk.Button(
    root,
    text="Restart Game",
    font=("Arial", 12),
    bg="#ffaa00",
    fg="black",
    command=restart
).grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()
