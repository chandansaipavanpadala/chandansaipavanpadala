#!/usr/bin/env python3
import os
import json
import html
import textwrap

def generate_svg_card(project):
    project_id = project["id"]
    title = html.escape(project["title"])
    subtitle = html.escape(project["subtitle"])
    description = project["description"]
    tags = project["tags"]
    accent_color = project["accent_color"]

    # Card dimensions
    width = 470
    height = 270

    # Wrap description text
    desc_wrapped = textwrap.wrap(description, width=56)
    desc_tspans = []
    for i, line in enumerate(desc_wrapped):
        escaped_line = html.escape(line)
        dy = "0" if i == 0 else "19"
        desc_tspans.append(f'<tspan x="24" dy="{dy}">{escaped_line}</tspan>')
    
    desc_tspans_str = "\n        ".join(desc_tspans)

    # Compute tag positions (wrapping if they exceed width)
    tag_rows = [[]]
    current_x = 24
    max_content_width = width - 24  # 446px limit
    
    # Calculate pill sizes and assign to rows
    for tag in tags:
        # Est. character width is ~6.2px for 11px sans-serif semibold, plus 20px padding (10px each side)
        tag_w = int(len(tag) * 6.2 + 20)
        
        if current_x + tag_w > max_content_width:
            if tag_rows[-1]:  # only wrap if current row is not empty
                tag_rows.append([tag])
                current_x = 24 + tag_w + 8
                continue
        
        tag_rows[-1].append(tag)
        current_x += tag_w + 8

    # Determine Y coordinates for tag rows anchored to the bottom
    num_rows = len(tag_rows)
    if num_rows == 1:
        y_positions = [224]
    elif num_rows == 2:
        y_positions = [194, 224]
    else:
        y_positions = [164, 194, 224]

    tag_elements = []
    for row_idx, row_tags in enumerate(tag_rows):
        if row_idx >= len(y_positions):
            break
        y_pos = y_positions[row_idx]
        x_pos = 24
        for tag in row_tags:
            tag_w = int(len(tag) * 6.2 + 20)
            escaped_tag = html.escape(tag)
            
            # Draw pill background and text
            pill_g = f"""  <g class="tag">
    <rect x="{x_pos}" y="{y_pos}" width="{tag_w}" height="22" rx="11" fill="{accent_color}" fill-opacity="0.12" />
    <text x="{x_pos + tag_w // 2}" y="{y_pos + 15}" fill="{accent_color}" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">{escaped_tag}</text>
  </g>"""
            tag_elements.append(pill_g)
            x_pos += tag_w + 8

    tags_str = "\n".join(tag_elements)

    # SVG template
    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- Glowing background radial gradient -->
    <radialGradient id="bg-glow-{project_id}" cx="0%" cy="0%" r="80%">
      <stop offset="0%" stop-color="{accent_color}" stop-opacity="0.08" />
      <stop offset="50%" stop-color="#0d1117" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="1" />
    </radialGradient>
    
    <!-- Smooth gradient border starting from accent color -->
    <linearGradient id="border-grad-{project_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{accent_color}" stop-opacity="1" />
      <stop offset="30%" stop-color="{accent_color}" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#30363d" stop-opacity="0.2" />
    </linearGradient>
  </defs>

  <!-- Solid card background -->
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="#0d1117" />
  
  <!-- Subtle radial glow overlay -->
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="url(#bg-glow-{project_id})" />
  
  <!-- Gradient border -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="12" fill="none" stroke="url(#border-grad-{project_id})" stroke-width="1.8" />

  <!-- Title -->
  <text x="24" y="38" fill="#f0f6fc" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700">{title}</text>
  
  <!-- Subtitle -->
  <text x="24" y="58" fill="{accent_color}" font-family="system-ui, -apple-system, sans-serif" font-size="12.5" font-weight="600">{subtitle}</text>

  <!-- Wrapped Description -->
  <text x="24" y="86" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="400" line-height="19">
    {desc_tspans_str}
  </text>

  <!-- Project Tech Tags -->
{tags_str}
</svg>"""

    return svg_template

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "projects.json")
    output_dir = os.path.join(script_dir, "project-cards")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Ensured output directory exists at: {output_dir}")
    
    # Read project entries
    with open(json_path, "r", encoding="utf-8") as f:
        projects = json.load(f)
        
    print(f"Loaded {len(projects)} projects from projects.json")
    
    # Generate one SVG per project
    generated_files = []
    for project in projects:
        svg_content = generate_svg_card(project)
        filename = f"{project['id']}.svg"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as sf:
            sf.write(svg_content)
            
        print(f"Generated card: {filepath}")
        generated_files.append(filename)

    # Print markdown snippet to include in README
    print("\n" + "="*40)
    print("MARKDOWN SNIPPET FOR README.md")
    print("="*40)
    markdown_lines = ['<div align="center">']
    
    for idx, project in enumerate(projects):
        if idx > 0 and idx % 2 == 0:
            markdown_lines.append('  <br/><br/>')
            
        col_snippet = f"""  <a href="{project['link']}" target="_blank">
    <img src="./project-cards/{project['id']}.svg" width="49%" alt="{html.escape(project['title'])}"/>
  </a>"""
        markdown_lines.append(col_snippet)
        
    markdown_lines.append('</div>')
    
    snippet = "\n".join(markdown_lines)
    print(snippet)
    print("="*40)

if __name__ == "__main__":
    main()
