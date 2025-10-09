// Global variables
let words = [];
let currentShape = 'square';
let isDrawing = false;
let drawingData = [];

// DOM elements
const wordList = document.getElementById('wordList');
const wordCount = document.getElementById('wordCount');
const addWordBtn = document.getElementById('addWordBtn');
const pasteWordsBtn = document.getElementById('pasteWordsBtn');
const uploadBtn = document.getElementById('uploadBtn');
const randomizeBtn = document.getElementById('randomizeBtn');
const wordModal = document.getElementById('wordModal');
const newWordInput = document.getElementById('newWord');
const addWordModalBtn = document.getElementById('addWord');
const cancelWordBtn = document.getElementById('cancelWord');
const closeModal = document.querySelector('.close');
const pasteModal = document.getElementById('pasteModal');
const pasteWordsTextarea = document.getElementById('pasteWords');
const pasteCount = document.getElementById('pasteCount');
const pastePreview = document.getElementById('pastePreview');
const addPastedWordsBtn = document.getElementById('addPastedWords');
const cancelPasteBtn = document.getElementById('cancelPaste');
const shapeSelect = document.getElementById('shapeSelect');
const shapePreview = document.getElementById('shapePreview');
const puzzlePreview = document.getElementById('puzzlePreview');
const wordsToFind = document.getElementById('wordsToFind');
const generatePuzzleBtn = document.getElementById('generatePuzzle');
const refreshPreviewBtn = document.getElementById('refreshPreview');
const exportFormat = document.getElementById('exportFormat');

// Tab elements
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// Drawing elements
const drawCanvas = document.getElementById('drawCanvas');
const clearCanvasBtn = document.getElementById('clearCanvas');
const saveDrawingBtn = document.getElementById('saveDrawing');
const brushSize = document.getElementById('brushSize');
const brushSizeValue = document.getElementById('brushSizeValue');
const brushColor = document.getElementById('brushColor');
const ctx = drawCanvas.getContext('2d');

// Upload elements
const shapeUpload = document.getElementById('shapeUpload');
const uploadShapeBtn = document.getElementById('uploadShapeBtn');

// Manage custom shapes elements
const refreshCustomShapesBtn = document.getElementById('refreshCustomShapes');
const customShapesList = document.getElementById('customShapesList');
const clearAllCustomShapesBtn = document.getElementById('clearAllCustomShapes');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    setupDrawingCanvas();
    updateWordCount();
    updateShapePreview();
    // Start with empty word list - user can add their own words
}

function setupEventListeners() {
    // Word management
    addWordBtn.addEventListener('click', openWordModal);
    pasteWordsBtn.addEventListener('click', openPasteModal);
    uploadBtn.addEventListener('click', openFileUpload);
    randomizeBtn.addEventListener('click', randomizeWords);
    addWordModalBtn.addEventListener('click', addWord);
    cancelWordBtn.addEventListener('click', closeWordModal);
    addPastedWordsBtn.addEventListener('click', addPastedWords);
    cancelPasteBtn.addEventListener('click', closePasteModal);
    closeModal.addEventListener('click', closeWordModal);
    
    // Modal keyboard events
    newWordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addWord();
        }
    });
    
    // Shape selection
    shapeSelect.addEventListener('change', updateShapePreview);
    
    // Tab switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });
    
    // Drawing events
    clearCanvasBtn.addEventListener('click', clearCanvas);
    saveDrawingBtn.addEventListener('click', saveDrawing);
    
    // Brush controls
    brushSize.addEventListener('input', updateBrushSize);
    brushColor.addEventListener('change', updateBrushColor);
    
    // Upload events
    uploadShapeBtn.addEventListener('click', () => shapeUpload.click());
    shapeUpload.addEventListener('change', handleShapeUpload);
    
    // Manage custom shapes events
    refreshCustomShapesBtn.addEventListener('click', loadCustomShapes);
    clearAllCustomShapesBtn.addEventListener('click', clearAllCustomShapes);
    
    // Preview and generation
    refreshPreviewBtn.addEventListener('click', generatePreview);
    generatePuzzleBtn.addEventListener('click', generatePuzzle);
    
    // Form inputs
    document.getElementById('title').addEventListener('input', generatePreview);
    document.getElementById('subject').addEventListener('input', generatePreview);
    document.getElementById('fontSelect').addEventListener('change', generatePreview);
    document.getElementById('themeSelect').addEventListener('change', generatePreview);
    document.getElementById('allowVertical').addEventListener('change', generatePreview);
    document.getElementById('allowHorizontal').addEventListener('change', generatePreview);
    document.getElementById('allowDiagonal').addEventListener('change', generatePreview);
    
    // Paste words textarea events
    pasteWordsTextarea.addEventListener('input', updatePastePreview);
    pasteWordsTextarea.addEventListener('paste', function(e) {
        // Small delay to let paste complete before processing
        setTimeout(updatePastePreview, 10);
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === wordModal) {
            closeWordModal();
        }
        if (e.target === pasteModal) {
            closePasteModal();
        }
    });
}

