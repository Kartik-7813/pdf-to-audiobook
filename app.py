from flask import Flask, request, render_template, send_from_directory, after_this_request
from werkzeug.utils import secure_filename
import os
import fitz
from gtts import gTTS
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = 'audio'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)

        # Extract text from PDF
        try:
            pdf = fitz.open(pdf_path)
            text = ''
            for page in pdf:
                text += page.get_text()
            pdf.close()
            
            if not text.strip():
                    return 'No text could be extracted from the PDF', 400

            # Convert text to audio
            audio_filename = f"{uuid.uuid4()}.mp3"
            audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
            tts = gTTS(text=text, lang='en')
            tts.save(audio_path)

            # Automatic cleanup after response
            @after_this_request
            def cleanup(response):
                try:
                    os.remove(pdf_path)
                    # Audio file cleanup after download can be handled separately
                except Exception:
                    pass
                return response

            return render_template('result.html', audio_file=audio_filename)

        except Exception as e:
            return f'Error processing PDF: {str(e)}', 500
    return 'Invalid file format. Please upload a PDF.', 400

@app.route('/download/<filename>')
def download_file(filename):
    @after_this_request
    def cleanup(response):
        try:
            audio_path = os.path.join(app.config['AUDIO_FOLDER'], filename)
            os.remove(audio_path)
        except Exception:
            pass
        return response
    return send_from_directory(app.config['AUDIO_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
