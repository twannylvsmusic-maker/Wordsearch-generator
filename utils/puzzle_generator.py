import random
import string
from .shape_masks import get_shape_mask

def generate_puzzle(words, shape='square', size=None, allow_vertical=True, allow_horizontal=True, allow_diagonal=True):
    """
    Generate a word search puzzle with the given words and shape.
    
    Args:
        words: List of words to place
        shape: Shape of the puzzle ('square', 'circle', 'heart', 'dog', etc.)
        size: Base size of the grid (auto-calculated if None)
        allow_vertical: Whether to allow vertical word placement
        allow_horizontal: Whether to allow horizontal word placement
        allow_diagonal: Whether to allow diagonal word placement
    
    Returns:
        tuple: (grid, placed_words) where grid is a 2D list and placed_words is a list of placed words
    """
    
    # Auto-calculate size based on longest word if not provided
    if size is None:
        max_word_length = max(len(word) for word in words) if words else 10
        if shape == 'square':
            # Limit square shape to 12x12 maximum
            size = min(12, max(8, max_word_length + 2))  # Between 8 and 12 for square
        else:
            size = max(20, min(30, max_word_length + 8))  # Between 20 and 30 for other shapes
    
    # Enforce 12x12 limit for square shapes even if user specifies larger size
    if shape == 'square' and size > 12:
        size = 12
    
    # Get the shape mask
    mask = get_shape_mask(shape, size)
    grid_size = len(mask)
    
    # Initialize grid with empty spaces
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Sort words by length (longest first) for better placement
    words = sorted(words, key=len, reverse=True)
    
    placed_words = []
    
    # Try to place each word, with multiple attempts
    for word in words:
        # Try up to 10 times to place difficult words (increased from 3)
        placed = False
        for attempt in range(10):
            if place_word(grid, mask, word, allow_vertical, allow_horizontal, allow_diagonal):
                placed_words.append(word)
                placed = True
                break
        
        # If word still couldn't be placed after 10 attempts, continue to next word
        if not placed:
            print(f"Warning: Could not place word '{word}' after 10 attempts")
    
    # Fill empty spaces with random letters
    for i in range(grid_size):
        for j in range(grid_size):
            if mask[i][j] and not grid[i][j]:
                grid[i][j] = random.choice(string.ascii_uppercase)
    
    return grid, placed_words

def place_word(grid, mask, word, allow_vertical=True, allow_horizontal=True, allow_diagonal=True):
    """
    Try to place a word in the grid.
    
    Returns:
        bool: True if word was placed successfully
    """
    
    directions = []
    if allow_horizontal:
        directions.extend([(0, 1), (0, -1)])  # Left-right, Right-left
    if allow_vertical:
        directions.extend([(1, 0), (-1, 0)])  # Top-bottom, Bottom-top
    if allow_diagonal:
        directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])  # Diagonals
    
    # Try multiple random starting positions (increased to 200 for better placement)
    positions = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if mask[i][j]]
    random.shuffle(positions)
    
    # Limit positions to try (but try more if we have fewer valid positions)
    max_positions = min(len(positions), 200)
    
    for start_i, start_j in positions[:max_positions]:
        for di, dj in directions:
            if can_place_word(grid, mask, word, start_i, start_j, di, dj):
                place_word_at(grid, word, start_i, start_j, di, dj)
                return True
    
    return False

def can_place_word(grid, mask, word, start_i, start_j, di, dj):
    """
    Check if a word can be placed at the given position and direction.
    """
    for k, letter in enumerate(word):
        i = start_i + k * di
        j = start_j + k * dj
        
        # Check bounds
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
            return False
        
        # Check if position is allowed by mask
        if not mask[i][j]:
            return False
        
        # Check if position is empty or has the same letter
        if grid[i][j] and grid[i][j] != letter:
            return False
    
    return True

def place_word_at(grid, word, start_i, start_j, di, dj):
    """
    Place a word in the grid at the given position and direction.
    """
    for k, letter in enumerate(word):
        i = start_i + k * di
        j = start_j + k * dj
        grid[i][j] = letter