function setupDrawingCanvas() {
    // Set up canvas drawing
    ctx.strokeStyle = brushColor.value;
    ctx.lineWidth = parseInt(brushSize.value);
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    
    // Fill canvas with white background
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, drawCanvas.width, drawCanvas.height);
    
    drawCanvas.addEventListener('mousedown', startDrawing);
    drawCanvas.addEventListener('mousemove', draw);
    drawCanvas.addEventListener('mouseup', stopDrawing);
    drawCanvas.addEventListener('mouseout', stopDrawing);
    
    // Touch events for mobile
    drawCanvas.addEventListener('touchstart', handleTouch);
    drawCanvas.addEventListener('touchmove', handleTouch);
    drawCanvas.addEventListener('touchend', stopDrawing);
    
    // Load custom shapes on initialization
    updateShapeSelector();
}

function updateBrushSize() {
    ctx.lineWidth = parseInt(brushSize.value);
    brushSizeValue.textContent = brushSize.value;
}

function updateBrushColor() {
    ctx.strokeStyle = brushColor.value;
}

function startDrawing(e) {
    isDrawing = true;
    const rect = drawCanvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    ctx.beginPath();
    ctx.moveTo(x, y);
}

function draw(e) {
    if (!isDrawing) return;
    
    const rect = drawCanvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    ctx.lineTo(x, y);
    ctx.stroke();
}

function stopDrawing() {
    if (isDrawing) {
        isDrawing = false;
        ctx.beginPath();
    }
}

function handleTouch(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const mouseEvent = new MouseEvent(e.type === 'touchstart' ? 'mousedown' : 
                                     e.type === 'touchmove' ? 'mousemove' : 'mouseup', {
        clientX: touch.clientX,
        clientY: touch.clientY
    });
    drawCanvas.dispatchEvent(mouseEvent);
}

function clearCanvas() {
    ctx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
    // Fill with white background
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, drawCanvas.width, drawCanvas.height);
}

async function saveDrawing() {
    // Check if there's anything drawn on the canvas
    const imageData = drawCanvas.toDataURL();
    const blankCanvas = document.createElement('canvas');
    blankCanvas.width = drawCanvas.width;
    blankCanvas.height = drawCanvas.height;
    const blankData = blankCanvas.toDataURL();
    
    if (imageData === blankData) {
        showToast('Please draw something first!', 'warning');
        return;
    }
    
    try {
        // Get shape name from user
        const shapeName = prompt('Enter a name for your custom shape:', 'my_drawing');
        if (!shapeName || shapeName.trim() === '') {
            showToast('Shape name is required', 'warning');
            return;
        }
        
        // Show loading state
        saveDrawingBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
        saveDrawingBtn.disabled = true;
        
        // Send drawing to server
        const response = await fetch('/save_drawing', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                canvas_data: imageData,
                shape_name: shapeName.trim()
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message, 'success');
            
            // Update the shape selector to include the new custom shape
            updateShapeSelector();
            
            // Switch to premade tab and select the new shape
            switchTab('premade');
            shapeSelect.value = shapeName.trim();
            updateShapePreview();
            
            // Clear the canvas
            clearCanvas();
        } else {
            throw new Error(data.error || 'Failed to save drawing');
        }
        
    } catch (error) {
        console.error('Save drawing error:', error);
        showToast('Error saving drawing: ' + error.message, 'error');
    } finally {
        // Reset button state
        saveDrawingBtn.innerHTML = '<i class="fas fa-save"></i> Save Shape';
        saveDrawingBtn.disabled = false;
    }
}

