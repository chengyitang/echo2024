from langchain_ollama import OllamaLLM
from flask import Flask, request, render_template, jsonify
import logging
import re
import PyPDF2
import os
from werkzeug.utils import secure_filename

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'mp3', 'mp4'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return None
    
# Define prompts for different output types
OUTPUT_PROMPTS = {
    'qa': "Create 10 multiple-choice and based on the key concepts discussed in the lecture or meeting. Provide correct answers and brief explanations for each. Return in the following format: Q1: the question A1: the answer. Following content: ",
    'transcripts': "Generate a detailed, well-structured transcript from the following content: ",
    'notes': "Based on the provided lecture or meeting transcript, summarize the theme and ten key points (bullet points), create a concise set of notes for easy review. Following content:",
    'summary': "Generate a comprehensive summary of the following content:"
}

def initialize_llama():
    try:
        # Initialize the LLaMA model directly
        llama_model = OllamaLLM(model="llama3.2:1b") # Change your model version here
        return llama_model
    except Exception as e:
        logging.error(f"Failed to initialize LLM: {e}")
        raise

llama_model = initialize_llama()

def prompt_ollama(content, output_types):
    results = {}

    for output_type in output_types:
        predefined_prompt = OUTPUT_PROMPTS[output_type]
        if output_type in OUTPUT_PROMPTS:
            prompt = f"{predefined_prompt} {content}"

        try:
            response = llama_model.invoke(prompt)
            #print('predefined_prompt:', predefined_prompt, "\n")
            #print('response:', response)
            results[output_type] = response
        except Exception as e:
            logging.error(f"Error invoking LLM: {e}")
            results[output_type] = "None"
    
    return results

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        output_types = request.form.getlist('output_types')
        
        # Check if a file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract content based on file type
            if filename.endswith('.pdf'):
                content = extract_text_from_pdf(filepath)
                if content is None:
                    return jsonify({'error': 'Failed to extract text from PDF'})
            else:
                # Handle other file types (mp3, mp4) here
                return jsonify({'error': 'File type not yet supported'})
            
            # Process content with LLM
            results = prompt_ollama(content, output_types)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify(results)
        
        return jsonify({'error': 'Invalid file type'})
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
