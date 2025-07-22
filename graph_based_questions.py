import json
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import JSONLoader
from langchain.embeddings import HuggingFaceEmbeddings

import json
from pathlib import Path
from pprint import pprint


load_dotenv()

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def metadata_func(record: dict, metadata: dict) -> dict:

    metadata["graph_type"] = record.get("graph_data")['type']
    return metadata

# loader = JSONLoader(
#     file_path='extracted_questions.json',
#     jq_schema='.[]',
#     content_key="question_text",
#     metadata_func=metadata_func
# )

# data = loader.load()

# # print(data)



# vectorstore = FAISS.from_documents(data, embedding_model)

# vectorstore.save_local("faiss_sat_questions_db")

# print("stored in vector db")


vectorstore = FAISS.load_local("faiss_sat_questions_db", embedding_model,allow_dangerous_deserialization=True)

def search_by_graph_type(vectorstore, query, graph_type, k=10):
    results = vectorstore.similarity_search(query, k=k)
    return [doc for doc in results if doc.metadata.get("graph_type", "").lower() == graph_type.lower()]


results = search_by_graph_type(vectorstore, "circle", "circle")

examples=[]
for doc in results:
    temp={}
    temp['question']=doc.page_content
    temp['graph type']=doc.metadata.get("graph_type")
    examples.append(temp)


print(examples)

questions="circle"

system_prompt = (
    '''
You are an expert SAT math question generator focused on graph-based visual reasoning.

You will be provided with a question (text only) and a graph type. Your task is to transform this into a **fully structured SAT-style multiple-choice question JSON** as follows:

- Use the provided question and graph type to generate a valid SAT-style visual math question.
- DO NOT reuse existing real SAT questions.
- Ensure the question is **answerable only by looking at the graph** and includes **all data required to reconstruct the graph** in code.
- Provide 4 options (A-D), the exact correct answer text, and detailed feedback explaining the correct answer and why the others are wrong.
- Include `graph_data`: shape type, parameters (like radius, side lengths, center, angle measures), axis labels, and the x/y range of the figure.

You MUST return a list of exactly 10 JSON objects like the format below, without any extra text or markdown:

{
  "content_name": "Problem Solving and Data Analysis",
  "question_type": "Graph",
  "question_choice": "What is the measure of angle ABC in the figure below?",
  "option_a": "30°",
  "option_b": "45°",
  "option_c": "60°",
  "option_d": "90°",
  "answer": "60°",
  "difficulty_level": "Medium",
  "category_type": "Maths",
  "feedback": "The figure shows triangle ABC with an equilateral shape. All angles in an equilateral triangle are 60°. The other options reflect common misconceptions about triangle angles.",
  "graph_data": {
    "type": "triangle",
    "parameters": {
      "side_lengths": [6, 6, 6],
      "angle_measures": [60, 60, 60],
      "vertices": [[0,0], [3,5.2], [6,0]]
    },
    "axis_labels": {"x": "Units", "y": "Units"},
    "x_range": [0, 10],
    "y_range": [0, 10]
  }
}
'''
)


user_prompt = (
    f"""
You are given sample SAT-style questions and their respective graph types.

Generate 10  new questions in the **exact same style** based on {questions}. Each question must rely on analyzing the graph/figure to be solved.

Include 4 choices (A-D), the correct answer, feedback, and full graph data (`type`, `parameters`, `axis_labels`, `x/y ranges`) needed to draw the figure.

Return a JSON array with 10 objects. Follow the JSON format strictly. Do not include any extra explanation or markdown.


Here are the examples:
{examples}




"""
)



generator = ChatOpenAI(
    openai_api_key=os.getenv("API_KEY"),
    model="gpt-4o",
    temperature=0.8
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]


response = generator.invoke(messages)
llm_response=response.content

print(llm_response)