async function handleShapeUpload(e) {
    const file = e.target.files[0];
    if (file) {
        try {
            // Get shape name from user
            const shapeName = prompt('Enter a name for your custom shape:', 'uploaded_shape');
            if (!shapeName || shapeName.trim() === '') {
                showToast('Shape name is required', 'warning');
                return;
            }
            
            // Show loading state
            uploadShapeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
            uploadShapeBtn.disabled = true;
            
            // Create form data
            const formData = new FormData();
            formData.append('shape_file', file);
            formData.append('shape_name', shapeName.trim());
            
            // Send to server
            const response = await fetch('/upload_shape', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                showToast(data.message, 'success');
                
                // Update the shape selector to include the new custom shape
                updateShapeSelector();
                
                // Switch to premade tab and select the new shape
                switchTab('premade');
                shapeSelect.value = shapeName.trim();
                updateShapePreview();
                
            } else {
                throw new Error(data.error || 'Failed to upload shape');
            }
            
        } catch (error) {
            console.error('Upload shape error:', error);
            showToast('Error uploading shape: ' + error.message, 'error');
        } finally {
            // Reset button state
            uploadShapeBtn.innerHTML = 'Choose File';
            uploadShapeBtn.disabled = false;
            
            // Clear the file input
            shapeUpload.value = '';
        }
    }
}

function switchTab(tabName) {
    // Update tab buttons
    tabBtns.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });
    
    // Update tab content
    tabContents.forEach(content => {
        content.classList.remove('active');
        if (content.id === tabName + 'Tab') {
            content.classList.add('active');
        }
    });
    
    // Load custom shapes when manage tab is opened
    if (tabName === 'manage') {
        loadCustomShapes();
    }
}

function openWordModal() {
    wordModal.style.display = 'block';
    newWordInput.focus();
    newWordInput.value = '';
}

function closeWordModal() {
    wordModal.style.display = 'none';
    newWordInput.value = '';
}

function openPasteModal() {
    pasteModal.style.display = 'block';
    pasteWordsTextarea.focus();
    pasteWordsTextarea.value = '';
    updatePastePreview();
}

function closePasteModal() {
    pasteModal.style.display = 'none';
    pasteWordsTextarea.value = '';
    updatePastePreview();
}

function addWord() {
    const word = newWordInput.value.trim().toUpperCase();
    
    if (word && !words.includes(word)) {
        words.push(word);
        updateWordList();
        updateWordCount();
        generatePreview();
        closeWordModal();
        showToast(`"${word}" added to word list`, 'success');
    } else if (words.includes(word)) {
        showToast('Word already exists in the list', 'warning');
    } else {
        showToast('Please enter a valid word', 'error');
    }
}

function removeWord(wordToRemove) {
    words = words.filter(word => word !== wordToRemove);
    updateWordList();
    updateWordCount();
    generatePreview();
    showToast(`"${wordToRemove}" removed from word list`, 'success');
}

