#!/usr/bin/env python3
import os
import sys
import random

# Reconfigure stdout to use UTF-8 to prevent encoding errors on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def build_banner():
    width = 1200
    height = 250
    
    # Glow filter and animated gradient mesh definitions
    defs = """  <defs>
    <!-- Glow filter for pulsing text shadow -->
    <filter id="text-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Animated gradient mesh components -->
    <radialGradient id="mesh-left" cx="20%" cy="30%" r="60%">
      <stop offset="0%" stop-color="#0077b6">
        <animate attributeName="stop-color" values="#0077b6;#00b4d8;#0d1117;#0077b6" dur="14s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </radialGradient>

    <radialGradient id="mesh-right" cx="80%" cy="70%" r="60%">
      <stop offset="0%" stop-color="#00b4d8">
        <animate attributeName="stop-color" values="#00b4d8;#0d1117;#0077b6;#00b4d8" dur="18s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </radialGradient>

    <radialGradient id="mesh-center" cx="50%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#0d1117">
        <animate attributeName="stop-color" values="#0d1117;#0077b6;#00b4d8;#0d1117" dur="22s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </radialGradient>
  </defs>"""

    # Generate 25 animated drifting background particles using animateMotion
    random.seed(101)  # Seed for deterministic generation
    particles_list = []
    
    for i in range(25):
        cx = random.randint(30, 1170)
        cy = random.randint(20, 230)
        r = round(random.uniform(0.8, 2.2), 1)
        
        # Drift offsets for animateMotion path (relative cubic bezier curve loop)
        dx1 = random.randint(-40, 40)
        dy1 = random.randint(-30, 30)
        dx2 = random.randint(-40, 40)
        dy2 = random.randint(-30, 30)
        dx3 = random.randint(-40, 40)
        dy3 = random.randint(-30, 30)
        
        # Closed curve path starting and ending at local origin 0,0
        path_str = f"M 0 0 C {dx1} {dy1}, {dx2} {dy2}, {dx3} {dy3} Z"
        dur = random.randint(15, 35)  # Drift slowly
        
        # Opacity breathing values
        min_op = round(random.uniform(0.08, 0.2), 2)
        max_op = round(random.uniform(0.4, 0.65), 2)
        op_vals = f"{min_op};{max_op};{min_op}"
        op_dur = random.randint(6, 12)
        
        particle_xml = f"""  <circle cx="{cx}" cy="{cy}" r="{r}" fill="#00b4d8">
    <animateMotion path="{path_str}" dur="{dur}s" repeatCount="indefinite" />
    <animate attributeName="opacity" values="{op_vals}" dur="{op_dur}s" repeatCount="indefinite" />
  </circle>"""
        particles_list.append(particle_xml)
        
    particles_str = "\n".join(particles_list)

    # SVG Template
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
{defs}

  <!-- Base background color -->
  <rect width="{width}" height="{height}" fill="#0d1117" />

  <!-- Overlapping animated gradient mesh layers -->
  <rect width="{width}" height="{height}" fill="url(#mesh-left)" />
  <rect width="{width}" height="{height}" fill="url(#mesh-right)" />
  <rect width="{width}" height="{height}" fill="url(#mesh-center)" />

  <!-- Animated background particles -->
{particles_str}

  <!-- Header Text Group -->
  <g id="header-text">
    <!-- Pulsing glow backdrop behind the name -->
    <text x="600" y="112" fill="#00b4d8" font-family="system-ui, -apple-system, sans-serif" font-size="48" font-weight="800" text-anchor="middle" filter="url(#text-glow)">
      <animate attributeName="opacity" values="0.3;0.8;0.3" dur="6s" repeatCount="indefinite" />
      Chandan Sai Pavan Padala
    </text>
    
    <!-- Main foreground name -->
    <text x="600" y="112" fill="#ffffff" font-family="system-ui, -apple-system, sans-serif" font-size="48" font-weight="800" text-anchor="middle">
      Chandan Sai Pavan Padala
    </text>

    <!-- Subtitle tagline -->
    <text x="600" y="156" fill="#00b4d8" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="600" text-anchor="middle" style="letter-spacing: 2px;">
      <animate attributeName="opacity" values="0.85;1.0;0.85" dur="8s" repeatCount="indefinite" />
      Embedded Systems | RTOS | Firmware | Defence Tech
    </text>
  </g>
</svg>"""

    return svg_content

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "banner.svg")
    
    print("Generating animated SVG header banner...")
    banner_content = build_banner()
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(banner_content)
        
    print(f"Successfully generated animated banner: {output_path}")

if __name__ == "__main__":
    main()
