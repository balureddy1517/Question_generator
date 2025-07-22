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



system_prompt=(
    '''
You are a highly accurate SAT question extractor from images.

You will be given one or more images that contain SAT math questions with accompanying figures or graphs. These images include:

- The question text
- Four multiple-choice options (A–D)
- A diagram or graph embedded alongside the question

Your task is to **extract** the full question, all options, and relevant figure/graph information **exactly as shown in the image**, and return them in **structured JSON format**.

Each extracted question must include:
- The full question text (as it appears)
- Four answer options (A–D)
- Any visible labels, values, or attributes from the figure
- A structured JSON describing the **graph or diagram** with shape type and parameters

 Do not make up or paraphrase. Extract only what is visible and clearly interpretable from the image.

Use this exact JSON format for each extracted question:

```json
{
  "question_text": "Full question text as shown in the image",
  "option_a": "Option A",
  "option_b": "Option B",
  "option_c": "Option C",
  "option_d": "Option D",
  "graph_data": {
    "type": "circle | rectangle | square | prism | cylinder | cone | triangle | bar_chart | line_graph | scatter_plot | other",
    "parameters": {
      "radius": 5,
      "center": [0, 0],
      "side_lengths": [4, 6],
      "height": 10,
      "angle_measures": [90, 45, 45],
      "labels": ["A", "B", "C", "D"]
    },
    "axis_labels": {"x": "Time (s)", "y": "Distance (m)"},
    "x_range": [0, 10],
    "y_range": [0, 100],
    "additional_info": "Any other visual elements or annotations in the figure"
  }
}

    '''

)


user_prompt=(
    '''
Please extract all SAT math questions from the image(s) provided.

Each image contains a question, four options (A - 


D), and a figure or graph.

Your task is to extract the question, options, and all data from the accompanying figure, and return everything in the exact JSON format defined above.

Only extract what is visible in the image. Do not add or infer missing data.

Return your answer as a single JSON array containing all extracted questions.
    '''
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
    temperature=0
)
print(response.choices[0].message.content)