function updateWordList() {
    if (words.length === 0) {
        wordList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-list-ul"></i>
                <p>No words added yet</p>
            </div>
        `;
        return;
    }
    
    wordList.innerHTML = words.map(word => `
        <div class="word-item fade-in">
            <span class="word-text">${word}</span>
            <button class="remove-word" onclick="removeWord('${word}')" title="Remove word">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `).join('');
}

function updateWordCount() {
    const count = words.length;
    wordCount.textContent = `${count} word${count !== 1 ? 's' : ''}`;
}

async function updateShapeSelector() {
    try {
        const response = await fetch('/custom_shapes');
        const data = await response.json();
        
        if (data.success) {
            // Remove existing custom shapes from selector
            const customOptGroups = shapeSelect.querySelectorAll('optgroup[label="Custom Shapes"]');
            customOptGroups.forEach(group => group.remove());
            
            // Add custom shapes if any exist
            if (data.shapes.length > 0) {
                const customGroup = document.createElement('optgroup');
                customGroup.label = 'Custom Shapes';
                
                data.shapes.forEach(shapeName => {
                    const option = document.createElement('option');
                    option.value = shapeName;
                    option.textContent = shapeName;
                    customGroup.appendChild(option);
                });
                
                shapeSelect.appendChild(customGroup);
            }
        }
    } catch (error) {
        console.error('Error loading custom shapes:', error);
    }
}

function updateShapePreview() {
    currentShape = shapeSelect.value;
    
    // Check if it's a custom shape
    if (currentShape && !isBuiltInShape(currentShape)) {
        // For custom shapes, show a generic custom icon
        shapePreview.innerHTML = `<i class="fas fa-paint-brush"></i>`;
    } else {
        // Update preview icon based on built-in shape
        const shapeIcons = {
            'square': 'fas fa-square',
            'circle': 'fas fa-circle',
            'diamond': 'fas fa-gem',
            'triangle': 'fas fa-play',
            'hexagon': 'fas fa-hexagon',
            'heart': 'fas fa-heart',
            'star': 'fas fa-star',
            'butterfly': 'fas fa-bug',
            'flower': 'fas fa-seedling',
            'dog': 'fas fa-dog',
            'cat': 'fas fa-cat',
            'fish': 'fas fa-fish',
            'tree': 'fas fa-tree',
            'house': 'fas fa-home',
            'car': 'fas fa-car'
        };
        
        const iconClass = shapeIcons[currentShape] || 'fas fa-square';
        shapePreview.innerHTML = `<i class="${iconClass}"></i>`;
    }
    
    generatePreview();
}

function isBuiltInShape(shapeName) {
    const builtInShapes = [
        'square', 'circle', 'diamond', 'triangle', 'hexagon',
        'heart', 'star', 'butterfly', 'flower', 'dog', 'cat',
        'fish', 'tree', 'house', 'car'
    ];
    return builtInShapes.includes(shapeName);
}

async function loadCustomShapes() {
    try {
        customShapesList.innerHTML = `
            <div class="loading-shapes">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Loading custom shapes...</p>
            </div>
        `;
        
        const response = await fetch('/custom_shapes');
        const data = await response.json();
        
        if (data.success) {
            displayCustomShapes(data.shapes);
        } else {
            throw new Error(data.error || 'Failed to load custom shapes');
        }
        
    } catch (error) {
        console.error('Error loading custom shapes:', error);
        customShapesList.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Error loading custom shapes: ${error.message}</p>
            </div>
        `;
    }
}

