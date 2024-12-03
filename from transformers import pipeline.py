import openai
import os
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize

openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


def generate_questions_from_text(text):
    words = word_tokenize(text)
    question_terms = ['circular', 'queue', 'stack', 'binary', 'linked', 'complexity', 'insert', 'delete', 'operation', 'algorithm', 'singly', 'doubly']
    questions = []
    for term in question_terms:
        if term in words:
            if term == 'circular':
                questions.append("What is a Circular Linked List and how does its insertion and deletion work?")
            elif term == 'queue':
                questions.append("What are the different operations of a Queue and how do you implement them?")
            elif term == 'stack':
                questions.append("Explain the Stack data structure and its basic operations.")
            elif term == 'binary':
                questions.append("What is the Binary Search algorithm and how does it work?")
            elif term == 'linked':
                questions.append("What is a Linked List and how do you perform insertion and deletion operations?")
            elif term == 'complexity':
                questions.append("What is the time complexity of Binary Search?")
            elif term == 'insert':
                questions.append("How do you insert a node in a Singly Linked List?")
            elif term == 'delete':
                questions.append("How do you delete a node from a Queue?")
            elif term == 'operation':
                questions.append("What are the main operations of a Stack?")
            elif term == 'algorithm':
                questions.append("What is an algorithm? Explain with an example.")
            elif term == 'singly':
                questions.append("What is a Singly Linked List and how does it differ from a Doubly Linked List?")
            elif term == 'doubly':
                questions.append("What are the advantages of a Doubly Linked List over a Singly Linked List?")

    return questions
    #usin openai to get me the answes :)
def get_answer_from_openai(question):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",  # Use the appropriate model here
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        answer = completion.choices[0].message['content']
        return answer
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "Answer not available"

#  generatin a study material text file
def generate_study_material(pdf_path, filename="study_material.txt"):
    
    text = extract_text_from_pdf(pdf_path)
    questions = generate_questions_from_text(text)
    
    with open(filename, 'w') as file:
        for i, question in enumerate(questions, 1):
            file.write(f"Q: {question}\n")
            answer = get_answer_from_openai(question)
            file.write(f"A: {answer}\n\n")
    
    print(f"Study material saved to {filename}")


pdf_path = r'enter the path to your pdf file'


generate_study_material(pdf_path)
