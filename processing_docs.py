import fitz  # PyMuPDF
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

def initializing_llm():
    client = OpenAI(
        api_key=os.getenv("API_KEY")
    )
    return client

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    page_texts = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        page_texts.append({"page_number": i+1, "text": text})
    return page_texts


def build_system_prompt():
    return (
        "You are a SAT Math Question Extractor.\n"
        "Your job is to extract all SAT math questions related to *Quadratic Equations* from the raw input text.\n\n"
        "Instructions:\n"
        "1. Extract each complete question related to Quadratic Equations.\n"
        "2. If answer options are present, group them under an 'options' list.\n"
        "3. If no options are present, just include the question text.\n"
        "4. Ignore any questions that are not related to Quadratic Equations.\n\n"
        "Return the result as a JSON array of objects like this:\n"
        "[\n"
        "  {\n"
        '    "question_number": 1,\n'
        '    "question_text": "What is the value of x in the equation x^2 - 5x + 6 = 0?",\n'
        '    "options": ["A) 2 and 3", "B) -2 and -3", "C) 1 and 6", "D) No solution"]\n'
        "  },\n"
        "  {\n"
        '    "question_number": 2,\n'
        '    "question_text": "Solve for x: x^2 = 49"\n'
        "  }\n"
        "]"
    )

def build_user_prompt(page_text):
    return f"Here is the raw text from a SAT math page:\n---\n{page_text}\n---"


def call_llm(system_prompt, user_prompt,client):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.1
    )
    output = response.choices[0].message.content
    # question_data = json.loads(output)
    return output


def save_page_output(page_number, doc_name,llm_output, output_dir="output_text"):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{doc_name}_page_{page_number}_questions.txt")
    with open(path, "w") as f:
        f.write(llm_output)



def process_pdf(pdf_path,doc_name):
    pages = extract_text_from_pdf(pdf_path)
    system_prompt = build_system_prompt()
    client=initializing_llm()
    i=0

    for page in pages:
        user_prompt = build_user_prompt(page["text"])
        llm_output = call_llm(system_prompt, user_prompt,client)
        print(llm_output)
        save_page_output(page["page_number"], doc_name,llm_output)
        if(i==5):
            break
        i+=1


input_docs_path='/Users/balakrishnareddyragannagari/Desktop/Sat_questions/Question_generator/docs'
docs=os.listdir(input_docs_path)

for doc in docs:
    doc_path=os.path.join(input_docs_path,doc)
    process_pdf(doc_path,doc)
