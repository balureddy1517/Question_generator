
import numpy as np
import matplotlib.pyplot as plt
import json
from dotenv import load_dotenv
import os
import re

load_dotenv()


def parse_equation(equation_str):
    """
    Parses equations like 'y = -2(x - 3)^2 + 4' or 'y = x^2 - 4x + 5'
    and returns a lambda function f(x) that computes y.
    """
    eq = equation_str.replace("^", "**").replace("y =", "").strip()

    # Insert * between number and parenthesis: -2(x - 3) => -2*(x - 3)
    eq = re.sub(r'(\d)(\()', r'\1*(', eq)           # 2(x+1) → 2*(x+1)
    eq = re.sub(r'(-)(\d)(\()', r'-\2*(', eq)       # -2(x+1) → -2*(x+1)
    eq = re.sub(r'(\))(\()', r')*(', eq)            # )( → )*(
    eq = re.sub(r'(\d)x', r'\1*x', eq)              # 2x → 2*x
    eq = re.sub(r'x(\()', r'x*(', eq)               # x(x+1) → x*(x+1)

    def f(x):
        return eval(eq, {}, {"x": x})
    return f



def extract_float_tuple(coord_str):
    # Input like "(2, 1)" => (2.0, 1.0)
    return tuple(map(float, re.findall(r"-?\d+\.?\d*", coord_str)))




def plot_question(question_data, idx):

    os.makedirs(os.getenv("QUAD_GRAPH_DIR"),exist_ok=True)
    eq_str = question_data["equation"]
    features = question_data["key_features"]
    question_text = question_data["question_choice"]

    vertex = extract_float_tuple(features["vertex"])
    axis = float(features["axis_of_symmetry"].split('=')[1].strip())
    x_intercepts = list(map(float, features["x_intercepts"])) if features["x_intercepts"] else []
    y_intercept = float(features["y_intercept"])

    f = parse_equation(eq_str)

    x_vals = np.linspace(vertex[0] - 10, vertex[0] + 10, 400)
    y_vals = [f(x) for x in x_vals]

    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_vals, label=eq_str)
    plt.axvline(x=axis, color='gray', linestyle='--', label="Axis of Symmetry")
    plt.plot(vertex[0], vertex[1], 'ro', label='Vertex')
    plt.plot(0, y_intercept, 'go', label='Y-Intercept')

    for xi in x_intercepts:
        plt.plot(xi, 0, 'bx', label='X-Intercept')

    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.title(f"Q{idx+1}: {question_text}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    # plt.show()
    graph_path=os.path.join(os.path.join(os.getcwd(),os.getenv("QUAD_GRAPH_DIR")),f"graph_question_{idx+1}")
    plt.savefig(graph_path)









questionjson_path=os.getenv("QUAD_QUESTION_JSON")

with open(questionjson_path, 'r') as file:
        data=json.load(file)


for idx, q in enumerate(data):
    print(idx)
    plot_question(q, idx)