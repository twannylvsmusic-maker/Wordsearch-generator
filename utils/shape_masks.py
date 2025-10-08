def get_shape_mask(shape, size=15):
    """
    Get a boolean mask for the specified shape.
    
    Args:
        shape: Name of the shape ('square', 'circle', 'heart', 'dog', etc.)
        size: Base size of the grid
    
    Returns:
        2D list of booleans indicating valid positions
    """
    
    if shape == 'square':
        return create_square_mask(size)
    elif shape == 'circle':
        return create_circle_mask(size)
    elif shape == 'heart':
        return create_heart_mask(size)
    elif shape == 'star':
        return create_star_mask(size)
    elif shape == 'diamond':
        return create_diamond_mask(size)
    elif shape == 'triangle':
        return create_triangle_mask(size)
    elif shape == 'hexagon':
        return create_hexagon_mask(size)
    elif shape == 'dog':
        return create_dog_mask(size)
    elif shape == 'cat':
        return create_cat_mask(size)
    elif shape == 'fish':
        return create_fish_mask(size)
    elif shape == 'butterfly':
        return create_butterfly_mask(size)
    elif shape == 'flower':
        return create_flower_mask(size)
    elif shape == 'tree':
        return create_tree_mask(size)
    elif shape == 'house':
        return create_house_mask(size)
    elif shape == 'car':
        return create_car_mask(size)
    else:
        # Default to square
        return create_square_mask(size)

def create_square_mask(size):
    """Create a square mask."""
    return [[True for _ in range(size)] for _ in range(size)]

def create_circle_mask(size):
    """Create a circular mask."""
    mask = []
    center = size // 2
    radius = center
    
    for i in range(size):
        row = []
        for j in range(size):
            # Distance from center
            distance = ((i - center) ** 2 + (j - center) ** 2) ** 0.5
            row.append(distance <= radius)
        mask.append(row)
    
    return mask

def create_heart_mask(size):
    """Create a heart-shaped mask."""
    mask = []
    center_x = size // 2
    center_y = size // 2
    scale = size / 15.0  # Scale factor for consistent sizing
    
    for i in range(size):
        row = []
        for j in range(size):
            # Normalize coordinates to -1 to 1 range
            x = (j - center_x) / (center_x * 0.8)
            y = (center_y - i) / (center_y * 0.8)
            
            # Simplified heart shape using two circles and a triangle
            # Top circles
            left_circle = ((x + 0.5) ** 2 + (y - 0.5) ** 2) <= 0.5
            right_circle = ((x - 0.5) ** 2 + (y - 0.5) ** 2) <= 0.5
            
            # Bottom triangle
            bottom = (y <= 0.5) and (abs(x) <= 1 - y) and (y >= -1)
            
            row.append(left_circle or right_circle or bottom)
        mask.append(row)
    
    return mask

def create_star_mask(size):
    """Create a star-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # Create a 5-pointed star using distance and angle
            distance = (x*x + y*y) ** 0.5
            
            # Create a star by combining a circle with extended points
            # Center circle
            center_circle = distance <= center * 0.4
            
            # Points extending from center
            point_north = abs(x) <= center * 0.2 and y >= 0 and y <= center
            point_south = abs(x) <= center * 0.2 and y <= 0 and y >= -center
            point_east = abs(y) <= center * 0.2 and x >= 0 and x <= center
            point_west = abs(y) <= center * 0.2 and x <= 0 and x >= -center
            
            # Diagonal points
            point_ne = abs(x - y) <= center * 0.15 and x >= 0 and y >= 0
            point_nw = abs(x + y) <= center * 0.15 and x <= 0 and y >= 0
            point_se = abs(x + y) <= center * 0.15 and x >= 0 and y <= 0
            point_sw = abs(x - y) <= center * 0.15 and x <= 0 and y <= 0
            
            is_star = center_circle or point_north or point_south or point_east or point_west or point_ne or point_nw or point_se or point_sw
            
            row.append(is_star and distance <= center)
        mask.append(row)
    
    return mask

def create_diamond_mask(size):
    """Create a diamond-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            # Diamond: |x| + |y| <= center
            distance = abs(i - center) + abs(j - center)
            row.append(distance <= center)
        mask.append(row)
    
    return mask

