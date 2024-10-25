import re

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

# Example usage
text = """Here are the 10 multiple-choice questions based on the key concepts discussed in the lecture or meeting: Q1: What is a cell? A1: A cell is the smallest unit of life that can function independently. Q2: What are prokaryotic and eukaryotic cells? A2: Prokaryotic cells, such as bacteria, lack a nucleus and other membrane-bound organelles. Eukaryotic cells make up plants, animals, fungi, and protists, which contain a nucleus that houses genetic material. Q3: What are the key components of a eukaryotic cell? A3: 1) Nucleus: The control center of the cell where DNA is stored and gene expression is regulated. 2) Mitochondria: Often referred to as the powerhouse of the cell, they convert nutrients into energy through cellular respiration. This energy is crucial for all cellular activities. Q4: What are the functions of each component mentioned? A4: 1) Nucleus: Regulates gene expression and is essential for cell replication. 2) Mitochondria: Convert nutrients into energy through cellular respiration. 3) Ribosomes: The sites of protein synthesis, where proteins can be made from amino acids. 4) Endoplasmic Reticulum (ER): Studded with ribosomes to synthesize proteins; involved in protein production and lipid synthesis. 5) Cell Membrane: Acts as a barrier controlling what enters and exits the cell. Q5: Why is understanding cells crucial? A5: Understanding cells is crucial for multiple reasons, including health and disease prevention, biotechnology breakthroughs, and ecological importance. Q6: What are some key applications of cell biology research? A6: 1) Health and disease research; researchers can develop targeted therapies and interventions. 2) Biotechnology advancements in genetically modified organisms and stem cell research have profound implications for medicine, agriculture, and environmental science. Q7: What is the role of cells in ecosystems? A7: Cells play a critical role in ecosystems by producing oxygen through photosynthesis, impacting global climate and carbon cycles. Q8: Why are cells the foundation of life? A8: Cells are the foundation of life because they are responsible for carrying out fundamental biological processes such as DNA replication, mitosis, and cell death regulation. Q9: What is a key difference between prokaryotic and eukaryotic cells? A9: Prokaryotic cells lack a nucleus and other membrane-bound organelles, while eukaryotic cells have a complex internal structure with a nucleus containing genetic material. Q10: How does understanding fundamental biological processes help address health challenges and environmental issues? A10: Understanding fundamental biological processes helps address health challenges and environmental issues by informing the development of targeted therapies, interventions, and sustainable practices."""  # Replace with the actual text

qa_pairs = extract_qa_pairs(text)

ret = []

# Print the extracted pairs in a formatted way
for i, pair in enumerate(qa_pairs, 1):
    # print(f"Q{i}: {pair['question']}")
    # print(f"A: {pair['answer']}")

    ret.append({
        'question': pair['question'],
        'answer': pair['answer']
    })

print(ret)

