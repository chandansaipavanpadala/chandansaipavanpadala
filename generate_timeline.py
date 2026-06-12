#!/usr/bin/env python3
import os
import sys
import html

# Reconfigure stdout to use UTF-8 to prevent encoding errors on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def generate_timeline():
    # SVG Dimensions
    width = 980
    height = 180
    
    # Milestone positions: 6 nodes from X=80 to X=900
    milestones = [
        {"x": 80,  "label": "Arduino & C",       "caption": "Basics & Hardware I/O"},
        {"x": 244, "label": "ARM7 LPC2148",      "caption": "Embedded C Drivers"},
        {"x": 408, "label": "ESP32 & FreeRTOS",   "caption": "Multi-tasking & IoT"},
        {"x": 572, "label": "STM32 / Cortex-M4", "caption": "DMA & Industrial Controls"},
        {"x": 736, "label": "Raspberry Pi",      "caption": "Robotics & ADAS"},
        {"x": 900, "label": "Defence Systems",   "caption": "Mission-Critical RTOS"}
    ]
    
    # Build milestone elements
    nodes_svg = []
    for m in milestones:
        x = m["x"]
        label = html.escape(m["label"])
        caption = html.escape(m["caption"])
        
        node_group = f"""  <!-- Milestone: {label} -->
  <g class="milestone-node">
    <!-- Glow effect simulated by concentric circles -->
    <circle cx="{x}" cy="95" r="14" fill="#00b4d8" fill-opacity="0.12" />
    <circle cx="{x}" cy="95" r="8" fill="#0d1117" stroke="#00b4d8" stroke-width="2.2" />
    <circle cx="{x}" cy="95" r="4.5" fill="#00b4d8" />
    
    <!-- Title Label (Above node) -->
    <text x="{x}" y="62" fill="#f0f6fc" font-family="system-ui, -apple-system, sans-serif" font-size="12.5" font-weight="700" text-anchor="middle">{label}</text>
    
    <!-- Subtitle Caption (Below node) -->
    <text x="{x}" y="132" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="10.5" font-weight="400" text-anchor="middle">{caption}</text>
  </g>"""
        nodes_svg.append(node_group)
        
    nodes_str = "\n".join(nodes_svg)

    # SVG Template
    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- Horizontal connector line gradient -->
    <linearGradient id="line-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#30363d" stop-opacity="0.3" />
      <stop offset="15%" stop-color="#00b4d8" stop-opacity="0.9" />
      <stop offset="85%" stop-color="#00b4d8" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#30363d" stop-opacity="0.3" />
    </linearGradient>
    
    <!-- Card border gradient -->
    <linearGradient id="border-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00b4d8" stop-opacity="0.8" />
      <stop offset="40%" stop-color="#00b4d8" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#30363d" stop-opacity="0.2" />
    </linearGradient>
  </defs>

  <!-- Solid card background -->
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="#0d1117" />
  
  <!-- Subtle card border -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="12" fill="none" stroke="url(#border-gradient)" stroke-width="1.5" />

  <!-- Horizontal connector line -->
  <line x1="60" y1="95" x2="920" y2="95" stroke="url(#line-gradient)" stroke-width="2.5" />

  <!-- Milestones and Nodes -->
{nodes_str}
</svg>"""

    return svg_template

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "skills-timeline.svg")
    
    print("Generating skills timeline SVG...")
    svg_content = generate_timeline()
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print(f"Successfully generated timeline: {output_path}")

if __name__ == "__main__":
    main()
