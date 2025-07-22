import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

base64_image = encode_image("pdf_images/samplepdfimage-1.jpg")

image_paths=[]

dir='pdf_images'
images=os.listdir(dir)
for image in images:
    path=os.path.join(dir,image)
    print(path)
    image_paths.append(path)

print(image_paths)

image_blocks = [
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(path)}"}}
    for path in image_paths
]

# general_math_image_prompt = '''
# You are a SAT Math Question Generator.

# Your job is to analyze **images of SAT math problems** that may contain **figures, graphs, diagrams, or mathematical content**, and generate a new multiple-choice question based on the information.

# Instructions:
# - Use the image to create a **new math multiple-choice question** similar to what might appear in the SAT exam.
# - The question should be **figure-based**, meaning the visual content (graph, shape, diagram) is important to the question.
# - The question must be answerable based on the **image content**, not from guesswork.
# - Generate 4 answer choices: A, B, C, and D.
# - Provide the **correct answer** explicitly.
# - Provide **clear feedback/explanation** for the correct answer.
# - Return the output as a JSON object in the exact format below.

# Output format (strictly return JSON):
# {
#   "content_name": "Problem Solving and Data Analysis | Geometry | Algebra | etc.",
#   "question_type": "Graph | Geometry | Word Problem | etc.",
#   "question_choice": "Text of the question here...",
#   "option_a": "Option A",
#   "option_b": "Option B",
#   "option_c": "Option C",
#   "option_d": "Option D",
#   "answer": "exact text of correct option",
#   "difficulty_level": "Easy | Medium | Hard",
#   "category_type": "Maths",
#   "feedback": "Explanation of answer including reasoning",
#   "figure_analysis": "Brief description of what’s in the image: graph, equation, labels, coordinates, etc."
# }
# '''


# general_math_user_prompt = '''
# You will receive an image from an SAT math worksheet or book.

# Use the image to generate a **10 new questions** that:
# - Is inspired by the content shown in the image (e.g., graph, diagram, shapes, equations)
# - Tests understanding of the concepts present in the image
# - Is of SAT-level quality and difficulty
# - Is clear and answerable based only on the image

# Return your result as a single **JSON object**, with no explanation outside of the JSON.

# Begin analyzing the image now.
# '''


# response = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "Generate a few SAT-style questions based on this image."
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{base64_image}"
#                     }
#                 }
#             ]
#         }
#     ],
# )
system_prompt = ('''
   
You are a SAT math question generator expert.

You will receive one or more images containing SAT graph-based math questions related to **geometry** (e.g., circles, quadrilaterals, and volume figures).

Your task is to generate **10 brand new, original multiple-choice questions** inspired by those images.

- Each question must be **answerable only by looking at the graph or figure**.
- Do NOT reuse or copy the original questions or answers.
- Questions must involve **geometry-based visual reasoning** such as interpreting circle properties, angles in quadrilaterals, or 3D volume dimensions.
- Each question must include the **full data needed to reconstruct the figure or graph exactly** (e.g., radius, center, side lengths, volume parameters, axis labels, angle measures).
- Questions must refer explicitly to the figure and require interpreting it.
- Provide four answer choices (A–D), the exact correct answer text, detailed feedback, difficulty level, and category.
- Return all 10 questions as a JSON array without any extra text or explanation.

Use this exact JSON format for each question:

{
  "content_name": "Problem Solving and Data Analysis",
  "question_type": "Graph",
  "question_choice": "Question text referring to the figure or diagram",
  "option_a": "Option A",
  "option_b": "Option B",
  "option_c": "Option C",
  "option_d": "Option D",
  "answer": "Exact correct answer option text",
  "difficulty_level": "Easy | Medium | Hard",
  "category_type": "Maths",
  "feedback": "Detailed explanation about why the correct answer is right and why others are wrong",
  "graph_data": {
    "type": "circle | rectangle | square | prism | cylinder | cone",
    "parameters": {
      "radius": 5,
      "center": [0, 0],
      "side_lengths": [4, 6],
      "height": 10,
      "angle_measures": [90, 45, 45]
    },
    "axis_labels": {"x": "Units", "y": "Units"},
    "x_range": [min_x, max_x],
    "y_range": [min_y, max_y]
  }
}


                 '''

)

# User prompt
user_prompt = (
   """
You are given one or more images containing SAT math questions involving graphs.

Based on these images, generate 10 **new** SAT math questions as per the system prompt above.

Questions must require analyzing the graph to answer, and must provide full data to redraw the graph programmatically.

Return the output as a JSON array.


"""
)


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [
            {"type": "text", "text": user_prompt},
            *image_blocks  # Unpack all image blocks here
        ]}
    ],
    temperature=0.8
)

print(response.choices[0].message.content)
