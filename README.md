# Word Search Generator v2

A modern, feature-rich word search puzzle generator with customizable shapes, themes, and export options.

## Features

### ✅ All Requested Features Implemented:
- **Shape Selection Tabs**: Premade, Draw, Upload
- **Live Preview**: Real-time puzzle preview as you build
- **Font & Theme Customization**: Multiple fonts and themes (Modern, Cozy, Playful)
- **Animal Shapes**: Dog, Cat, Fish, and more
- **Export Options**: Both PDF and Word Document formats
- **Improved Layout**: Word list on left, instructions centered under puzzle
- **Better Formatting**: Proper margins, spacing, and capitalization

### 🎨 Enhanced UI:
- Modern, responsive design
- Dark/light theme toggle
- Font size adjustment
- Intuitive tabbed interface
- Real-time preview updates

### 🧩 Shape Options:
- **Basic Shapes**: Square, Circle, Diamond, Triangle, Hexagon
- **Fun Shapes**: Heart, Star, Butterfly, Flower
- **Animals**: Dog, Cat, Fish
- **Objects**: Tree, House, Car

### 📄 Export Features:
- **PDF Export**: Professional layout with proper margins
- **Word Export**: Editable .docx format
- **Customizable**: Fonts, themes, and formatting options

## Quick Start

1. **Double-click `start.bat`** to run the application
2. **Open your browser** to `http://127.0.0.1:5000`
3. **Add words** using the "Add Word" button
4. **Select a shape** from the dropdown
5. **Customize** fonts and themes
6. **Preview** your puzzle in real-time
7. **Export** as PDF or Word document

## File Structure

```
wordsearch_generator_v2/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── start.bat             # Windows startup script
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── styles.css        # CSS styles
│   └── script.js         # JavaScript functionality
└── utils/
    ├── __init__.py
    ├── puzzle_generator.py    # Puzzle generation logic
    ├── shape_masks.py         # Shape definitions
    ├── pdf_exporter.py        # PDF export functionality
    └── word_exporter.py       # Word document export
```

## Dependencies

- Flask 3.1.2
- ReportLab 4.4.4 (PDF generation)
- python-docx 1.1.0 (Word document generation)
- Pillow 11.3.0 (Image processing)

## Usage

### Adding Words
- Click "Add Word" to manually add words
- Use "Upload" to load words from a text file
- Words are automatically capitalized

### Shape Selection
- **Premade**: Choose from predefined shapes
- **Draw**: Draw your own custom shape (demo feature)
- **Upload**: Upload an image as a shape (demo feature)

### Customization
- **Fonts**: Choose from 7 different fonts
- **Themes**: Modern, Cozy, or Playful
- **Word Directions**: Enable/disable vertical, horizontal, diagonal placement

### Export Options
- **PDF**: Professional layout with proper margins (0.5" on all sides)
- **Word**: Editable document format for further customization

## Layout Improvements

✅ **Word list positioned on the left** (not below the puzzle)
✅ **Instructions centered under the puzzle**
✅ **Proper margins**: 0.5 inches on all sides
✅ **Word list header**: "Wordlist:" (not "Words to Find:")
✅ **Capitalized words** with preserved internal spaces
✅ **Increased spacing** between words in the list

## Technical Notes

- Built with Flask for the web framework
- Uses ReportLab for PDF generation
- Uses python-docx for Word document creation
- Responsive design works on desktop and mobile
- Real-time preview updates as you make changes

## Troubleshooting

If you encounter issues:

1. **Python not found**: Install Python 3.8 or later
2. **Dependencies fail**: Run `pip install -r requirements.txt` manually
3. **Port in use**: Change the port in `app.py` (line with `app.run()`)
4. **Browser cache**: Press Ctrl+F5 to hard refresh

## 🚀 Deployment & Portfolio

### Live Demo
- **Static Demo**: [GitHub Pages Demo](https://yourusername.github.io/wordsearch-generator)
- **Full App**: [Heroku Live Demo](https://wordsearch-generator-demo.herokuapp.com)

### Deploy to Heroku
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create Heroku app: `heroku create your-app-name`
3. Deploy: `git push heroku main`
4. Open: `heroku open`

### Deploy to GitHub Pages
1. Push to GitHub repository
2. Enable Pages in repository settings
3. Set source to main branch
4. Access at `https://yourusername.github.io/repository-name`

### Portfolio Integration
Add this project to your portfolio with:
- **Live Demo Link**: Showcase the working application
- **Source Code**: Link to GitHub repository
- **Technologies**: Flask, Python, JavaScript, HTML/CSS
- **Features**: Highlight key functionality and design choices

## Future Enhancements

- Custom shape drawing and uploading (currently demo)
- More shape categories
- Puzzle difficulty levels
- Save/load puzzle configurations
- Batch puzzle generation
