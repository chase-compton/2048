from tkinter import Frame, Label, CENTER
import csv
import numpy as np

import game_functions
import monte_carlo_ai

EDGE_LENGTH = 600
CELL_COUNT = 4
CELL_PAD = 5

UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY = "'d'"
AI_KEY = "'q'"
AI_PLAY_KEY = "'p'"
RESTART_KEY = "'r'"

SEARCHES_PER_MOVE = 30

SEARCH_LENGTH = 20

LABEL_FONT = ("Verdana", 40, "bold")

GAME_COLOR = "#BBADA0"

EMPTY_COLOR = "#CCC0B3"

TILE_COLORS = {
    2: "#F6E8DD",
    4: "#F9E5CD",
    8: "#FEB274",
    16: "#FE975C",
    32: "#FE7E5B",
    64: "#F65E3B",
    128: "#FECD64",
    256: "#EDCC61",
    512: "#FFD966",
    1024: "#FEC868",
    2048: "#F0A500",
    4096: "#B784AB",
    8192: "#E45826",
}

LABEL_COLORS = {
    2: "#736A61",
    4: "#736A61",
    8: "#F9FCF9",
    16: "#F9FCF9",
    32: "#F9FCF9",
    64: "#F9FCF9",
    128: "#F9FCF9",
    256: "#F9FCF9",
    512: "#F9FCF9",
    1024: "#F9FCF9",
    2048: "#F9FCF9",
    4096: "#F9FCF9",
    8192: "#F9FCF9",
}


class Display(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title("2048")
        self.master.bind("<Key>", self.key_press)

        self.commands = {
            UP_KEY: game_functions.move_up,
            DOWN_KEY: game_functions.move_down,
            LEFT_KEY: game_functions.move_left,
            RIGHT_KEY: game_functions.move_right,
            AI_KEY: monte_carlo_ai.ai_move,
        }

        self.grid_cells = []
        self.build_grid()
        self.init_matrix()
        self.draw_grid_cells()
        self.add_current_score()
        self.add_high_score()
        self.add_game_over()

        self.mainloop()

    def build_grid(self):
        background = Frame(self, bg=GAME_COLOR, width=EDGE_LENGTH, height=EDGE_LENGTH)
        background.grid(pady=(200, 200))

        for row in range(CELL_COUNT):
            grid_row = []
            for col in range(CELL_COUNT):
                cell = Frame(
                    background,
                    bg=EMPTY_COLOR,
                    width=EDGE_LENGTH / CELL_COUNT,
                    height=EDGE_LENGTH / CELL_COUNT,
                )
                cell.grid(row=row, column=col, padx=CELL_PAD, pady=CELL_PAD)
                t = Label(
                    master=cell,
                    text="",
                    bg=EMPTY_COLOR,
                    justify=CENTER,
                    font=LABEL_FONT,
                    width=5,
                    height=2,
                )
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = game_functions.initialize_game()

    def draw_grid_cells(self):
        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                tile_value = self.matrix[row][col]
                if not tile_value:
                    self.grid_cells[row][col].configure(text="", bg=EMPTY_COLOR)
                else:
                    self.grid_cells[row][col].configure(
                        text=str(tile_value),
                        bg=TILE_COLORS[tile_value],
                        fg=LABEL_COLORS[tile_value],
                    )
        self.update_idletasks()

    def add_current_score(self):
        score_frame = Frame(self)
        score_frame.place(relx=0.5, rely=0.1, anchor="center")
        Label(score_frame, text="Score", font=LABEL_FONT, fg="#736A61").grid(row=0)
        self.score_label = Label(score_frame, text="0", font=LABEL_FONT, fg="#736A61")
        self.score_label.grid(row=1)

    def add_high_score(self):
        high_score_frame = Frame(self)
        high_score_frame.place(relx=0.5, rely=0.9, anchor="center")
        Label(
            high_score_frame,
            text="High Score",
            font=LABEL_FONT,
            fg="#736A61",
        ).grid(row=0)
        self.high_score_label = Label(
            high_score_frame, text="0", font=LABEL_FONT, fg="#736A61"
        )
        self.high_score_label.grid(row=1)

    def add_game_over(self):
        self.game_over_frame = Frame(self.master, borderwidth=2)
        self.game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.game_over_label = Label(
            self.game_over_frame, text="", bg=GAME_COLOR, fg="#736A61", font=LABEL_FONT
        )
        self.game_over_label.pack_forget()

    def game_over(self):
        if game_functions.check_for_win(self.matrix):
            self.game_over_label.config(text="You Win!")
            self.game_over_label.pack()
        elif game_functions.check_for_loss(self.matrix):
            self.game_over_label.config(text="Game Over!")
            self.game_over_label.pack()

    def update_score(self, current_score):
        self.score_label.config(text=current_score + int(self.score_label.cget("text")))
        self.high_score_label.config(
            text=max(
                int(self.score_label.cget("text")),
                int(self.high_score_label.cget("text")),
            )
        )
    def restart(self):
        self.game_over_frame.destroy()
        self.add_game_over()
        self.init_matrix()
        self.draw_grid_cells()
        self.score_label.config(text="0")

    def key_press(self, event):
        valid_game = True
        key = repr(event.char)
        self.game_over()
        if key == RESTART_KEY:
            self.restart()
        else:
            if key == AI_PLAY_KEY:
                move_count = 0
                while (
                    valid_game
                    and not game_functions.check_for_win(self.matrix)
                    and not game_functions.check_for_loss(self.matrix)
                ):
                    self.matrix, valid_game, current_score = monte_carlo_ai.ai_move(
                        self.matrix, SEARCHES_PER_MOVE, SEARCH_LENGTH
                    )
                    self.update_score(current_score)
                    if valid_game:
                        self.matrix = game_functions.add_new_tile(self.matrix)
                        self.draw_grid_cells()
                    move_count += 1
                self.game_over()

            if key == AI_KEY:
                self.matrix, move_made, current_score = monte_carlo_ai.ai_move(
                    self.matrix, SEARCHES_PER_MOVE, SEARCH_LENGTH
                )
                if move_made:
                    self.matrix = game_functions.add_new_tile(self.matrix)
                    self.draw_grid_cells()
                    move_made = False
                    self.update_score(current_score)

            elif key in self.commands:
                self.matrix, move_made, current_score = self.commands[repr(event.char)](
                    self.matrix
                )
                if move_made:
                    self.matrix = game_functions.add_new_tile(self.matrix)
                    self.draw_grid_cells()
                    move_made = False
                    self.update_score(current_score)


gamegrid = Display()
