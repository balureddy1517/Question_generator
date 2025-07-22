

import matplotlib.pyplot as plt
import numpy as np
import json
import os

def draw_graph(graph_data, index):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Set axis limits
    x_min, x_max = graph_data.get("x_range", [-10, 10])
    y_min, y_max = graph_data.get("y_range", [-10, 10])
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Label axes
    axis_labels = graph_data.get("axis_labels", {})
    ax.set_xlabel(axis_labels.get("x", "x"))
    ax.set_ylabel(axis_labels.get("y", "y"))

    gtype = graph_data["type"]
    params = graph_data["parameters"]


    # Draw based on graph type
    if gtype == "circle":
        radius = params["radius"]
        center = params["center"]
        angles = graph_data["parameters"].get("angle_measures", [])
        circle = plt.Circle(center, radius, fill=False, edgecolor='blue', linewidth=2)
        ax.add_patch(circle)
        ax.plot(center[0], center[1], 'ro') 
        radius_endpoint = [center[0] + radius, center[1]]  # horizontal radius line for simplicity
        ax.plot([center[0], radius_endpoint[0]], [center[1], radius_endpoint[1]], 'g--', label='Radius')
        if angles:
            theta = np.radians(angles[0])  # Convert angle to radians
            t = np.linspace(0, theta, 100)
            
            # Generate arc points for the sector
            arc_x = center[0] + radius * np.cos(t)
            arc_y = center[1] + radius * np.sin(t)
            
            # Add sector wedge
            sector_x = np.concatenate([[center[0]], arc_x, [center[0]]])
            sector_y = np.concatenate([[center[1]], arc_y, [center[1]]])
            ax.fill(sector_x, sector_y, color='orange', alpha=0.4, label=f'Sector {angles[0]}°')

            # Draw radius lines for the sector
            ax.plot([center[0], center[0] + radius], [center[1], center[1]], 'g--')  # 0°
            ax.plot([center[0], center[0] + radius * np.cos(theta)], [center[1], center[1] + radius * np.sin(theta)], 'g--')



    elif gtype in ["square", "rectangle"]:
        side_lengths = params["side_lengths"]
        x0, y0 = params.get("bottom_left", [0, 0])
        width, height = side_lengths
        rect = plt.Rectangle((x0, y0), width, height, fill=False, edgecolor='green', linewidth=2)
        ax.add_patch(rect)

    elif gtype == "triangle":
        points = params["points"]
        polygon = plt.Polygon(points, fill=False, edgecolor='purple', linewidth=2)
        ax.add_patch(polygon)

    elif gtype in ["prism", "cylinder", "cone"]:
        # Show as 2D projection (height + base)
        radius = params.get("radius", 1)
        height = params.get("height", 2)
        base_center = params.get("center", [0, 0])

        # Draw base as circle
        base = plt.Circle(base_center, radius, fill=False, edgecolor='orange', linestyle='--')
        ax.add_patch(base)

        # Draw height line (vertical)
        x0, y0 = base_center
        ax.plot([x0, x0], [y0, y0 + height], color='orange', linestyle='-', linewidth=2)

    else:
        print(f"Unsupported type: {gtype}")

    ax.set_title(f"Graph {index+1}: {gtype}")
    plt.grid(True)
    # plt.show()
    cir_graph_dir="circle_graphs"
    os.makedirs(cir_graph_dir,exist_ok=True)
    path = os.path.join(cir_graph_dir, f'graph-{index + 1}.png')
    plt.savefig(path, bbox_inches='tight') 
    plt.close() 


with open('circle_questions.json', 'r') as file:
        data=json.load(file)

for i, item in enumerate(data):
    draw_graph(item["graph_data"], i)








        