def create_triangle_mask(size):
    """Create a triangle-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            # Triangle: y >= center - x and y >= x - center and y <= center
            if i <= center and j >= center - i and j <= center + i:
                row.append(True)
            else:
                row.append(False)
        mask.append(row)
    
    return mask

def create_hexagon_mask(size):
    """Create a hexagon-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # Hexagon: |x| <= center and |y| <= center and |x + y| <= center
            if abs(x) <= center and abs(y) <= center and abs(x + y) <= center:
                row.append(True)
            else:
                row.append(False)
        mask.append(row)
    
    return mask

def create_dog_mask(size):
    """Create a simple dog-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            # Simple dog shape: oval body with triangular head
            x = j - center
            y = center - i
            
            # Body (oval)
            body = (x*x / (center*center)) + (y*y / (center*center*0.7)) <= 1
            
            # Head (smaller oval at top)
            head = (x*x / ((center*0.6)**2)) + ((y-center*0.3)**2 / ((center*0.4)**2)) <= 1
            
            row.append(body or head)
        mask.append(row)
    
    return mask

def create_cat_mask(size):
    """Create a simple cat-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            # Similar to dog but with pointed ears
            x = j - center
            y = center - i
            
            # Body (oval)
            body = (x*x / (center*center)) + (y*y / (center*center*0.7)) <= 1
            
            # Head with pointed ears
            head = (x*x / ((center*0.6)**2)) + ((y-center*0.3)**2 / ((center*0.4)**2)) <= 1
            
            # Ears (triangular points)
            ears = (abs(x) <= center*0.3 and y >= center*0.2)
            
            row.append(body or head or ears)
        mask.append(row)
    
    return mask

def create_fish_mask(size):
    """Create a simple fish-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # Fish body (oval)
            body = (x*x / (center*center*0.8)) + (y*y / (center*center*0.5)) <= 1
            
            # Tail
            tail = (x <= -center*0.5 and abs(y) <= center*0.3)
            
            row.append(body or tail)
        mask.append(row)
    
    return mask

def create_butterfly_mask(size):
    """Create a butterfly-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # Butterfly wings (four ovals)
            wing1 = ((x-center*0.3)**2 / (center*0.4)**2) + (y*y / (center*0.6)**2) <= 1
            wing2 = ((x+center*0.3)**2 / (center*0.4)**2) + (y*y / (center*0.6)**2) <= 1
            
            row.append(wing1 or wing2)
        mask.append(row)
    
    return mask

def create_flower_mask(size):
    """Create a flower-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # Flower petals (multiple circles)
            petal1 = ((x-center*0.4)**2 + y*y) <= (center*0.3)**2
            petal2 = ((x+center*0.4)**2 + y*y) <= (center*0.3)**2
            petal3 = (x*x + (y-center*0.4)**2) <= (center*0.3)**2
            petal4 = (x*x + (y+center*0.4)**2) <= (center*0.3)**2
            
            # Center
            center_circle = (x*x + y*y) <= (center*0.2)**2
            
            row.append(petal1 or petal2 or petal3 or petal4 or center_circle)
        mask.append(row)
    
    return mask

def create_tree_mask(size):
    """Create a tree-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # Tree trunk (rectangle at bottom)
            trunk = (abs(x) <= center*0.1 and y <= -center*0.3)
            
            # Tree top (triangle)
            top = (y >= -center*0.3 and abs(x) <= (y + center*0.3) * 0.5)
            
            row.append(trunk or top)
        mask.append(row)
    
    return mask

def create_house_mask(size):
    """Create a house-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # House base (rectangle)
            base = (abs(x) <= center*0.4 and y >= -center*0.3 and y <= center*0.3)
            
            # House roof (triangle)
            roof = (y >= center*0.3 and abs(x) <= (center*0.8 - y*0.5))
            
            row.append(base or roof)
        mask.append(row)
    
    return mask

def create_car_mask(size):
    """Create a car-shaped mask."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # Car body (rectangle with rounded corners)
            body = (abs(x) <= center*0.6 and abs(y) <= center*0.2)
            
            # Car wheels
            wheel1 = ((x-center*0.4)**2 + (y-center*0.15)**2) <= (center*0.1)**2
            wheel2 = ((x+center*0.4)**2 + (y-center*0.15)**2) <= (center*0.1)**2
            
            row.append(body or wheel1 or wheel2)
        mask.append(row)
    
    return mask
