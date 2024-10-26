from langchain_ollama import OllamaLLM
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import logging
import re
import PyPDF2
import os
from werkzeug.utils import secure_filename
import to_text

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'mp3', 'mp4'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Extract text from a PDF file
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
    'qa': "Create 10 multiple-choice and based on the key concepts discussed in the lecture or meeting. Provide correct answers including brief explanations for each question. Return in the following format: Q<n>: the question\n A<n>: the answer\n (<n> is the question number)\n Following content: ",
    'transcripts': "Generate a detailed, well-structured transcript from the following content: ",
    'notes': 
    """
    Based on the provided lecture or meeting transcript, summarize the theme and ten key points, create a concise set of notes for easy review.\n
    Each note Output format are as follows:
    Key word1: explanation and summary,
    Key word2: explanation and summary,
    ……,
    Key word10: explanation and summary

    """,
    'summary': "Generate a comprehensive summary of the following content:",
    'learing_objectives': """ 
    From the provided lecture transcript, identify the primary 10 learning objectives. Adhere strictly to the format given where the response should contain no more than 1000 characters in total. List each objective as follows:
        Objective 1,
        Objective 2,
        …,
        Objective 10
        Do not provide explanations, interpretations, or any output beyond this format.
    """,
    'Action_items':"""
    Generate 8 action items based on the discussion in the meeting.If possible, list them in order by considering both importance and urgency. Include the task, responsible person, and deadlines if mentioned as the following format:
        1. Task:,
        Responsible Person:,
        Deadline
        2. Task:,
        Responsible Person:,
        Deadline
        etc.
    """,
    
    
}

# Initialize the LLaMA model
def initialize_llama():
    try:
        # Initialize the LLaMA model directly
        llama_model = OllamaLLM(model="llama3.1:8b") # Change your model version here
        return llama_model
    except Exception as e:
        logging.error(f"Failed to initialize LLM: {e}")
        raise

llama_model = initialize_llama()

# Prompt the LLaMA model
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

def extract_qa_pairs(text):
    """
    Extract question-answer pairs from text where questions are marked with Q1, Q2, etc.
    and answers are marked with A1, A2, etc.
    
    Args:
        text (str): Input text containing question-answer pairs
        
    Returns:
        list: List of dictionaries containing question-answer pairs
    """
    # Split the text into individual QA pairs
    qa_pairs = []
    
    # Find all questions using regex
    questions = re.findall(r'Q\d+:\s*(.*?)\s*(?=A\d+:|$)', text)
    
    # Find all answers using regex
    answers = re.findall(r'A\d+:\s*(.*?)\s*(?=Q\d+:|$)', text)
    
    # Combine questions and answers into pairs
    for i in range(len(questions)):
        qa_pairs.append({
            'question': questions[i].strip(),
            'answer': answers[i].strip()
        })

    ret = []

    # Print the extracted pairs in a formatted way
    for i, pair in enumerate(qa_pairs, 1):
        # print(f"Q{i}: {pair['question']}")
        # print(f"A: {pair['answer']}")

        ret.append({
            'question': pair['question'],
            'answer': pair['answer']
        })
    
    return ret

@app.route('/api/extract-text', methods=['POST'])
def extract_text_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract text
        text_content = to_text.to_text(filepath)

        # Clean up uploaded and temporary files
        os.remove(filepath)
        temp_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav')
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

        if text_content is None:
            return jsonify({'error': 'Failed to extract text from the file'}), 500

        return jsonify({'text': text_content}), 200

    return jsonify({'error': 'Invalid file type'}), 400

            
# Main route for the Flask app
@app.route('/api/process-content', methods=['POST'])
def process_content():
    data = request.get_json()
    content = data.get('content', '')
    data_types = data.get('data_types', [])

    if not content:
        return jsonify({'error': 'No content provided'}), 400
    print(data)

    # Process content with LLM using default output types
    results = prompt_ollama(content, data_types)

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)
