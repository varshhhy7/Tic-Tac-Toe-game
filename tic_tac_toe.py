from tkinter import *
import random

window = Tk()
window.title("TIC-TAC-TOE")
window.geometry("600x700")

players = ["X", "O"]
player = "X"  # 🔧 Always start with "X"
buttons = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
game_mode = None
current_theme = "light"

light_theme = {
    "bg": "#ffffff",
    "fg": "#000000",
    "button_bg": "#f0f0f0",
    "highlight": "lightgreen"
}

dark_theme = {
    "bg": "#2c2c2c",
    "fg": "#ffffff",
    "button_bg": "#444444",
    "highlight": "#33cc33"
}

theme = light_theme

def next_turn(row, column):
    global player

    if buttons[row][column]["text"] == "" and check_winner() is False:
        buttons[row][column]["text"] = player
        buttons[row][column]["fg"] = "blue" if player == "X" else "red"

        if check_winner() is False:
            player = players[1] if player == players[0] else players[0]
            label.config(text=player + " turn")

            if game_mode == "single" and player == "O":
                window.after(500, computer_move)

        elif check_winner() is True:
            label.config(text=player + " wins! 🎉")
        elif check_winner() == "Tie":
            label.config(text="It's a Tie! 🤝")

def computer_move():
    available = [(r, c) for r in range(3) for c in range(3) if buttons[r][c]["text"] == ""]
    if available:
        row, col = random.choice(available)
        next_turn(row, col)

def check_winner():
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            highlight_buttons([(i, 0), (i, 1), (i, 2)])
            return True
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            highlight_buttons([(0, i), (1, i), (2, i)])
            return True

    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        highlight_buttons([(0, 0), (1, 1), (2, 2)])
        return True

    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        highlight_buttons([(0, 2), (1, 1), (2, 0)])
        return True

    if not empty_space():
        return "Tie"

    return False

def empty_space():
    for row in buttons:
        for btn in row:
            if btn["text"] == "":
                return True
    return False

def highlight_buttons(coords):
    for r, c in coords:
        buttons[r][c].config(bg=theme["highlight"])

def new_game():
    global player
    player = "X"  # 🔧 Always reset to "X"
    label.config(text=player + " turn")
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="", bg=theme["button_bg"], fg=theme["fg"])

def toggle_theme():
    global theme, current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    theme = dark_theme if current_theme == "dark" else light_theme
    apply_theme()

def apply_theme():
    window.config(bg=theme["bg"])
    if "label" in globals():
        label.config(bg=theme["bg"], fg=theme["fg"])
    if "reset_button" in globals():
        reset_button.config(bg=theme["button_bg"], fg=theme["fg"])
    if "back_button" in globals():
        back_button.config(bg=theme["button_bg"], fg=theme["fg"])
    if "toggle_button" in globals():
        toggle_button.config(bg=theme["button_bg"], fg=theme["fg"])
    if "buttons" in globals():
        for row in buttons:
            for btn in row:
                if isinstance(btn, Button):
                    btn.config(bg=theme["button_bg"], fg=theme["fg"])
    if "start_frame" in globals():
        start_frame.config(bg=theme["bg"])
        for widget in start_frame.winfo_children():
            widget.config(bg=theme["button_bg"], fg=theme["fg"])

def back_to_menu():
    game_frame.destroy()
    label.destroy()
    reset_button.destroy()
    back_button.destroy()
    toggle_button.destroy()
    show_start_menu()

def start_game(mode):
    global game_mode, label, reset_button, back_button, toggle_button, game_frame, player
    game_mode = mode
    start_frame.destroy()
    player = "X"  # 🔧 Always start with human as "X"

    label_text = player + " turn"
    label_font = ('consolas', 40)
    label = Label(window, text=label_text, font=label_font)
    label.pack(pady=10)

    reset_button = Button(window, text="🔄 Restart", font=('consolas', 16), command=new_game)
    reset_button.pack(pady=5)

    back_button = Button(window, text="⬅️ Main Menu", font=('consolas', 16), command=back_to_menu)
    back_button.pack(pady=5)

    toggle_button = Button(window, text="🌗 Toggle Theme", font=('consolas', 16), command=toggle_theme)
    toggle_button.pack(pady=5)

    game_frame = Frame(window)
    game_frame.pack()

    for row in range(3):
        for col in range(3):
            buttons[row][col] = Button(
                game_frame,
                text="",
                font=('consolas', 40),
                width=5,
                height=2,
                bg=theme["button_bg"],
                fg=theme["fg"],
                command=lambda r=row, c=col: next_turn(r, c)
            )
            buttons[row][col].grid(row=row, column=col)

    apply_theme()

def show_start_menu():
    global start_frame
    start_frame = Frame(window, bg=theme["bg"])
    start_frame.pack(expand=True)

    Label(start_frame, text="Choose Game Mode", font=('consolas', 30),
          bg=theme["bg"], fg=theme["fg"]).pack(pady=20)

    Button(start_frame, text="👫 Play with Friend", font=('consolas', 20), width=20,
           bg=theme["button_bg"], fg=theme["fg"], command=lambda: start_game("multi")).pack(pady=10)

    Button(start_frame, text="🤖 Play with Computer", font=('consolas', 20), width=20,
           bg=theme["button_bg"], fg=theme["fg"], command=lambda: start_game("single")).pack(pady=10)

    apply_theme()

show_start_menu()
window.mainloop()
