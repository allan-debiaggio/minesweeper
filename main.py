from tkinter import *
from cell import Cell
import settings
import utilities

root = Tk()

# Override the settings of the window
root.configure(bg="Black")
root.geometry(f"{settings.WIDTH}x{settings.HEIGHT}")
root.title("Minesweeper")
root.resizable(False, False)

top_frame = Frame(
    root,
    bg = "black", # Change color to see the frame
    width = settings.WIDTH,
    height = utilities.height_prct(25),
)
top_frame.place(x = 0, y = 0)

game_title = Label(
    top_frame,
    bg = "black",
    fg = "white",
    text = "Minesweeper",
    font = ("", 42)
)

game_title.place(
    x = utilities.width_prct(25),
    y = 0
)

left_frame = Frame(
    root,
    bg = "black", # Change color to see the frame
    width = utilities.width_prct(25),
    height = utilities.height_prct(75)
)
left_frame.place(x=0, y= utilities.height_prct(25))

center_frame = Frame(
    root,
    bg = "black", # Change color to see the frame
    width = utilities.width_prct(75),
    height = utilities.height_prct(75)
)
center_frame.place(
    x = utilities.width_prct(25),
    y = utilities.height_prct(25)
)

for x in range(settings.GRID_SIZE) :
    for y in range(settings.GRID_SIZE) :
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
            column = x, row = y
        )

# Call the label from the Cell class
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x = 0, y = 0)

Cell.randomize_mines()

# Run the window
root.mainloop()