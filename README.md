# Minesweeper  
  
Implement a program that is a Minesweeper game.  
  
## Possible outcomes :  
- Revealed square is a mine, it explodes, the game ends
- Revealed square is empty and not directly adjacent to one or more mines, setting a chain
reaction that reveals all adjacent empty squares and the outlining numbers
- Revealed square is empty and is adjacent to one or more mines, displaying a number indicating
number of mines next to it (from 1 to 8)  
  
## Prerequisites :  
- Python
- Graphics library
- Object Oriented Programming
- Recursive Programming
- The mines are placed after the first click (One could never hit a mine on his first click)
- Same set of rules as the original (Flags / questionmarks)
- Different difficulties (map size, number of mines, number of flags / questionmarks)
- Dinamically allocated mines number (rand between min and max, depending on difficulty)
- In game Timer
- Button to reset game
  
## Going Further :
- Display on game window the remaining number of mines to find and number of flags / questionmarks
put on the board
- Number of flags / Questionmarks (depending on)
- Scoring / High scores (Super bonus) 