import os
import requests
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'your_secret_key'
API_KEY = 'K85173817188957'

# Function to extract text from image using OCR.space API
def extract_text_from_image(file_path):
    url = 'https://api.ocr.space/parse/image'
    payload = {
        'apikey': API_KEY,
        'language': 'eng',
        'isOverlayRequired': False
    }
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files, data=payload)
    if response.status_code == 200:
        result = response.json()
        if 'ParsedResults' in result and result['ParsedResults']:
            return result['ParsedResults'][0]['ParsedText']
    return None

# Function to separate MCQ type questions and options
def separate_mcq(text):
    mcqs = []
    lines = text.split('\n')
    current_mcq = {'number': None, 'text': None, 'options': []}

    for line in lines:
        line = line.strip()
        if line.startswith('a)') or line.startswith('b)') or line.startswith('c)') or line.startswith('d)'):
            # Add option to current MCQ
            current_mcq['options'].append(line)
        elif line and line[0].isdigit() and line[1] == '.':
            # If we encounter a new MCQ number, store the previous MCQ (if any) and start a new one
            if current_mcq['number'] is not None:
                mcqs.append(current_mcq)
                current_mcq = {'number': None, 'text': None, 'options': []}
            # Extract MCQ number and text
            current_mcq['number'], current_mcq['text'] = line.split('. ', 1)
        elif not line:
            # End of MCQ, store the current MCQ
            if current_mcq['number'] is not None:
                mcqs.append(current_mcq)
                current_mcq = {'number': None, 'text': None, 'options': []}

    # Add the last MCQ (if any)
    if current_mcq['number'] is not None:
        mcqs.append(current_mcq)

    return mcqs

@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # Save the file to the uploads folder
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Extract text from the uploaded image using OCR.space API
            text = extract_text_from_image(file_path)
            if text:
                # Separate MCQ type questions and options
                mcqs = separate_mcq(text)
                return render_template('mock2.html', mcqs=mcqs)
            else:
                flash('Failed to extract text from file')
                return redirect('/')
    return render_template('upload.html')

@app.route('/result')
def result():
    score = request.args.get('score')
    return render_template('result.html', score = score)


if __name__ == '__main__':
    app.run(debug=True)
