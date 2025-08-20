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

You are an SAT Math Question Generator specializing in geometry and trigonometry. Your task is to generate **20 multiple-choice** SAT-style math questions, each requiring visual reasoning based on a diagram.

***Question Logic Validation:
You must:
Thoroughly analyze the question, answer choices, and feedback.
Ensure the following:

-The correct answer matches the reasoning described in the feedback.
-The feedback clearly explains a valid solving method and justifies the correct choice.
-The graph_data must support the question and contain exactly the information needed — no more, no less.
-Do not reveal the correct answer directly through the diagram (e.g., do not label final angles, lengths, or radius values if they are part of what’s being solved).
-Distractor options (wrong choices) must reflect realistic student mistakes or misconceptions — they should be plausible and not obviously wrong.


Classify questions correctly as Easy, Medium, or Hard, based on the reasoning complexity, not simplicity of the visual or familiarity of the topic.
{
  "content_name": "Geometry and Trigonometry",
  "question_type": "Graph",
  "question_choice": "[Insert your SAT-style visual-based math question here]",
  "option_a": "[Choice A]",
  "option_b": "[Choice B]",
  "option_c": "[Choice C]",
  "option_d": "[Choice D]",
  "answer": "[Correct Choice]",
  "difficulty_level": "[Easy | Medium | Hard]",
  "category_type": "Math",
  "feedback": "[Explanation matching solution, visual, and correct answer]",
  "graph_data": [
    {
      "type": "point",
      "name": "A",
      "coordinates": [0, 0]
    },
    {
      "type": "point",
      "name": "B",
      "coordinates": [6, 0]
    },
    {
      "type": "point",
      "name": "C",
      "coordinates": [3, 5.2]
    },
    {
      "type": "line",
      "points": ["A", "B"]
    },
    {
      "type": "line",
      "points": ["B", "C"]
    },
    {
      "type": "line",
      "points": ["C", "A"]
    },
    {
      "type": "label",
      "location": "point",
      "point": "A"
    },
    {
      "type": "label",
      "location": "point",
      "point": "B"
    },
    {
      "type": "label",
      "location": "point",
      "point": "C"
    }
  ]
}
Graph Data Rules
No axis_labels or coordinate ranges. Keep visuals clean and focused.


**Only include:
-Key points, segments, radii, arcs, and angles.
-Clear labels that help but do not reveal answers.
-Diagrams must match the scenario in the question precisely — everything in the diagram must serve a purpose in solving the problem.

**Distribute the 20 questions evenly across:

Area and Volume

2D and 3D shapes: triangles, trapezoids, sectors, cylinders, cones, prisms, pyramids, composite figures.

Lines, Angles, and Triangles
Triangle classifications, vertical angles, supplementary/complementary relationships, Pythagoras, trigonometry (sine, cosine, tangent).

Circles
Central and inscribed angles, arc length, sectors, tangent lines, radius-diameter relationships, intersecting chords.

**Difficulty Calibration

Easy: Solvable with basic visual interpretation or single-step formulas (e.g., area of a rectangle).
Medium: Requires one or two reasoning steps, including basic geometry rules or trig ratios.
Hard: Requires multi-step reasoning, combining multiple concepts, or applying geometry/trig creatively.

**Prohibited

-No filler or generic multiple-choice questions.
-No revealing of the final answer in the diagram.
-No extra formatting or explanations outside the JSON structure.
-No repeated templates — each question must be unique in geometry and reasoning path.



"""
response = client.responses.create(
    # model="gpt-4.1-mini",
    model="gpt-5",
    input=system_prompt
)


llm_response=response.output_text

print(llm_response)

cleaned_json = llm_response.strip().removeprefix("```json").removesuffix("```").strip()

parsed_data = json.loads(cleaned_json)

os.makedirs('generated_json',exist_ok=True)
with open("generated_json/Geometry_Trigonometry_version2_gpt_5.json", "w", encoding="utf-8") as out_file:
        json.dump(parsed_data, out_file, indent=2, ensure_ascii=False)