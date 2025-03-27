# Dimensions de la fenêtre
WIDTH = 1440
HEIGHT = 720

# Niveaux de difficulté
DIFFICULTY = {
    'easy': {
        'GRID_SIZE': 8,
        'MINES_COUNT': 10
    },
    'medium': {
        'GRID_SIZE': 16,
        'MINES_COUNT': 40
    },
    'hard': {
        'GRID_SIZE': 24,
        'MINES_COUNT': 99
    }
}

# Niveau par défaut
current_difficulty = 'easy'
GRID_SIZE = DIFFICULTY[current_difficulty]['GRID_SIZE']
MINES_COUNT = DIFFICULTY[current_difficulty]['MINES_COUNT']
CELL_COUNT = GRID_SIZE ** 2