function displayCustomShapes(shapes) {
    if (shapes.length === 0) {
        customShapesList.innerHTML = `
            <div class="no-shapes">
                <i class="fas fa-puzzle-piece"></i>
                <p>No custom shapes created yet</p>
                <small>Draw or upload shapes to see them here</small>
            </div>
        `;
        clearAllCustomShapesBtn.disabled = true;
        return;
    }
    
    customShapesList.innerHTML = shapes.map(shapeName => `
        <div class="shape-item">
            <div class="shape-info">
                <i class="fas fa-paint-brush"></i>
                <span class="shape-name">${shapeName}</span>
            </div>
            <div class="shape-actions">
                <button type="button" class="btn-use-shape" onclick="useCustomShape('${shapeName}')" title="Use this shape">
                    <i class="fas fa-check"></i>
                </button>
                <button type="button" class="btn-delete-shape" onclick="deleteCustomShape('${shapeName}')" title="Delete this shape">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    clearAllCustomShapesBtn.disabled = false;
}

async function deleteCustomShape(shapeName) {
    if (!confirm(`Are you sure you want to delete the custom shape "${shapeName}"?`)) {
        return;
    }
    
    try {
        const response = await fetch('/delete_custom_shape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                shape_name: shapeName
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message, 'success');
            
            // Reload the custom shapes list
            loadCustomShapes();
            
            // Update the shape selector
            updateShapeSelector();
            
            // If the deleted shape was currently selected, switch to square
            if (currentShape === shapeName) {
                shapeSelect.value = 'square';
                updateShapePreview();
            }
            
        } else {
            throw new Error(data.message || 'Failed to delete shape');
        }
        
    } catch (error) {
        console.error('Delete shape error:', error);
        showToast('Error deleting shape: ' + error.message, 'error');
    }
}

async function clearAllCustomShapes() {
    const customShapes = customShapesList.querySelectorAll('.shape-item');
    const count = customShapes.length;
    
    if (count === 0) {
        showToast('No custom shapes to clear', 'warning');
        return;
    }
    
    if (!confirm(`Are you sure you want to delete all ${count} custom shapes? This action cannot be undone.`)) {
        return;
    }
    
    try {
        clearAllCustomShapesBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Clearing...';
        clearAllCustomShapesBtn.disabled = true;
        
        const response = await fetch('/clear_all_custom_shapes', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message, 'success');
            
            // Reload the custom shapes list
            loadCustomShapes();
            
            // Update the shape selector
            updateShapeSelector();
            
            // Switch to square if a custom shape was selected
            if (!isBuiltInShape(currentShape)) {
                shapeSelect.value = 'square';
                updateShapePreview();
            }
            
        } else {
            throw new Error(data.error || 'Failed to clear custom shapes');
        }
        
    } catch (error) {
        console.error('Clear all shapes error:', error);
        showToast('Error clearing custom shapes: ' + error.message, 'error');
    } finally {
        clearAllCustomShapesBtn.innerHTML = '<i class="fas fa-trash"></i> Clear All Custom Shapes';
        clearAllCustomShapesBtn.disabled = false;
    }
}

function useCustomShape(shapeName) {
    // Switch to premade tab and select the custom shape
    switchTab('premade');
    shapeSelect.value = shapeName;
    updateShapePreview();
    showToast(`Using custom shape: ${shapeName}`, 'success');
}

function clearTitle() {
    document.getElementById('title').value = '';
    generatePreview();
    showToast('Title cleared', 'success');
}

function clearSubject() {
    document.getElementById('subject').value = '';
    generatePreview();
    showToast('Subject cleared', 'success');
}

function loadSampleWords() {
    // Optional: Load some sample words for demonstration
    // Disabled by default - users start with empty list
    const sampleWords = ['PUZZLE', 'SEARCH', 'WORDS', 'FIND', 'GAME', 'FUN'];
    words = [...sampleWords];
    updateWordList();
    updateWordCount();
    generatePreview();
}

async function generatePreview() {
    if (words.length === 0) {
        puzzlePreview.innerHTML = `
            <div class="preview-placeholder">
                <i class="fas fa-puzzle-piece"></i>
                <p>Add words to see preview</p>
            </div>
        `;
        wordsToFind.innerHTML = '<p class="empty-message">Words will appear here</p>';
        return;
    }
    
    try {
        // Show loading state
        puzzlePreview.innerHTML = `
            <div class="preview-placeholder">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Generating preview...</p>
            </div>
        `;
        
        // Prepare form data
        const formData = new FormData();
        formData.append('words', words.join('\n'));
        formData.append('shape', currentShape);
        formData.append('allowVertical', document.getElementById('allowVertical').checked ? 'on' : 'off');
        formData.append('allowHorizontal', document.getElementById('allowHorizontal').checked ? 'on' : 'off');
        formData.append('allowDiagonal', document.getElementById('allowDiagonal').checked ? 'on' : 'off');
        
        // Send preview request
        const response = await fetch('/preview', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayPuzzlePreview(data.grid, data.words);
            displayWordsToFind(data.words);
        } else {
            throw new Error(data.error || 'Failed to generate preview');
        }
        
    } catch (error) {
        console.error('Preview error:', error);
        puzzlePreview.innerHTML = `
            <div class="preview-placeholder">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Error generating preview</p>
                <small>${error.message}</small>
            </div>
        `;
        showToast('Error generating preview: ' + error.message, 'error');
    }
}

function displayPuzzlePreview(grid, placedWords) {
    let html = '<table class="puzzle-grid">';
    
    for (let i = 0; i < grid.length; i++) {
        html += '<tr>';
        for (let j = 0; j < grid[i].length; j++) {
            const letter = grid[i][j] || '';
            html += `<td>${letter}</td>`;
        }
        html += '</tr>';
    }
    
    html += '</table>';
    
    puzzlePreview.innerHTML = html;
}

function displayWordsToFind(placedWords) {
    if (placedWords.length === 0) {
        wordsToFind.innerHTML = '<p class="empty-message">No words could be placed</p>';
        return;
    }
    
    wordsToFind.innerHTML = placedWords.map(word => 
        `<div class="word-tag">${word}</div>`
    ).join('');
}

async function generatePuzzle() {
    if (words.length === 0) {
        showToast('Please add some words first', 'warning');
        return;
    }
    
    try {
        // Show loading state
        generatePuzzleBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        generatePuzzleBtn.disabled = true;
        
        // Prepare form data
        const formData = new FormData();
        formData.append('title', document.getElementById('title').value || 'Word Search Puzzle');
        formData.append('subject', document.getElementById('subject').value || '');
        formData.append('words', words.join('\n'));
        formData.append('shape', currentShape);
        formData.append('font', document.getElementById('fontSelect').value);
        formData.append('theme', document.getElementById('themeSelect').value);
        formData.append('exportFormat', exportFormat.value);
        formData.append('allowVertical', document.getElementById('allowVertical').checked ? 'on' : 'off');
        formData.append('allowHorizontal', document.getElementById('allowHorizontal').checked ? 'on' : 'off');
        formData.append('allowDiagonal', document.getElementById('allowDiagonal').checked ? 'on' : 'off');
        
        // Send generation request
        const response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Download the file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = response.headers.get('Content-Disposition')?.split('filename=')[1] || 'puzzle.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showToast('Puzzle generated successfully!', 'success');
        } else {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to generate puzzle');
        }
        
    } catch (error) {
        console.error('Generation error:', error);
        showToast('Error generating puzzle: ' + error.message, 'error');
    } finally {
        // Reset button state
        generatePuzzleBtn.innerHTML = '<i class="fas fa-download"></i> Generate Puzzle';
        generatePuzzleBtn.disabled = false;
    }
}

function randomizeWords() {
    if (words.length === 0) {
        showToast('No words to randomize', 'warning');
        return;
    }
    
    // Fisher-Yates shuffle algorithm
    for (let i = words.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [words[i], words[j]] = [words[j], words[i]];
    }
    
    updateWordList();
    generatePreview();
    showToast('Words randomized!', 'success');
}

function parsePastedWords(text) {
    if (!text.trim()) return [];
    
    // Split by various delimiters: newlines, commas, tabs, semicolons, and multiple spaces
    const words = text
        .split(/[\n\r,;\t]+|\s{2,}/) // Split by newlines, commas, semicolons, tabs, or multiple spaces
        .map(word => word.trim().toUpperCase()) // Clean and uppercase each word
        .filter(word => word.length > 0 && /^[A-Z\s]+$/.test(word)); // Filter out empty words and non-letter characters
    
    // Remove duplicates while preserving order
    return [...new Set(words)];
}

function updatePastePreview() {
    const text = pasteWordsTextarea.value;
    const parsedWords = parsePastedWords(text);
    
    pasteCount.textContent = parsedWords.length;
    
    if (parsedWords.length === 0) {
        pastePreview.innerHTML = '<p class="no-words">No valid words found</p>';
        addPastedWordsBtn.disabled = true;
        return;
    }
    
    // Show preview of words (limit to first 20 for display)
    const displayWords = parsedWords.slice(0, 20);
    const remainingCount = parsedWords.length - 20;
    
    pastePreview.innerHTML = displayWords.map(word => 
        `<span class="preview-word">${word}</span>`
    ).join('') + (remainingCount > 0 ? `<span class="more-words">... and ${remainingCount} more</span>` : '');
    
    addPastedWordsBtn.disabled = false;
}

function addPastedWords() {
    const text = pasteWordsTextarea.value;
    const parsedWords = parsePastedWords(text);
    
    if (parsedWords.length === 0) {
        showToast('No valid words found to add', 'warning');
        return;
    }
    
    // Filter out words that already exist
    const newWords = parsedWords.filter(word => !words.includes(word));
    const duplicateCount = parsedWords.length - newWords.length;
    
    if (newWords.length > 0) {
        words = [...words, ...newWords];
        updateWordList();
        updateWordCount();
        generatePreview();
        
        let message = `${newWords.length} word${newWords.length !== 1 ? 's' : ''} added`;
        if (duplicateCount > 0) {
            message += ` (${duplicateCount} duplicate${duplicateCount !== 1 ? 's' : ''} skipped)`;
        }
        showToast(message, 'success');
    } else {
        showToast('All words already exist in the list', 'warning');
    }
    
    closePasteModal();
}

function openFileUpload() {
    // Create file input for word list upload
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.txt,.csv,.xlsx,.xls,.docx,.doc';
    
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (file) {
            const fileName = file.name.toLowerCase();
            
            // Check file extension
            if (fileName.endsWith('.xlsx') || fileName.endsWith('.xls')) {
                showToast('Excel files not yet supported. Please use .txt or .csv files.', 'warning');
                return;
            } else if (fileName.endsWith('.docx') || fileName.endsWith('.doc')) {
                showToast('Word documents not yet supported. Please use .txt or .csv files.', 'warning');
                return;
            }
            
            const reader = new FileReader();
            reader.onload = function(e) {
                const content = e.target.result;
                const lines = content.split(/[\n,]/).map(line => line.trim()).filter(line => line);
                
                if (lines.length > 0) {
                    words = [...new Set([...words, ...lines.map(word => word.toUpperCase())])];
                    updateWordList();
                    updateWordCount();
                    generatePreview();
                    showToast(`${lines.length} words loaded from file`, 'success');
                } else {
                    showToast('No valid words found in file', 'warning');
                }
            };
            reader.readAsText(file);
        }
    };
    
    input.click();
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Theme toggle functionality
document.getElementById('themeToggle').addEventListener('click', function() {
    document.body.classList.toggle('dark-theme');
    const icon = this.querySelector('i');
    if (document.body.classList.contains('dark-theme')) {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
});

// Font size toggle functionality
document.getElementById('fontSizeToggle').addEventListener('click', function() {
    document.body.classList.toggle('large-font');
    const icon = this.querySelector('i');
    if (document.body.classList.contains('large-font')) {
        icon.className = 'fas fa-text-height';
        icon.style.transform = 'scaleY(1.2)';
    } else {
        icon.className = 'fas fa-text-height';
        icon.style.transform = 'scaleY(1)';
    }
});

// Add CSS for theme and font size toggles
const style = document.createElement('style');
style.textContent = `
    .dark-theme {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: #ecf0f1;
    }
    
    .dark-theme .header,
    .dark-theme .sidebar,
    .dark-theme .preview-section {
        background: rgba(44, 62, 80, 0.95);
        color: #ecf0f1;
    }
    
    .dark-theme .form-group input,
    .dark-theme .form-group select {
        background: #34495e;
        border-color: #4a5f7a;
        color: #ecf0f1;
    }
    
    .dark-theme .word-list-container {
        background: #34495e;
        border-color: #4a5f7a;
    }
    
    .dark-theme .puzzle-preview {
        background: #34495e;
    }
    
    .large-font {
        font-size: 1.1em;
    }
    
    .large-font .puzzle-grid td {
        font-size: 1.3rem;
        width: 40px;
        height: 40px;
    }
`;
document.head.appendChild(style);
