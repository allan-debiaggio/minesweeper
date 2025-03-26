from tkinter import Button, Label
import random
import settings
import ctypes
import sys

class Cell :
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    def __init__(self, x, y, is_mine = False):
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
            width = 12,
            height = 4,
        )
        btn.bind("<Button-1>", self.left_click_actions)
        btn.bind("<Button-3>", self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location) :
        lbl = Label(
            location,
            bg = "black",
            fg = "white",
            text=f"Cells Left:{Cell.cell_count}",
            font = ("", 20)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event) :
        if self.is_mine :
            self.show_mine()
        else :
            if self.surrounded_cells_mines_length == 0 :
                for cell_obj in self.surrounded_cells :
                    cell_obj.show_cell()
            self.show_cell()

            # If mines count == remaining cells count, player won
            if Cell.cell_count == settings.MINES_COUNT :
                ctypes.windll.user32.MessageBoxW(
                    0, "You won the game !", "Game Over !", 0)

        # Cancel left and right click actions if cell is already open :
        self.cell_btn_object.unbind("<Button-1>")
        self.cell_btn_object.unbind("<Button-3>")

    def get_cell_by_axis(self, x, y) :
        # Return cell object based on x and y
        for cell in Cell.all :
            if cell.x == x and cell.y == y :
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
        for cell in self.surrounded_cells :
            if cell.is_mine :
                counter += 1
            
        return counter

    def show_cell(self) :
        if not self.is_opened :
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            # Replace the text of cell count label with newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}")
            # If this was a flagged cell, make it go back to original
            # color after left click
            self.cell_btn_object.configure(
                bg = "SystemButtonFace"
            )
        # Mark the cell as opened (need to use it at the last line)
        self.is_opened = True

    def show_mine(self) :
        # Logic to interrupt the game and display a message
        # that player lost
        self.cell_btn_object.configure(bg = "red")
        ctypes.windll.user32.MessageBoxW(0, "You clicked on a mine !", "Game Over !", 0)
        sys.exit()

    def right_click_actions(self, event) :
        if not self.is_flagged :
            self.cell_btn_object.configure(
                bg="orange"
            )
            self.is_flagged = True
        elif not self.is_questionmark :
            self.cell_btn_object.configure(
                bg = "yellow"
            )
            self.is_questionmark = True
        else :
            self.cell_btn_object.configure(
                bg = "SystemButtonFace"
            )
            self.is_flagged = False
            self.is_questionmark = False
    
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        for picked_cell in picked_cells :
            picked_cell.is_mine = True


    def __repr__(self) :
        return f"Cell({self.x}, {self.y})"