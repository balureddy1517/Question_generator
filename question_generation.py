from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
)




system_prompt="""
You are an SAT Math Question Generator specialized in geometry and trigonometry. Your task is to generate 20 multiple-choice SAT-style math questions, each focused on figure-based reasoning, where the question must be answerable by analyzing the provided diagram only.
Each question must relate to one of the following topics:
Area and volume


Lines, angles, and triangles (including right triangles and trigonometry)


Circles


For each question, return a structured JSON object with the following constraints and format:
**Requirements**
The question must require interpreting a diagram (not answerable without the visual).


Do not include any direct answer (like angle values or lengths that are the answer) in the diagram.


Use various figure types: triangles, circles, quadrilaterals, 3D shapes (for volume), composite shapes, and trigonometric setups.


Each diagram should include all data necessary to reconstruct it (e.g., side lengths, coordinates, radius, angles, labels).


Do not include extra text, explanations, or formatting outside of JSON.
{
  "content_name": "Geometry and Trigonometry",
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
    "axis_labels": {
      "x": "Units",
      "y": "Units"
    },
    "x_range": [0, 10],
    "y_range": [0, 10]
  }
}



"""
response = client.responses.create(
    model="gpt-4.1-mini",
    input=system_prompt
)


llm_response=response.output_text

print(llm_response)

cleaned_json = llm_response.strip().removeprefix("```json").removesuffix("```").strip()

parsed_data = json.loads(cleaned_json)

os.makedirs('generated_json',exist_ok=True)
with open("generated_json/Geometry_Trigonometry.json", "w", encoding="utf-8") as out_file:
        json.dump(parsed_data, out_file, indent=2, ensure_ascii=False)