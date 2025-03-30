from tkinter import Button, Label
from PIL import Image, ImageTk
import random
import settings
import ctypes
import sys
import pygame

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    first_click = True
    game_over = False  # Track whether the game has ended
    images = {
        'numbers': [],
        'mine': None,
        'flag': None,
        'question': None,
        'empty': None,
        'default': None
    }
    assets = None  # Reference to the assets instance

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_flagged = False
        self.is_questionmark = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            image=Cell.images['default'],
            bg='black',
            activebackground='black',
            bd=0,
            highlightthickness=0,
            borderwidth=0,
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        """
        Create a label to display the number of remaining clickable cells.
        """
        if Cell.cell_count_label_object:
            Cell.cell_count_label_object.destroy()  # Remove the old label if it exists

        Cell.cell_count_label_object = Label(
            location,
            bg="black",
            fg="white",
            text=f"Cells Left: {Cell.cell_count - settings.MINES_COUNT}",
            font=("", 16)
        )
        Cell.cell_count_label_object.place(x=0, y=0)

    def left_click_actions(self, event):
        if Cell.game_over:  # Prevent interactions if the game is over
            return

        if Cell.first_click:
            Cell.randomize_mines(exclude_cell=self)
            Cell.first_click = False

        if self.is_mine:
            Cell.assets.play_audio('mine')  # Play mine sound
            self.show_mine()
            Cell.game_over = True  # Set game_over to True
        else:
            Cell.assets.play_audio('click')  # Play click sound
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()

            if Cell.cell_count == settings.MINES_COUNT:
                Cell.assets.play_audio('victory')  # Play victory sound
                ctypes.windll.user32.MessageBoxW(
                    0, "You win the game!", "Game Over!", 0
                )
                Cell.game_over = True  # Set game_over to True

        self.cell_btn_object.unbind("<Button-1>")
        self.cell_btn_object.unbind("<Button-3>")

    def get_cell_by_axis(self, x, y):
        # Return cell object based on x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            self.is_opened = True
            Cell.cell_count -= 1  # Decrement the cell count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.config(
                    text=f"Cells Left: {Cell.cell_count - settings.MINES_COUNT}"
                )

            # Update the button appearance
            if self.surrounded_cells_mines_length > 0:
                self.cell_btn_object.configure(
                    image=Cell.images['numbers'][self.surrounded_cells_mines_length - 1]
                )
            else:
                self.cell_btn_object.configure(
                    image=Cell.images['empty']
                )

    def show_mine(self):
        Cell.assets.play_audio('game_over')  # Play game over sound
        self.cell_btn_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0, "You clicked on a mine!", "Game Over!", 0)

    def right_click_actions(self, event):
        if Cell.game_over or self.is_opened:  # Prevent interactions if the game is over or cell is opened
            return

        if not self.is_flagged:
            self.cell_btn_object.configure(image=Cell.images['flag'])
            self.is_flagged = True
            Cell.assets.play_audio('flag')  # Play flag sound
        elif not self.is_questionmark:
            self.cell_btn_object.configure(image=Cell.images['question'])
            self.is_questionmark = True
            Cell.assets.play_audio('questionmark')  # Play questionmark sound
        else:
            self.cell_btn_object.configure(image=Cell.images['default'])
            self.is_flagged = False
            self.is_questionmark = False

    @staticmethod
    def randomize_mines(exclude_cell=None):
        if exclude_cell:
            # Exclude the first clicked cell and its neighbors
            available_cells = [
                cell for cell in Cell.all
                if cell != exclude_cell and cell not in exclude_cell.surrounded_cells
            ]
        else:
            # If no exclude_cell is provided, use all cells
            available_cells = Cell.all

        # Randomly select cells to be mines
        picked_cells = random.sample(available_cells, settings.MINES_COUNT)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    @staticmethod
    def load_images():
        if settings.current_difficulty == "hard":
            cell_size = 20
        else:
            cell_size = 30  # Default size
        
        # Load number images (1-8)
        for i in range(1, 9):
            image = Image.open(f"assets/images/{i}.png")
            image = image.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
            Cell.images['numbers'].append(ImageTk.PhotoImage(image))

        # Load other images
        for img_name in ['default', 'mine', 'flag', 'question', 'empty']:
            image = Image.open(f"assets/images/case_{img_name}.png")
            image = image.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
            Cell.images[img_name] = ImageTk.PhotoImage(image)

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"