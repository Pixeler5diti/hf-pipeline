from transformers import pipeline
from PyPDF2 import PdfReader

# Step 1: Load Question Generation Pipeline
qg_pipeline = pipeline("text2text-generation", model="valhalla/t5-small-qg-prepend")

# Step 2: Extract Text from PDF
def extract_text_from_pdf("C:\Users\Upma\Documents\genai\Generative Deep Learning, 2nd Edition.pdf"):
    """
    Extracts text from a PDF file.

    Args:
    pdf_path (str): Path to the PDF file.

    Returns:
    str: Extracted text from the PDF.
    """
    from PyPDF2 import PdfReader  # Ensure this import is at the top if running the whole script.
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    return full_text
# Step 3: Split Text into Chunks
def split_text_into_chunks(text, chunk_size=500):
    """
    Splits text into smaller chunks.

    Args:
    text (str): The text to split.
    chunk_size (int): Number of words per chunk.

    Returns:
    list: A list of text chunks.
    """
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Step 4: Generate Questions from Chunks
def generate_questions(text_chunks, num_questions=3):
    """
    Generates questions from text chunks using a Hugging Face pipeline.

    Args:
    text_chunks (list): List of text chunks.
    num_questions (int): Number of questions per chunk.

    Returns:
    dict: A dictionary mapping chunk indices to generated questions.
    """
    all_questions = {}
    for idx, chunk in enumerate(text_chunks):
        try:
            generated = qg_pipeline(f"generate question: {chunk}", 
                                    max_length=100, 
                                    num_return_sequences=num_questions)
            all_questions[f"Chunk {idx + 1}"] = [q["generated_text"] for q in generated]
        except Exception as e:
            all_questions[f"Chunk {idx + 1}"] = [f"Error: {str(e)}"]
    return all_questions

# Step 5: Main Function to Process PDF
def process_pdf_and_generate_questions(pdf_path, chunk_size=500, num_questions=3, output_file="output_questions.txt"):
    """
    Processes a PDF file to generate questions for each text chunk.

    Args:
    pdf_path (str): Path to the PDF file.
    chunk_size (int): Number of words per chunk.
    num_questions (int): Number of questions per chunk.
    output_file (str): Path to save the generated questions.
    """
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)

    print("Splitting text into chunks...")
    chunks = split_text_into_chunks(text, chunk_size=chunk_size)

    print(f"Generating questions for {len(chunks)} chunks...")
    questions = generate_questions(chunks, num_questions=num_questions)

    print("Saving questions to file...")
    with open(output_file, "w") as f:
        for chunk, qs in questions.items():
            f.write(f"{chunk}:\n")
            f.writelines(f"- {q}\n" for q in qs)
            f.write("\n")
    print(f"Questions saved to {output_file}!")

# Step 6: Run the Script
if __name__ == "__main__":
    pdf_path = "path_to_your_pdf.pdf"  # Replace with the path to your PDF
    process_pdf_and_generate_questions(pdf_path, chunk_size=500, num_questions=3)
