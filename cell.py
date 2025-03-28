from tkinter import Button, Label
from PIL import Image, ImageTk
import random
import settings
import ctypes
import sys

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    first_click = True  # Track if it's the first click
    images = {
        'numbers': [],
        'mine': None,
        'flag': None,
        'question': None,
        'empty': None,
        'default': None
    }

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_flagged = False
        self.is_questionmark = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append the object to the Cell.all list
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
        lbl = Label(
            location,
            bg="black",
            fg="white",
            text=f"Cells Left:{Cell.cell_count}",
            font=("", 20)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if Cell.first_click:
            # Randomize mines, excluding the first clicked cell
            Cell.randomize_mines(exclude_cell=self)
            Cell.first_click = False  # Set first_click to False after the first click

        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()

            # If mines count == remaining cells count, player won
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(
                    0, "You win the game!", "Game Over!", 0
                )

        # Cancel left and right click actions if cell is already open
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
            Cell.cell_count -= 1
            if self.surrounded_cells_mines_length > 0:
                self.cell_btn_object.configure(
                    image=Cell.images['numbers'][self.surrounded_cells_mines_length - 1],
                    bg='black',
                    activebackground='black',
                    bd=0,
                    relief='flat',
                    highlightthickness=0
                )
            else:
                self.cell_btn_object.configure(
                    image=Cell.images['empty'],
                    bg='black',
                    activebackground='black',
                    bd=0,
                    relief='flat',
                    highlightthickness=0
                )
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}")
        self.is_opened = True

    def show_mine(self):
        # Logic to interrupt the game and display a message that player lost
        self.cell_btn_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0, "You clicked on a mine!", "Game Over!", 0)
        sys.exit()

    def right_click_actions(self, event):
        if not self.is_flagged:
            self.cell_btn_object.configure(
                image=Cell.images['flag']
            )
            self.is_flagged = True
        elif not self.is_questionmark:
            self.cell_btn_object.configure(
                image=Cell.images['question']
            )
            self.is_questionmark = True
        else:
            self.cell_btn_object.configure(
                image=Cell.images['default']
            )
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