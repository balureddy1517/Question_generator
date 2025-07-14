import json
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

questionjson_path=os.getenv("QUESTION_JSON")

with open(questionjson_path, 'r') as file:
        examples=json.load(file)
        
        

graph_system_prompt = '''
You are a SAT math question generator that specializes in **figure-based quadratic graph questions**.

Your goal is to create **graphical multiple choice questions** that test students' understanding of **quadratic functions**, specifically based on their graphs.

Every question must:
- Be related to a **quadratic function graph** (e.g., parabolas in standard, vertex, or factored form)
- Be a **multiple-choice** question (4 options only)
- Include a valid **quadratic equation**
- Contain **enough information in the JSON** (`equation`, `key_features`) to allow someone to **plot the parabola**
- Ask questions that require **interpreting the graph data**, NOT just guessing from options
- Include full metadata in the required JSON format

Important rules:
- The **question should NOT rely on answer options** to understand the function or graph.
- All necessary data for graphing (e.g., vertex, intercepts, axis) should be available in the JSON under `equation` and `key_features`.
- Use realistic SAT-level difficulty levels (Easy, Medium, Hard).

Return each question as a JSON object in the following format:

{
  "content_name": "Problem Solving and Data Analysis",
  "question_type": "Graph",
  "question_choice": "question body (related to the graph, not the answers)",
  "option_a": "Option A",
  "option_b": "Option B",
  "option_c": "Option C",
  "option_d": "Option D",
  "answer": "exact text of correct option",
  "difficulty_level": "Easy | Medium | Hard",
  "category_type": "Maths",
  "feedback": "Detailed explanation of all answer options, especially the correct one",
  "parabola_type": "Standard | Vertex | Factored",
  "equation": "e.g. y = x^2 + 4x + 3",
  "key_features": {
    "vertex": "(x, y)",
    "axis_of_symmetry": "x = value",
    "x_intercepts": ["value1", "value2"],
    "y_intercept": "value"
  }
}
'''


graph_user_prompt = f'''
Below are example SAT math questions involving **quadratic graphs (parabolas)**.

Use these as reference to generate **10 NEW tricky and exam-like questions** that:
- Are **multiple choice**
- All involve **parabolic graphs** (quadratic functions)
- Vary in difficulty (Easy, Medium, Hard)
- Contain graph data (equation or key points like vertex, intercepts, etc.)
- Include full equation and features of the parabola
- Return results as a **clean JSON array** of question objects with NO extra explanation or text

EXAMPLES:
{examples}

Now generate 10 new figure-based quadratic graph questions in the specified format.
'''



generator = ChatOpenAI(
    openai_api_key=os.getenv("API_KEY"),
    model="gpt-4o",
    temperature=0.8
)

messages = [
    {"role": "system", "content": graph_system_prompt},
    {"role": "user", "content": graph_user_prompt}
]


response = generator.invoke(messages)
llm_response=response.content

print(llm_response)


cleaned_json = llm_response.strip().removeprefix("```json").removesuffix("```").strip()

parsed_data = json.loads(cleaned_json)

with open("Quad_equations_ques.json", "w", encoding="utf-8") as out_file:
        json.dump(parsed_data, out_file, indent=2, ensure_ascii=False)