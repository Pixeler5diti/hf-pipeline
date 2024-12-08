import os
import PyPDF2
from collections import Counter
import re

# Replace this with a local LLM (e.g., GPT4All or llama.cpp)
def generate_questions_and_answers_local(text, trends):
    # Placeholder function: Replace with local LLM integration
    similar_questions = [f"Sample question about {topic}" for topic, _ in trends.most_common(5)]
    answers = ["Generated answer" for _ in similar_questions]
    return list(zip(similar_questions, answers))

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def analyze_qna_trends(text):
    questions = re.findall(r'Q:\s*(.+)', text)
    answers = re.findall(r'A:\s*(.+)', text)
    topics = [q.split()[0] for q in questions]  # Extract first words as topics
    topic_trends = Counter(topics)
    return questions, answers, topic_trends

def generate_study_material(pdf_path, filename="study_material.txt"):
    # Step 1: Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Analyze Q&A trends
    questions, answers, trends = analyze_qna_trends(text)
    
    # Step 3: Generate similar questions and answers
    similar_qna = generate_questions_and_answers_local(text, trends)
    
    # Step 4: Save results to file
    with open(filename, 'w') as file:
        file.write("Generated Study Material:\n\n")
        for idx, (q, a) in enumerate(similar_qna, 1):
            file.write(f"Q{idx}: {q}\n")
            file.write(f"A{idx}: {a}\n\n")
    print(f"Study material saved to {filename}")

# Example usage
pdf_path = "path_to_previous_qna.pdf"
generate_study_material(pdf_path)
