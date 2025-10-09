def get_shape_mask(shape, size=15):
    """
    Get a boolean mask for the specified shape.
    
    Args:
        shape: Name of the shape ('square', 'circle', 'heart', 'dog', etc.)
        size: Base size of the grid
    
    Returns:
        2D list of booleans indicating valid positions
    """
    
    # Check if it's a custom shape first
    custom_mask = get_custom_shape(shape)
    if custom_mask is not None:
        # Resize custom mask to target size if needed
        if len(custom_mask) != size or len(custom_mask[0]) != size:
            # Simple resize by sampling or padding
            return resize_mask(custom_mask, size)
        return custom_mask
    
    # Built-in shapes
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
    """Create a circular mask optimized for maximum letter placement."""
    mask = []
    center = size // 2
    # Use a slightly larger radius to fill more of the shape
    radius = center - 0.5  # Slightly larger than center for better coverage
    
    for i in range(size):
        row = []
        for j in range(size):
            # Distance from center
            distance = ((i - center) ** 2 + (j - center) ** 2) ** 0.5
            # Use a more generous radius for better symmetry and coverage
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
    """Create a dog-shaped mask with improved symmetry and coverage."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # Body (larger, more symmetrical oval)
            body = (x*x / ((center*0.8)**2)) + (y*y / ((center*0.6)**2)) <= 1
            
            # Head (larger, more centered)
            head = (x*x / ((center*0.7)**2)) + ((y-center*0.2)**2 / ((center*0.5)**2)) <= 1
            
            # Ears (floppy dog ears)
            ears = (abs(x) <= center*0.5 and y >= center*0.1 and abs(x) >= center*0.3)
            
            # Tail (curved extension)
            tail = (x >= center*0.6 and abs(y) <= center*0.3)
            
            # Snout (small extension)
            snout = (y <= -center*0.2 and abs(x) <= center*0.2)
            
            row.append(body or head or ears or tail or snout)
        mask.append(row)
    
    return mask

def create_cat_mask(size):
    """Create a cat-shaped mask with improved symmetry and coverage."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # Body (larger, more symmetrical oval)
            body = (x*x / ((center*0.8)**2)) + (y*y / ((center*0.6)**2)) <= 1
            
            # Head (larger, more centered)
            head = (x*x / ((center*0.7)**2)) + ((y-center*0.2)**2 / ((center*0.5)**2)) <= 1
            
            # Ears (larger triangular points)
            ears = (abs(x) <= center*0.4 and y >= center*0.1 and abs(x) >= center*0.2)
            
            # Tail (curved extension)
            tail = (x >= center*0.6 and abs(y) <= center*0.3)
            
            row.append(body or head or ears or tail)
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
    """Create a tree-shaped mask with improved symmetry and coverage."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # Tree trunk (wider rectangle at bottom)
            trunk = (abs(x) <= center*0.15 and y <= -center*0.2)
            
            # Tree top (larger triangle with better proportions)
            top = (y >= -center*0.2 and abs(x) <= (y + center*0.2) * 0.7)
            
            # Tree branches (horizontal extensions)
            branches = (y >= -center*0.1 and y <= center*0.1 and abs(x) <= center*0.6)
            
            row.append(trunk or top or branches)
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
    """Create a car-shaped mask with improved symmetry and coverage."""
    mask = []
    center = size // 2
    
    for i in range(size):
        row = []
        for j in range(size):
            x = j - center
            y = center - i
            
            # Car body (larger rectangle with better proportions)
            body = (abs(x) <= center*0.7 and abs(y) <= center*0.25)
            
            # Car roof (smaller rectangle on top)
            roof = (abs(x) <= center*0.5 and y >= center*0.1 and y <= center*0.25)
            
            # Car wheels (larger and more visible)
            wheel1 = ((x-center*0.45)**2 + (y-center*0.18)**2) <= (center*0.12)**2
            wheel2 = ((x+center*0.45)**2 + (y-center*0.18)**2) <= (center*0.12)**2
            
            # Car front and back (rounded ends)
            front = (x >= center*0.6 and abs(y) <= center*0.2)
            back = (x <= -center*0.6 and abs(y) <= center*0.2)
            
            row.append(body or roof or wheel1 or wheel2 or front or back)
        mask.append(row)
    
    return mask

# Custom drawing functionality
import base64
from PIL import Image, ImageOps
import io
import numpy as np

# Storage for custom shapes
custom_shapes = {}

def flood_fill_shape(border_mask, size):
    """
    Use flood fill algorithm to fill the interior of a shape defined by borders.
    
    Args:
        border_mask: 2D boolean array where True indicates border pixels
        size: Size of the grid
    
    Returns:
        2D boolean array where True indicates filled area (border + interior)
    """
    # Create a working mask that includes borders
    filled_mask = border_mask.copy()
    
    # Find the center point as starting position for flood fill
    center = size // 2
    
    # If center is already part of border, find an alternative starting point
    start_points = [
        (center, center),
        (center + 1, center),
        (center - 1, center),
        (center, center + 1),
        (center, center - 1),
        (center + 1, center + 1),
        (center - 1, center - 1),
        (center + 1, center - 1),
        (center - 1, center + 1)
    ]
    
    # Find a good starting point (not on border)
    start_x, start_y = None, None
    for x, y in start_points:
        if 0 <= x < size and 0 <= y < size and not border_mask[x, y]:
            start_x, start_y = x, y
            break
    
    # If no good starting point found, try to find any non-border point
    if start_x is None:
        for i in range(size):
            for j in range(size):
                if not border_mask[i, j]:
                    start_x, start_y = i, j
                    break
            if start_x is not None:
                break
    
    # If still no starting point, return just the border
    if start_x is None:
        return border_mask
    
    # Perform flood fill
    stack = [(start_x, start_y)]
    visited = set()
    
    while stack:
        x, y = stack.pop()
        
        # Skip if out of bounds, already visited, or part of border
        if (x < 0 or x >= size or y < 0 or y >= size or 
            (x, y) in visited or border_mask[x, y]):
            continue
        
        # Mark as filled and visited
        filled_mask[x, y] = True
        visited.add((x, y))
        
        # Add neighbors to stack
        stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
    
    return filled_mask

def resize_mask(mask, target_size):
    """
    Resize a mask to the target size.
    
    Args:
        mask: 2D list of booleans
        target_size: Target size for the mask
    
    Returns:
        Resized 2D list of booleans
    """
    if not mask:
        return [[True for _ in range(target_size)] for _ in range(target_size)]
    
    current_size = len(mask)
    if current_size == target_size:
        return mask
    
    # Create new mask
    new_mask = [[False for _ in range(target_size)] for _ in range(target_size)]
    
    # Scale factor
    scale = current_size / target_size
    
    for i in range(target_size):
        for j in range(target_size):
            # Map to original coordinates
            orig_i = int(i * scale)
            orig_j = int(j * scale)
            
            # Ensure we don't go out of bounds
            orig_i = min(orig_i, current_size - 1)
            orig_j = min(orig_j, current_size - 1)
            
            new_mask[i][j] = mask[orig_i][orig_j]
    
    return new_mask

def process_canvas_to_mask(canvas_data, size=15):
    """
    Convert canvas drawing data to a boolean mask.
    Treats the drawn lines as a border and fills the interior area.
    
    Args:
        canvas_data: Base64 encoded image data from canvas
        size: Target grid size
    
    Returns:
        2D list of booleans indicating valid positions
    """
    try:
        # Remove data URL prefix if present
        if canvas_data.startswith('data:image'):
            canvas_data = canvas_data.split(',')[1]
        
        # Decode base64 image data
        image_data = base64.b64decode(canvas_data)
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to grayscale and resize to target size
        image = image.convert('L')
        image = image.resize((size, size), Image.Resampling.LANCZOS)
        
        # Convert to numpy array for processing
        img_array = np.array(image)
        
        # Create border mask based on non-white pixels (the drawn lines)
        # Threshold to handle anti-aliasing
        threshold = 240  # Pixels darker than this are considered "drawn"
        border_mask = img_array < threshold
        
        # If no border detected, return a simple filled square
        if not np.any(border_mask):
            center = size // 2
            return [[True for _ in range(size)] for _ in range(size)]
        
        # Use flood fill to fill the interior of the shape
        # Start from the center and flood fill outward
        filled_mask = flood_fill_shape(border_mask, size)
        
        # Convert to list of lists
        mask_list = filled_mask.tolist()
        
        return mask_list
        
    except Exception as e:
        print(f"Error processing canvas data: {e}")
        # Return a simple square mask as fallback
        return [[True for _ in range(size)] for _ in range(size)]

def add_custom_shape(name, mask):
    """
    Add a custom shape to the available shapes.
    
    Args:
        name: Name for the custom shape
        mask: Boolean mask for the shape
    """
    custom_shapes[name] = mask
    print(f"Added custom shape: {name}")

def get_custom_shape(name):
    """
    Get a custom shape mask by name.
    
    Args:
        name: Name of the custom shape
    
    Returns:
        Boolean mask or None if not found
    """
    return custom_shapes.get(name)

def list_custom_shapes():
    """
    Get list of available custom shapes.
    
    Returns:
        List of custom shape names
    """
    return list(custom_shapes.keys())

def delete_custom_shape(name):
    """
    Delete a custom shape by name.
    
    Args:
        name: Name of the custom shape to delete
    
    Returns:
        True if shape was deleted, False if not found
    """
    if name in custom_shapes:
        del custom_shapes[name]
        print(f"Deleted custom shape: {name}")
        return True
    return False

def clear_all_custom_shapes():
    """
    Clear all custom shapes.
    
    Returns:
        Number of shapes that were cleared
    """
    count = len(custom_shapes)
    custom_shapes.clear()
    print(f"Cleared {count} custom shapes")
    return count

def process_uploaded_image_to_mask(image_file, size=15):
    """
    Process an uploaded image file to create a shape mask.
    Treats dark areas as borders and fills the interior.
    
    Args:
        image_file: Uploaded file object
        size: Target grid size
    
    Returns:
        2D list of booleans indicating valid positions
    """
    try:
        # Open and process the image
        image = Image.open(image_file)
        
        # Convert to grayscale and resize
        image = image.convert('L')
        image = image.resize((size, size), Image.Resampling.LANCZOS)
        
        # Apply automatic thresholding to separate foreground from background
        image = ImageOps.autocontrast(image)
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Use adaptive thresholding - darker areas are borders
        threshold = np.mean(img_array) * 0.8
        border_mask = img_array < threshold
        
        # If no border detected, return a simple filled square
        if not np.any(border_mask):
            center = size // 2
            return [[True for _ in range(size)] for _ in range(size)]
        
        # Use flood fill to fill the interior of the shape
        filled_mask = flood_fill_shape(border_mask, size)
        
        # Convert to list of lists
        mask_list = filled_mask.tolist()
        
        return mask_list
        
    except Exception as e:
        print(f"Error processing uploaded image: {e}")
        # Return a simple square mask as fallback
        return [[True for _ in range(size)] for _ in range(size)]
