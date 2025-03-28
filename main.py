from tkinter import *
from cell import Cell
import settings
import utilities
import pygame
from assets import ClassicAssets, HomemadeAssets

# Initialize assets
classic_assets = ClassicAssets()
homemade_assets = HomemadeAssets()
Cell.assets = classic_assets  # Start with ClassicAssets

# Function to toggle assets
def toggle_assets():
    global Cell
    if toggle_btn['text'] == "Homemade":
        toggle_btn['text'] = "Classic"
        Cell.assets = homemade_assets  # Switch to HomemadeAssets
    else:
        toggle_btn['text'] = "Homemade"
        Cell.assets = classic_assets  # Switch to ClassicAssets

def restart_game():
    # Clear existing grid
    for widget in center_frame.winfo_children():
        widget.destroy()
    Cell.all = []
    Cell.cell_count = settings.CELL_COUNT
    Cell.first_click = True  # Reset first_click to True

    # Configure grid without spacing
    for i in range(settings.GRID_SIZE):
        center_frame.grid_columnconfigure(i, weight=1, uniform="cells", pad=0)
        center_frame.grid_rowconfigure(i, weight=1, uniform="cells", pad=0)

    # Recreate grid
    for x in range(settings.GRID_SIZE):
        for y in range(settings.GRID_SIZE):
            c = Cell(x, y)
            c.create_btn_object(center_frame)
            c.cell_btn_object.grid(
                column=x,
                row=y,
                padx=0,
                pady=0,
                ipady=0,
                ipadx=0,  
                sticky='nsew'
            )
    Cell.create_cell_count_label(left_frame)
    # Remove this line to prevent premature mine placement
    # Cell.randomize_mines()

def change_difficulty(level):
    settings.current_difficulty = level
    settings.GRID_SIZE = settings.DIFFICULTY[level]['GRID_SIZE']
    settings.MINES_COUNT = settings.DIFFICULTY[level]['MINES_COUNT']
    settings.CELL_COUNT = settings.GRID_SIZE ** 2

    # Reset images with new size
    Cell.images = {
        'numbers': [],
        'mine': None,
        'flag': None,
        'question': None,
        'empty': None,
        'default': None
    }
    Cell.load_images()
    restart_game()  # Restart the game, which resets first_click

def play_hover_sound(event):
    Cell.assets.play_audio('hover')

root = Tk()

# Override the settings of the window
root.configure(bg="Black")
root.geometry(f"{settings.WIDTH}x{settings.HEIGHT}")
root.title("Minesweeper")
root.resizable(False, False)

# Create frames
top_frame = Frame(
    root,
    bg="black",
    width=settings.WIDTH,
    height=utilities.height_prct(25)
)
top_frame.place(x=0, y=0)

game_title = Label(
    top_frame,
    bg="black",
    fg="white",
    text="Minesweeper",
    font=("", 42)
)

game_title.place(
    x=utilities.width_prct(25),
    y=0
)

# Add the toggle button to the left of the title
toggle_btn = Button(
    top_frame,
    text="Homemade",
    width=10,
    bg="blue",
    fg="white",
    command=toggle_assets
)
toggle_btn.place(
    x=utilities.width_prct(5),
    y=utilities.height_prct(5)
)

# Bind hover sound to the toggle button
toggle_btn.bind("<Enter>", play_hover_sound)

# Create difficulty buttons frame
difficulty_frame = Frame(
    top_frame,
    bg="black"
)
difficulty_frame.place(
    x=utilities.width_prct(60),
    y=utilities.height_prct(5)
)

# Difficulty buttons
easy_btn = Button(
    difficulty_frame,
    text="Easy",
    width=10,
    bg="green",
    fg="white",
    command=lambda: change_difficulty('easy')
)
easy_btn.grid(row=0, column=0, padx=5)

medium_btn = Button(
    difficulty_frame,
    text="Medium",
    width=10,
    bg="orange",
    fg="white",
    command=lambda: change_difficulty('medium')
)
medium_btn.grid(row=0, column=1, padx=5)

hard_btn = Button(
    difficulty_frame,
    text="Hard",
    width=10,
    bg="red",
    fg="white",
    command=lambda: change_difficulty('hard')
)
hard_btn.grid(row=0, column=2, padx=5)

# Bind hover events to difficulty buttons
easy_btn.bind("<Enter>", play_hover_sound)
medium_btn.bind("<Enter>", play_hover_sound)
hard_btn.bind("<Enter>", play_hover_sound)

left_frame = Frame(
    root,
    bg="black",  # Change color to see the frame
    width=utilities.width_prct(25),
    height=utilities.height_prct(75)
)
left_frame.place(x=0, y=utilities.height_prct(25))

center_frame = Frame(
    root,
    bg="black",  # Change color to see the frame
    width=utilities.width_prct(75),
    height=utilities.height_prct(75),

)

center_frame.place(
    x=utilities.width_prct(25),
    y=utilities.height_prct(25)
)

# Configure grid
for i in range(settings.GRID_SIZE):
    center_frame.grid_columnconfigure(i, weight=1, uniform="cells", pad=0)
    center_frame.grid_rowconfigure(i, weight=1, uniform="cells", pad=0)

# Load images
Cell.load_images()

# Create cells
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
            column=x,
            row=y,
            padx=0,
            pady=0,
            sticky='nsew'
        )

# Create cell count label
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=0, y=0)

# Initialize mines
# Cell.randomize_mines()

# Run the window
root.mainloop()