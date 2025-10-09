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
            # Non-square shapes: fixed 15x15 grid for perfect symmetry
            size = 15  # Fixed 15x15 for non-square shapes
    
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
    
    # For non-square shapes, remove empty columns to make grid more compact
    if shape != 'square':
        grid = remove_empty_columns(grid)
    
    # Apply symmetry correction for non-square shapes
    if shape != 'square':
        grid = fix_symmetry(grid, shape)
    
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

def remove_empty_columns(grid):
    """
    Remove empty columns from the grid to make it more compact.
    Keeps all rows but removes columns that are completely empty.
    Returns the trimmed grid.
    """
    if not grid or not grid[0]:
        return grid
    
    # Find non-empty columns (columns that have at least one non-empty cell)
    non_empty_cols = []
    for j in range(len(grid[0])):
        if any(row[j] for row in grid):
            non_empty_cols.append(j)
    
    if not non_empty_cols:
        return grid
    
    # Create trimmed grid with only non-empty columns
    trimmed_grid = []
    for row in grid:
        trimmed_row = [row[j] for j in non_empty_cols]
        trimmed_grid.append(trimmed_row)
    
    return trimmed_grid

def analyze_symmetry(grid):
    """
    Analyze the symmetry of the grid by counting letters in each row and column.
    Returns dictionaries with letter counts for rows and columns.
    """
    if not grid or not grid[0]:
        return {}, {}
    
    rows = len(grid)
    cols = len(grid[0])
    
    # Count letters in each row
    row_counts = {}
    for i in range(rows):
        count = sum(1 for cell in grid[i] if cell and cell.strip())
        row_counts[i] = count
    
    # Count letters in each column
    col_counts = {}
    for j in range(cols):
        count = sum(1 for i in range(rows) if grid[i][j] and grid[i][j].strip())
        col_counts[j] = count
    
    return row_counts, col_counts

def fix_symmetry(grid, shape='square'):
    """
    Fix asymmetry in non-square shapes by strategically adding letters.
    For shapes like circle, heart, star, ensure better symmetry while respecting shape boundaries.
    """
    if shape == 'square':
        return grid  # Square shapes don't need symmetry correction
    
    if not grid or not grid[0]:
        return grid
    
    # Get the shape mask to respect boundaries
    from .shape_masks import get_shape_mask
    size = len(grid)
    mask = get_shape_mask(shape, size)
    
    # Get current symmetry analysis
    row_counts, col_counts = analyze_symmetry(grid)
    
    # Create a copy to work with
    fixed_grid = [row[:] for row in grid]
    
    # Fix column symmetry (left vs right) - only within shape boundaries
    cols = len(fixed_grid[0])
    for j in range(cols // 2):
        left_col = j
        right_col = cols - 1 - j
        
        left_count = col_counts.get(left_col, 0)
        right_count = col_counts.get(right_col, 0)
        
        # If there's an imbalance, add letters to the side with fewer letters
        if left_count < right_count:
            # Add letters to left column - only within shape boundaries
            for i in range(len(fixed_grid)):
                if (mask[i][left_col] and 
                    (not fixed_grid[i][left_col] or not fixed_grid[i][left_col].strip())):
                    # Add a random letter to balance - only within shape
                    import random
                    fixed_grid[i][left_col] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                    break
        elif right_count < left_count:
            # Add letters to right column - only within shape boundaries
            for i in range(len(fixed_grid)):
                if (mask[i][right_col] and 
                    (not fixed_grid[i][right_col] or not fixed_grid[i][right_col].strip())):
                    # Add a random letter to balance - only within shape
                    import random
                    fixed_grid[i][right_col] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                    break
    
    # Fix row symmetry (top vs bottom) - only within shape boundaries
    rows = len(fixed_grid)
    for i in range(rows // 2):
        top_row = i
        bottom_row = rows - 1 - i
        
        top_count = row_counts.get(top_row, 0)
        bottom_count = row_counts.get(bottom_row, 0)
        
        # If there's an imbalance, add letters to the side with fewer letters
        if top_count < bottom_count:
            # Add letters to top row - only within shape boundaries
            for j in range(len(fixed_grid[top_row])):
                if (mask[top_row][j] and 
                    (not fixed_grid[top_row][j] or not fixed_grid[top_row][j].strip())):
                    # Add a random letter to balance - only within shape
                    import random
                    fixed_grid[top_row][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                    break
        elif bottom_count < top_count:
            # Add letters to bottom row - only within shape boundaries
            for j in range(len(fixed_grid[bottom_row])):
                if (mask[bottom_row][j] and 
                    (not fixed_grid[bottom_row][j] or not fixed_grid[bottom_row][j].strip())):
                    # Add a random letter to balance - only within shape
                    import random
                    fixed_grid[bottom_row][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                    break
    
    return fixed_grid
