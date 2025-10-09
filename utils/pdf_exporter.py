from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
import os

# Custom page size for 6.5" x 9"
CUSTOM_PAGE_SIZE = (6.5*inch, 9*inch)

def export_to_pdf(title, subject, grid, word_list, font_name, filename, theme='modern', shape='square'):
    """
    Export puzzle to PDF with improved formatting for 6.5" x 9" page.
    
    Layout improvements:
    - Custom 6.5" x 9" page size
    - Title and subtitle centered on the puzzle grid
    - Word list on the left side with header aligned to puzzle grid
    - Increased word list column width for longer words
    - Centered content on page
    - Maintained color scheme: blue titles, light blue subtitles, black text
    """
    
    # Map non-standard fonts to PDF-compatible fonts
    font_mapping = {
        'Inter': 'Helvetica',
        'Inter (Modern)': 'Helvetica'
    }
    font_name = font_mapping.get(font_name, font_name)
    
    # Theme colors
    theme_colors = get_theme_colors(theme)
    
    # Normalize path to handle Windows paths with spaces
    normalized_path = os.path.abspath(filename)
    print(f"DEBUG pdf_exporter: Attempting to save to: {normalized_path}")
    print(f"DEBUG pdf_exporter: Directory exists: {os.path.exists(os.path.dirname(normalized_path))}")
    
    # Create PDF document with custom 6.5" x 9" page size and conditional margins
    if shape == 'square':
        # Square shape: 1.5" header, 0.5" left, 0.75" right, 1.5" footer margins (space for instructions)
        doc = SimpleDocTemplate(
            normalized_path,
            pagesize=CUSTOM_PAGE_SIZE,
            leftMargin=0.5*inch,   # 0.5" left margin
            rightMargin=0.75*inch,  # 0.75" right margin
            topMargin=1.5*inch,    # 1.5" top margin
            bottomMargin=1.5*inch  # 1.5" bottom margin (increased for footer instructions)
        )
    else:
        # Non-square shapes: equal left and right margins like Word version
        doc = SimpleDocTemplate(
            normalized_path,
            pagesize=CUSTOM_PAGE_SIZE,
            leftMargin=0.5*inch,   # Equal left margin
            rightMargin=0.5*inch,  # Equal right margin (matching left)
            topMargin=0.5*inch,    # Reduced top margin for more space
            bottomMargin=1.0*inch  # Increased bottom margin for footer instructions
        )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create puzzle table and word list
    puzzle_table = create_puzzle_table(grid, font_name, theme_colors, shape)
    word_list_table = create_word_list_table(word_list, font_name, theme_colors, shape, grid)
    
    # Create title and subject paragraphs for centering on page
    title_para = None
    subject_para = None
    
    if title:
        title_style = ParagraphStyle(
            'CustomTitle',
            fontSize=20,  # Match puzzle letters: 17pt → 20pt
            textColor=colors.black,  # Black color
            fontName=font_name,
            alignment=TA_CENTER,
            spaceAfter=6
        )
        title_para = Paragraph(f"<b>{title}</b>", title_style)
    
    if subject:
        # Conditional spacing based on shape type
        if shape == 'square':
            space_before = 0  # No extra spacing for square shapes
        else:
            space_before = 12  # Additional spacing above subject/topic for non-square shapes
            
        subject_style = ParagraphStyle(
            'CustomSubject',
            fontSize=16,  # Set to 16pt as requested
            textColor=colors.black,  # Black color
            fontName=font_name,
            alignment=TA_CENTER,
            spaceAfter=8,
            spaceBefore=space_before  # Conditional spacing above subject/topic
        )
        subject_para = Paragraph(subject, subject_style)
    
    # Create centered puzzle table (no titles - they're on the page)
    if shape == 'square':
        # For square shapes: calculate width based on optimized cell size
        grid_size = len(grid)
        available_width = 5.25*inch  # 6.5" - 1.25" margins
        min_wordlist_width = 2.0*inch  # Reduced minimum wordlist width to maximize puzzle
        max_puzzle_width = available_width - min_wordlist_width  # 3.25" max puzzle width
        cell_size = max_puzzle_width / grid_size  # Dynamic cell size
        puzzle_width = grid_size * cell_size  # Calculate actual puzzle width
    else:
        # Non-square shapes: calculate width to fit properly with word list (equal margins)
        available_width = 5.5*inch  # 6.5" - 1.0" margins (0.5" left + 0.5" right)
        wordlist_width = 1.8*inch   # Further reduced word list width for 2X larger puzzle cells
        puzzle_width = available_width - wordlist_width - 0.2*inch  # 3.5" for puzzle with gap
    
    centered_puzzle_table = Table([[puzzle_table]], colWidths=[puzzle_width])
    centered_puzzle_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),  # Remove top padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0), # Remove bottom padding
        ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Remove left padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 0), # Remove right padding
    ]))
    
    # Combine word list and puzzle with conditional column widths
    if shape == 'square':
        # Square shape: calculate wordlist width to center content
        available_width = 5.25*inch  # 6.5" - 1.25" margins
        wordlist_width = available_width - puzzle_width
        main_table = Table([
            [word_list_table, centered_puzzle_table]
        ], colWidths=[wordlist_width, puzzle_width])
    else:
        # Non-square shapes: optimized sizing to prevent overlap (equal margins)
        available_width = 5.5*inch  # 6.5" - 1.0" margins (0.5" left + 0.5" right)
        wordlist_width = 1.8*inch   # Further reduced word list width for 2X larger puzzle cells
        puzzle_width = available_width - wordlist_width - 0.2*inch  # 3.5" for puzzle with gap
        main_table = Table([
            [word_list_table, centered_puzzle_table]
        ], colWidths=[wordlist_width, puzzle_width])
    
    # Style the main table - better alignment for grid container
    main_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),   # Left align the entire table
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Word list left-aligned within its column
        ('ALIGN', (1, 0), (1, 0), 'CENTER'), # Puzzle centered within its column
        ('BACKGROUND', (0, 0), (-1, -1), theme_colors['background']),  # Ensure white background
        ('TOPPADDING', (0, 0), (-1, -1), 0),  # Remove top padding from main table
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0), # Remove bottom padding from main table
    ]))
    
    # Build content
    story = []
    
    # Add space at the top to push content down (optimized for page fit)
    if shape == 'square':
        story.append(Spacer(1, 20))
    else:
        story.append(Spacer(1, 10))  # Less space for non-square shapes
    
    # Add title and subject to page (centered)
    if title_para:
        story.append(title_para)
    if subject_para:
        story.append(subject_para)
    
    # Add space between title and main content (optimized for page fit)
    if shape == 'square':
        story.append(Spacer(1, 40))
    else:
        story.append(Spacer(1, 20))  # Less space for non-square shapes
    
    # Add the main table (word list + puzzle)
    story.append(main_table)
    
    # Add space after the main content (optimized for page fit)
    if shape == 'square':
        story.append(Spacer(1, 20))
    else:
        story.append(Spacer(1, 10))  # Less space for non-square shapes
    
    # Instructions formatted to match Word document
    if shape != 'square':
        # For non-square shapes: instructions will be added to footer via canvas
        pass  # Instructions added via footer canvas function
    
    # Build PDF with white background and footer
    def add_background_and_footer(canvas, doc):
        canvas.setFillColor(colors.white)
        canvas.rect(0, 0, CUSTOM_PAGE_SIZE[0], CUSTOM_PAGE_SIZE[1], fill=1, stroke=0)
        
        # Add footer instructions for both shapes
        if shape == 'square':
            add_instructions_to_pdf_footer(canvas, doc, font_name, theme_colors)
        else:
            # Add footer instructions for non-square shapes
            add_instructions_to_pdf_footer_for_non_square(canvas, doc, font_name, theme_colors)
    
    doc.build(story, onFirstPage=add_background_and_footer, onLaterPages=add_background_and_footer)

