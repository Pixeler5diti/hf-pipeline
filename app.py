import openai
import os
import PyPDF2
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def generate_questions_from_text(text):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Based on the following text, generate 5 questions with answers:\n{text}"}
            ]
        )
        questions_and_answers = completion.choices[0].message['content']
        return questions_and_answers
    except Exception as e:
        print(f"Error generating questions: {e}")
        return "Questions and answers not available"

def generate_study_material(pdf_path, filename="study_material.txt"):
  
    text = extract_text_from_pdf(pdf_path)
    
    
    questions_and_answers = generate_questions_from_text(text)
    
    
    with open(filename, 'w') as file:
        file.write(questions_and_answers)
    
    print(f"Study material saved to {filename}")


pdf_path = r"" #enter path to your pdf file
#your text file is ready,check downloads folder :)
generate_study_material(pdf_path)
