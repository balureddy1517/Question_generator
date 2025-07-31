import base64
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import base64



load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def image_generation(question,graph_data,n):

    prompt = f"""
        You are an image generator assistant responsible for creating accurate, SAT-style math figures based on provided data.

        You will be given:
        → A **math question** that relies on a visual diagram to be solved.  
        → Corresponding **graph_data**, which includes all necessary details to render the figure (e.g., shape type, coordinates, side lengths, angles, radius, axis labels, etc.).

        ---

        🎯 **Your Objectives**:

        1. Carefully **analyze the question and graph_data**.
        2. Generate a **precise and visually clear diagram** that matches both the question and the graph_data.
        3. Ensure the **diagram includes all relevant information needed to answer the question**, but **does NOT reveal the answer directly** (e.g., do not label an angle that the question is asking to find).

        ---

        ✅ **Diagram Requirements**:
        - Clearly **label key points** (e.g., A, B, C), angles, lines, radius, or dimensions *as described in the graph_data*.
        - If a radius, side, or angle is referenced in the question or graph_data, it should be **visibly labeled in the figure** (e.g., "radius = 3").
        - Use **axis labels and proper scaling** to clearly show coordinates and allow easy interpretation. Avoid cluttered or misleading axes.
        - Use common geometric markers:  
        - Right-angle square marks  
        - Tick marks for congruent sides  
        - Dashed lines for construction lines  
        - Make the diagram **readable and unambiguous** for students.

        ---

        🔍 **Final Check**:
        - Before generating the image, ask yourself:  
        **“Can this question be answered correctly and confidently by only looking at the figure?”**  
        - If **any critical label or value is missing**, or if the axis makes it hard to read coordinates, **fix it** or **flag it as incomplete**.

        ---

        **Question**:  
        {question}

        ---

        **Graph Data**:  
        {graph_data}
                """
    
    response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt,
    tools=[{"type": "image_generation"}],
)
    
    image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

    os.makedirs('geo_tri_graphs',exist_ok=True)   
    image_path=f'geo_tri_graphs/'+f'{n}.png'
    if image_data:
        image_base64 = image_data[0]
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image_base64))
    

with open('generated_json/Geometry_Trigonometry.json', 'r') as file:
        data=json.load(file)

for i, item in enumerate(data):
    item["image_number"] = f'{i}.png'
    image_generation(item["question_choice"],item["graph_data"], i)


filtered_data = []
for item in data:
    # Make a copy without the "graph_data" key
    item_copy = {key: value for key, value in item.items() if key != "graph_data"}
    filtered_data.append(item_copy)

with open('generated_json/Geometry_Trigonometry_Final.json', 'w') as file:
    json.dump(filtered_data, file, indent=4)