def add_instructions_to_pdf_footer(canvas, doc, font_name, theme_colors):
    """Add instructions to the actual PDF footer using canvas drawing."""
    
    # Set font and color
    canvas.setFont(font_name, 11)  # Keep instructions at 11pt
    canvas.setFillColor(colors.black)  # Black color
    
    # Calculate footer position (bottom margin is 1.5", so start at 1.7" from bottom)
    footer_y = 1.7 * inch
    left_margin = 0.5 * inch
    
    # Instructions title
    canvas.drawString(left_margin, footer_y, "Instructions:")
    
    # Instruction lines (left-aligned, no spacing between sentences)
    instructions = [
        "Find all the words hidden in the puzzle above.",
        "Circle or highlight each word as you find it.",
        "Words can be read horizontally, vertically, or diagonally."
    ]
    
    # Draw each instruction line
    line_height = 12  # 12 points between lines
    for i, instruction in enumerate(instructions):
        y_position = footer_y - (i + 1) * line_height
        canvas.drawString(left_margin, y_position, instruction)

def add_instructions_to_pdf_footer_for_non_square(canvas, doc, font_name, theme_colors):
    """Add instructions to the actual PDF footer for non-square shapes with paragraph-like formatting."""
    
    # Calculate footer position (bottom margin is 1.0", so start at 1.2" from bottom)
    footer_y = 1.2 * inch
    left_margin = 0.5 * inch
    right_margin = 0.5 * inch
    available_width = 6.5 * inch - left_margin - right_margin  # Available width for text
    
    # Set font and color for "Instructions:" (bold)
    canvas.setFont(font_name + "-Bold", 11)  # Bold font for "Instructions:"
    canvas.setFillColor(colors.black)  # Black color
    
    # Draw "Instructions:" in bold
    canvas.drawString(left_margin, footer_y, "Instructions:")
    
    # Calculate width of "Instructions:" to position the rest of the text
    instructions_label_width = canvas.stringWidth("Instructions:", font_name + "-Bold", 11)
    
    # Set font for the rest of the text (regular)
    canvas.setFont(font_name, 11)  # Regular font for instruction text
    
    # Instruction text with proper wrapping
    instruction_text = "Find all the words hidden in the puzzle above, circle or highlight each word as you find it. Note: Words may be read horizontally, vertically, or diagonally."
    
    # Split text into lines that fit within margins
    words = instruction_text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        # Check if "Note:" should be bold
        if word == "Note:":
            test_line = current_line + (" " if current_line else "") + word
            test_width = canvas.stringWidth(current_line + (" " if current_line else ""), font_name, 11)
            test_width += canvas.stringWidth("Note:", font_name + "-Bold", 11)
            if test_width > available_width - instructions_label_width - 10:
                if current_line:
                    lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        else:
            test_width = canvas.stringWidth(test_line, font_name, 11)
            if test_width > available_width - instructions_label_width - 10:
                if current_line:
                    lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
    
    if current_line:
        lines.append(current_line)
    
    # Draw the instruction lines with proper bold formatting for "Note:"
    for i, line in enumerate(lines):
        y_position = footer_y - (i + 1) * 13  # 13pt line spacing
        x_position = left_margin
        
        # Check if line contains "Note:" and handle bold formatting
        if "Note:" in line:
            parts = line.split("Note:")
            # Draw text before "Note:"
            if parts[0]:
                canvas.setFont(font_name, 11)  # Regular font
                canvas.drawString(x_position, y_position, parts[0])
                x_position += canvas.stringWidth(parts[0], font_name, 11)
            
            # Draw "Note:" in bold
            canvas.setFont(font_name + "-Bold", 11)  # Bold font
            canvas.drawString(x_position, y_position, "Note:")
            x_position += canvas.stringWidth("Note:", font_name + "-Bold", 11)
            
            # Draw text after "Note:"
            if len(parts) > 1 and parts[1]:
                canvas.setFont(font_name, 11)  # Regular font
                canvas.drawString(x_position, y_position, parts[1])
        else:
            # Regular line without "Note:"
            canvas.setFont(font_name, 11)  # Regular font
            canvas.drawString(x_position, y_position, line)


