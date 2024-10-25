from langchain_ollama import OllamaLLM # type: ignore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
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
    'qa': "Generate a Q&A format response for the following content: {content}",
    'transcripts': "Generate a detailed transcript from the following content: {content}",
    'notes': "Generate concise notes highlighting key points from the following content: {content}",
    'summary': "Generate a comprehensive summary of the following content: {content}"
}

# # Define a function to format text by converting Markdown bold syntax to HTML strong tags
# def format_output(text):
#     """Convert Markdown bold syntax to HTML strong tags."""
#     return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

# Define chatbot initialization
def initialize_llama():
    try:
        llama_model = OllamaLLM(model="llama3.2:1b")
        format_output = StrOutputParser()
        return llama_model, format_output
    except Exception as e:
        logging.error(f"Failed to initialize LLM: {e}")
        raise

def process_with_llm(content, output_types):
    llama_model, output_parser = initialize_llama()
    results = {}
    
    for output_type in output_types:
        if output_type in OUTPUT_PROMPTS:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a professional content analyzer"),
                ("user", OUTPUT_PROMPTS[output_type])
            ])
            chain = prompt | llama_model | output_parser
            try:
                response = chain.invoke({'content': content})
                results[output_type] = response
            except Exception as e:
                logging.error(f"Error processing {output_type}: {e}")
                results[output_type] = f"Error generating {output_type}"
    
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
            results = process_with_llm(content, output_types)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify(results)
        
        return jsonify({'error': 'Invalid file type'})
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)