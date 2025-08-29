# PDF to Audiobook Converter
This is a simple web application that converts a PDF file into an audiobook. It uses Flask for the web framework, PyPDF2 to extract text from the PDF, and gTTS (Google Text-to-Speech) to generate the audio.

## Features
- Upload PDF: Users can upload a PDF file through a simple web interface.
- Convert to Audio: The application extracts text from the PDF and converts it into an MP3 audio file.
- Download Audio: Once converted, the user can download the generated audiobook.

## Installation
- Prerequisites: Make sure you have Python 3.x installed.

- Steps
  1. Clone the repository:
    git clone https://github.com/Kartik-7813/pdf-to-audiobook.git
    cd pdf-to-audiobook

  2. Create a virtual environment (optional but recommended):
     - For Linux: 
       python -m venv venv
       source venv/bin/activate

     - For Windows:
       python -m venv venv
       venv\Scripts\activate

  3. Install the required libraries:
     pip install -r requirements.txt
     
## Usage
- To run the application, execute the following command in your terminal:
flask run
- Open your web browser and navigate to http://127.0.0.1:5000 to access the application.