def add_instructions_to_pdf_footer_for_custom_shapes(story, font_name, theme_colors):
    """Add instructions to footer for custom shapes in a single line."""
    
    # Single line instructions (matching Word format)
    instruction_text = "Instructions: Find all the words hidden in the puzzle above. Circle or highlight each word as you find it. Words can be read horizontally, vertically, or diagonally."
    
    instruction_style = ParagraphStyle(
        'InstructionsLine',
        fontSize=11,  # 11pt for PDF to match Word appearance
        textColor=colors.black,
        fontName=font_name,
        alignment=TA_LEFT,
        spaceAfter=0
    )
    instruction_para = Paragraph(instruction_text, instruction_style)
    
    # Add instructions to story
    story.append(instruction_para)

def add_constrained_instructions_pdf(story, font_name, theme_colors, max_width):
    """Add instructions constrained to a specific width (left-aligned, matching image format)."""
    
    # Instructions title
    title_style = ParagraphStyle(
        'InstructionsTitle',
        fontSize=11,  # Keep instructions at 11pt
        textColor=colors.black,  # Black color
        fontName=font_name,
        alignment=TA_LEFT,
        spaceAfter=0
    )
    title_para = Paragraph("<b>Instructions:</b>", title_style)
    
    # Instruction lines (left-aligned, matching image format)
    instructions = [
        "Find all the words hidden in the puzzle above.",
        "Circle or highlight each word as you find it.",
        "Words can be read horizontally, vertically, or diagonally."
    ]
    
    instruction_paras = [title_para]
    for instruction in instructions:
        instruction_style = ParagraphStyle(
            'InstructionLine',
            fontSize=11,  # Keep instructions at 11pt
            textColor=colors.black,  # Black color
            fontName=font_name,
            alignment=TA_LEFT,
            spaceAfter=0
        )
        instruction_para = Paragraph(instruction, instruction_style)
        instruction_paras.append(instruction_para)
    
    # Create a table to constrain width
    instructions_table = Table([instruction_paras], colWidths=[max_width])
    instructions_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), theme_colors['background']),
    ]))
    
    story.append(instructions_table)

