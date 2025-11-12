import requests
import re
import pandas as pd
import plotly.graph_objects as go
import os


# --- CONFIG ---
REPO_RAW_URL = "https://raw.githubusercontent.com/piesauce/awesome-dLLM-resources/main/README.md"
OUTPUT_DIR = "graphics"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- FETCH README ---
response = requests.get(REPO_RAW_URL)
response.raise_for_status()
markdown_text = response.text

# --- PARSE CATEGORIES & PAPERS ---
category_pattern = r"## (.+)"
paper_pattern = r"- \*\*(.+?)\*\* — \*(.+?), 2025\*"

categories = re.findall(category_pattern, markdown_text)
papers = re.findall(paper_pattern, markdown_text)

# Map papers to categories
category_papers = {cat: [] for cat in categories}

# Split markdown into sections by categories
sections = re.split(r"(## .+)", markdown_text)
for i in range(1, len(sections), 2):
    cat = sections[i].replace("## ", "").strip()
    paper_lines = sections[i+1].splitlines()
    count = sum(1 for line in paper_lines if line.startswith("- **"))
    category_papers[cat] = count

# --- RADAR CHART ---
labels = list(category_papers.keys())
values = list(category_papers.values())

fig = go.Figure(
    data=[
        go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name='Papers per Category'
        )
    ],
    layout=go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values)+1],
                showticklabels=False,
                showline=False, 
                showgrid=True,
            ),
            angularaxis=dict(
                rotation=90,
                direction="clockwise"
            )
        ),
        showlegend=False,
    )
)

output_path = os.path.join(OUTPUT_DIR, "papers_by_category_radar.png")
fig.write_image(output_path)
print(f"Radar chart saved to {output_path}")