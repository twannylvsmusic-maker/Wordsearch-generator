from flask import Flask, render_template, request, send_file, jsonify
from utils.puzzle_generator import generate_puzzle
from utils.pdf_exporter import export_to_pdf
from utils.word_exporter import export_to_word
import os
import json

app = Flask(__name__)

# Use absolute path for uploads folder to avoid path issues
UPLOAD_FOLDER = os.path.abspath('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure uploads directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    print(f"Created uploads folder at: {app.config['UPLOAD_FOLDER']}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get form data
        title = request.form.get('title', 'Word Search Puzzle')
        subject = request.form.get('subject', '')
        words_text = request.form.get('words', '')
        shape = request.form.get('shape', 'square')
        font = request.form.get('font', 'Arial')
        theme = request.form.get('theme', 'modern')
        export_format = request.form.get('exportFormat', 'pdf')
        allow_vertical = request.form.get('allowVertical') == 'on'
        allow_horizontal = request.form.get('allowHorizontal') == 'on'
        allow_diagonal = request.form.get('allowDiagonal') == 'on'
        
        # Process words - keep original with spaces for display
        original_words = [word.strip().upper() for word in words_text.split('\n') if word.strip()]
        
        # Create versions without spaces for puzzle placement
        puzzle_words = [word.replace(' ', '') for word in original_words]
        
        if not puzzle_words:
            return jsonify({'error': 'No words provided'}), 400
        
        # Generate puzzle using words without spaces
        grid, placed_words_no_spaces = generate_puzzle(
            words=puzzle_words,
            shape=shape,
            allow_vertical=allow_vertical,
            allow_horizontal=allow_horizontal,
            allow_diagonal=allow_diagonal
        )
        
        # Map placed words back to original format with spaces
        # Create a mapping from no-space version to original
        word_mapping = {word.replace(' ', ''): word for word in original_words}
        placed_words_with_spaces = [word_mapping.get(word, word) for word in placed_words_no_spaces]
        
        # Create filename with full path
        safe_title = title.replace(' ', '_').replace('/', '_').replace('\\', '_')
        
        # Export based on format (use words with spaces for display)
        if export_format == 'word':
            filename = f"{safe_title}.docx"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"DEBUG: Saving Word file to: {filepath}")
            print(f"DEBUG: Upload folder exists: {os.path.exists(app.config['UPLOAD_FOLDER'])}")
            print(f"DEBUG: Full upload folder path: {os.path.abspath(app.config['UPLOAD_FOLDER'])}")
            export_to_word(title, subject, grid, placed_words_with_spaces, font, filepath, theme, shape)
        else:  # PDF
            filename = f"{safe_title}.pdf"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"DEBUG: Saving PDF file to: {filepath}")
            print(f"DEBUG: Upload folder exists: {os.path.exists(app.config['UPLOAD_FOLDER'])}")
            print(f"DEBUG: Full upload folder path: {os.path.abspath(app.config['UPLOAD_FOLDER'])}")
            export_to_pdf(title, subject, grid, placed_words_with_spaces, font, filepath, theme, shape)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview():
    try:
        # Get form data
        words_text = request.form.get('words', '')
        shape = request.form.get('shape', 'square')
        allow_vertical = request.form.get('allowVertical') == 'on'
        allow_horizontal = request.form.get('allowHorizontal') == 'on'
        allow_diagonal = request.form.get('allowDiagonal') == 'on'
        
        # Process words - keep original with spaces for display
        original_words = [word.strip().upper() for word in words_text.split('\n') if word.strip()]
        
        # Create versions without spaces for puzzle placement
        puzzle_words = [word.replace(' ', '') for word in original_words]
        
        if not puzzle_words:
            return jsonify({'error': 'No words provided'}), 400
        
        # Generate puzzle using words without spaces
        grid, placed_words_no_spaces = generate_puzzle(
            words=puzzle_words,
            shape=shape,
            allow_vertical=allow_vertical,
            allow_horizontal=allow_horizontal,
            allow_diagonal=allow_diagonal
        )
        
        # Map placed words back to original format with spaces
        word_mapping = {word.replace(' ', ''): word for word in original_words}
        placed_words_with_spaces = [word_mapping.get(word, word) for word in placed_words_no_spaces]
        
        return jsonify({
            'grid': grid,
            'words': placed_words_with_spaces,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