def create_puzzle_table_with_title(grid, title, subject, font_name, theme_colors):
    """Create a table containing title, subject, and puzzle grid."""
    
    # Create title and subject paragraphs
    title_style = ParagraphStyle(
        'CustomTitle',
        fontSize=18,
        textColor=theme_colors['primary'],
        fontName=font_name,
        alignment=TA_CENTER,
        spaceAfter=12  # Increased space after title
    )
    
    subject_style = ParagraphStyle(
        'CustomSubject',
        fontSize=14,
        textColor=theme_colors['secondary'],
        fontName=font_name,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    # Create puzzle table
    puzzle_table = create_puzzle_table(grid, font_name, theme_colors)
    
    # Create combined table data
    table_data = []
    
    # Add title if provided
    if title:
        table_data.append([Paragraph(title, title_style)])
    
    # Add subject if provided
    if subject:
        table_data.append([Paragraph(subject, subject_style)])
    
    # Add puzzle table
    table_data.append([puzzle_table])
    
    # Create the combined table
    combined_table = Table(table_data, colWidths=[3.75*inch])
    
    # Style the combined table
    combined_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    return combined_table

def create_puzzle_table(grid, font_name, theme_colors, shape='square'):
    """Create the puzzle grid as a table."""
    
    # Create table data
    table_data = []
    for row in grid:
        table_data.append([cell for cell in row])
    
    # Create table with optimized cell sizes to maximize puzzle without overlapping wordlist
    grid_size = len(table_data)
    available_width = 5.25*inch  # 6.5" - 1.25" margins
    min_wordlist_width = 2.0*inch  # Reduced minimum wordlist width to maximize puzzle
    max_puzzle_width = available_width - min_wordlist_width  # 3.25" max puzzle width
    
    if grid_size <= 12:  # 8x8 to 12x12 grids (square shapes)
        # Calculate optimal cell size to fit within max puzzle width
        cell_size = max_puzzle_width / grid_size  # Dynamic sizing based on available space
        puzzle_font_size = 20  # Original font size for square shapes (unchanged)
        cell_padding = 2  # Original padding for square shapes (unchanged)
    else:  # Larger grids (15x15 custom shapes)
        # Use the same successful approach as square shapes but for 15x15 grids
        available_width = 5.5*inch  # 6.5" - 1.0" margins (0.5" left + 0.5" right)
        wordlist_width = 1.8*inch   # Reduced word list width
        max_puzzle_width = available_width - wordlist_width - 0.2*inch  # 3.5" for puzzle with gap
        cell_size = max_puzzle_width / grid_size  # Same calculation method as square shapes
        puzzle_font_size = 17  # Reduced by 1pt for non-square shapes (18pt → 17pt)
        cell_padding = 2  # Use the same successful padding as square shapes
    
    table = Table(table_data, colWidths=cell_size, rowHeights=cell_size)
    
    # Style the table using the same successful approach as square shapes
    table_style = [
        ('FONTNAME', (0, 0), (-1, -1), font_name),  # Back to original font
        ('FONTSIZE', (0, 0), (-1, -1), puzzle_font_size),  # Conditional font size
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # Black color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center letters horizontally
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Use same alignment as square shapes
        ('GRID', (0, 0), (-1, -1), 0.5, theme_colors['grid']),
        ('BACKGROUND', (0, 0), (-1, -1), theme_colors['background']),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),  # Use same padding as square shapes
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 0),   # Use same padding as square shapes
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15), # Increased bottom padding to push letters up for better centering
    ]
    
    table.setStyle(TableStyle(table_style))
    
    return table

