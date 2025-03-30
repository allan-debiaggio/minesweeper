from tkinter import *
from cell import Cell
import settings
import utilities
import pygame
import ctypes
from assets import ClassicAssets, HomemadeAssets

class Game:
    def __init__(self):
        self.root = Tk()
        self.classic_assets = ClassicAssets()
        self.homemade_assets = HomemadeAssets()
        self.current_assets = self.classic_assets  # Start with ClassicAssets
        Cell.assets = self.current_assets

        self.setup_window()
        self.create_frames()
        self.create_widgets()
        self.configure_grid()
        Cell.load_images()
        self.create_cells()
        Cell.create_cell_count_label(self.left_frame)

    def setup_window(self):
        self.root.configure(bg="Black")
        self.root.geometry(f"{settings.WIDTH}x{settings.HEIGHT}")
        self.root.title("Minesweeper")
        self.root.resizable(False, False)

    def create_frames(self):
        self.top_frame = Frame(self.root, bg="black", width=settings.WIDTH, height=utilities.height_prct(25))
        self.top_frame.place(x=0, y=0)

        self.left_frame = Frame(self.root, bg="black", width=utilities.width_prct(25), height=utilities.height_prct(75))
        self.left_frame.place(x=0, y=utilities.height_prct(25))

        self.center_frame = Frame(self.root, bg="black", width=utilities.width_prct(75), height=utilities.height_prct(75))
        self.center_frame.place(x=utilities.width_prct(25), y=utilities.height_prct(25))

    def create_widgets(self):
        game_title = Label(self.top_frame, bg="black", fg="white", text="Minesweeper", font=("", 42))
        game_title.place(x=utilities.width_prct(25), y=0)

        self.toggle_btn = Button(self.top_frame, text="Homemade", width=10, bg="blue", fg="white", command=self.toggle_assets)
        self.toggle_btn.place(x=utilities.width_prct(5), y=utilities.height_prct(5))
        self.toggle_btn.bind("<Enter>", self.play_hover_sound)

        difficulty_frame = Frame(self.top_frame, bg="black")
        difficulty_frame.place(x=utilities.width_prct(60), y=utilities.height_prct(5))

        easy_btn = Button(difficulty_frame, text="Easy", width=10, bg="green", fg="white", command=lambda: self.change_difficulty('easy'))
        easy_btn.grid(row=0, column=0, padx=5)
        easy_btn.bind("<Enter>", self.play_hover_sound)  # Bind hover sound

        medium_btn = Button(difficulty_frame, text="Medium", width=10, bg="orange", fg="white", command=lambda: self.change_difficulty('medium'))
        medium_btn.grid(row=0, column=1, padx=5)
        medium_btn.bind("<Enter>", self.play_hover_sound)  # Bind hover sound

        hard_btn = Button(difficulty_frame, text="Hard", width=10, bg="red", fg="white", command=lambda: self.change_difficulty('hard'))
        hard_btn.grid(row=0, column=2, padx=5)
        hard_btn.bind("<Enter>", self.play_hover_sound)  # Bind hover sound

        win_btn = Button(difficulty_frame, text="Win", width=10, bg="purple", fg="white", command=self.simulate_win)
        win_btn.grid(row=1, column=0, padx=5, pady=5)
        win_btn.bind("<Enter>", self.play_hover_sound)  # Bind hover sound

    def configure_grid(self):
        for i in range(settings.GRID_SIZE):
            self.center_frame.grid_columnconfigure(i, weight=1, uniform="cells", pad=0)
            self.center_frame.grid_rowconfigure(i, weight=1, uniform="cells", pad=0)

    def create_cells(self):
        for x in range(settings.GRID_SIZE):
            for y in range(settings.GRID_SIZE):
                c = Cell(x, y)
                c.create_btn_object(self.center_frame)
                c.cell_btn_object.grid(column=x, row=y, padx=0, pady=0, sticky='nsew')

    def toggle_assets(self):
        if self.toggle_btn['text'] == "Homemade":
            self.toggle_btn['text'] = "Classic"
            self.current_assets = self.homemade_assets
        else:
            self.toggle_btn['text'] = "Homemade"
            self.current_assets = self.classic_assets
        Cell.assets = self.current_assets

    def restart_game(self):
        for widget in self.center_frame.winfo_children():
            widget.destroy()
        Cell.all = []
        Cell.cell_count = settings.CELL_COUNT
        Cell.first_click = True
        Cell.game_over = False
        self.configure_grid()
        self.create_cells()
        Cell.create_cell_count_label(self.left_frame)

    def change_difficulty(self, level):
        settings.current_difficulty = level
        settings.GRID_SIZE = settings.DIFFICULTY[level]['GRID_SIZE']
        settings.MINES_COUNT = settings.DIFFICULTY[level]['MINES_COUNT']
        settings.CELL_COUNT = settings.GRID_SIZE ** 2
        Cell.images = {'numbers': [], 'mine': None, 'flag': None, 'question': None, 'empty': None, 'default': None}
        Cell.load_images()
        self.restart_game()

    def play_hover_sound(self, event):
        self.current_assets.play_audio('hover')  # Use the hover sound from assets

    def simulate_win(self):
        Cell.cell_count = settings.MINES_COUNT
        Cell.assets.play_audio('victory')
        ctypes.windll.user32.MessageBoxW(0, "You win the game!", "Game Over!", 0)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = Game()
    game.run()