def create_word_list_table(word_list, font_name, theme_colors, shape='square', grid=None):
    """Create the word list table for left side positioning."""
    
    # Add minimal padding to align with puzzle grid top
    padding_style = ParagraphStyle(
        'Padding',
        fontSize=1,
        textColor=theme_colors['background'],
        spaceAfter=2
    )
    padding = Paragraph("&nbsp;", padding_style)  # Invisible spacer
    
    # Header - conditional font size
    if shape == 'square':
        header_font_size = 20  # Original font size for square shapes
    else:
        header_font_size = 16  # Adjusted font size for non-square shapes
    
    header_style = ParagraphStyle(
        'WordListHeader',
        fontSize=header_font_size,  # Conditional header font size
        textColor=colors.black,  # Black color
        fontName=font_name,
        spaceAfter=30  # Significantly increased spacing below "Wordlist" header
    )
    
    header = Paragraph("<b>Wordlist:</b>", header_style)
    
    # Create word list data with padding
    word_list_data = [[padding], [header]]
    
    # Add multiple spacer rows for extra spacing below "Wordlist:" header
    for i in range(1):  # Add 1 spacer row for 50% less spacing
        spacer_style = ParagraphStyle(
            'Spacer',
            fontSize=1,
            textColor=colors.white,
            spaceAfter=0,
            spaceBefore=0
        )
        spacer = Paragraph("&nbsp;", spacer_style)
        word_list_data.append([spacer])
    
    # Add words with proper spacing
    for word in word_list:
        # Capitalize and preserve spaces within words
        formatted_word = word.upper()
        
        # Conditional font size for words
        if shape == 'square':
            word_font_size = 16  # Original font size for square shapes
        else:
            word_font_size = 14  # Adjusted font size for non-square shapes
        
        word_style = ParagraphStyle(
            'WordItem',
            fontSize=word_font_size,  # Conditional word font size
            textColor=colors.black,  # Black color
            fontName=font_name,
            alignment=TA_LEFT,  # Left align under "Wordlist:" title
            spaceAfter=6  # Increased spacing between words
        )
        word_para = Paragraph(formatted_word, word_style)  # Remove bullet point
        word_list_data.append([word_para])
    
    # Create table with conditional column width
    if shape == 'square' and grid:
        # For square shapes: use dynamic width based on available space
        available_width = 5.25*inch  # 6.5" - 1.25" margins
        grid_size = len(grid)
        min_wordlist_width = 2.0*inch  # Reduced minimum wordlist width to maximize puzzle
        max_puzzle_width = available_width - min_wordlist_width  # 3.25" max puzzle width
        cell_size = max_puzzle_width / grid_size  # Dynamic cell size
        puzzle_width = grid_size * cell_size  # Calculate actual puzzle width
        wordlist_width = available_width - puzzle_width  # Remaining space for wordlist
        table = Table(word_list_data, colWidths=[wordlist_width])
    else:
        # Non-square shapes: optimized width to prevent overlap
        wordlist_width = 1.8*inch  # Further reduced width to accommodate 2X larger puzzle cells
        table = Table(word_list_data, colWidths=[wordlist_width])
    
    # Style the table
    table_style = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BACKGROUND', (0, 0), (-1, -1), theme_colors['background']),  # Ensure white background
    ]
    
    table.setStyle(TableStyle(table_style))
    
    return table

def get_theme_colors(theme):
    """Get color scheme for the specified theme."""
    
    if theme == 'modern':
        return {
            'primary': colors.darkblue,        # Blue titles
            'secondary': colors.blue,          # Light blue subtitles
            'text': colors.black,              # Black text for puzzle and word list
            'background': colors.white,        # White background
            'grid': colors.lightgrey           # Light grey grid lines
        }
    elif theme == 'cozy':
        return {
            'primary': colors.darkgreen,
            'secondary': colors.green,
            'text': colors.black,
            'background': colors.beige,
            'grid': colors.lightgrey
        }
    elif theme == 'playful':
        return {
            'primary': colors.purple,
            'secondary': colors.orange,
            'text': colors.black,
            'background': colors.lightblue,
            'grid': colors.lightgrey
        }
    else:
        # Default to modern with black text on white background
        return {
            'primary': colors.darkblue,        # Blue titles
            'secondary': colors.blue,          # Light blue subtitles
            'text': colors.black,              # Black text for puzzle and word list
            'background': colors.white,        # White background
            'grid': colors.lightgrey           # Light grey grid lines
        }
