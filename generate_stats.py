#!/usr/bin/env python3
import os
import sys

# Reconfigure stdout to use UTF-8 to prevent encoding errors on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def build_stats_card():
    # Placeholder values for GitHub stats (user can easily edit these)
    stats = {
        "total_stars": "18",
        "total_commits": "824",
        "prs": "47",
        "issues": "12",
        "contributed_to": "15"
    }

    width = 600
    height = 330

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- Soft drop shadow for the glass panel -->
    <filter id="panel-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000000" flood-opacity="0.65" />
    </filter>

    <!-- Backdrop blur filter for the glass panel -->
    <filter id="backdrop-blur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="15" result="blur" />
      <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1.2 0" />
    </filter>

    <!-- Radial gradients for background glassmorphism glowing orbs -->
    <radialGradient id="glow-cyan" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00b4d8" stop-opacity="0.22" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="glow-blue" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0077b6" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </radialGradient>

    <!-- Border highlight linear gradient -->
    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00b4d8" stop-opacity="0.45" />
      <stop offset="30%" stop-color="#0077b6" stop-opacity="0.1" />
      <stop offset="70%" stop-color="#00b4d8" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#0077b6" stop-opacity="0.45" />
    </linearGradient>

    <!-- Text fill gradient -->
    <linearGradient id="text-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="100%" stop-color="#00b4d8" />
    </linearGradient>
    
    <!-- Mask for matching the blurred elements to the glass panel bounds -->
    <mask id="panel-mask">
      <rect x="30" y="30" width="540" height="270" rx="16" fill="#ffffff" />
    </mask>
  </defs>

  <!-- Base background card -->
  <rect width="{width}" height="{height}" fill="#0d1117" rx="20" />

  <!-- Colorful background orbs underneath the glass panel -->
  <g id="bg-glows">
    <circle cx="150" cy="120" r="140" fill="url(#glow-cyan)" />
    <circle cx="450" cy="220" r="130" fill="url(#glow-blue)" />
  </g>

  <!-- Blurred backdrop layer (masked to glass panel boundaries) -->
  <g mask="url(#panel-mask)">
    <use href="#bg-glows" filter="url(#backdrop-blur)" />
  </g>

  <!-- Glass panel rectangle (tinted face, border, drop shadow) -->
  <rect x="30" y="30" width="540" height="270" rx="16" 
        fill="#ffffff" fill-opacity="0.02" 
        stroke="url(#border-grad)" stroke-width="1.5" 
        filter="url(#panel-shadow)" />

  <!-- Card Header -->
  <g id="header" transform="translate(0, 0)">
    <!-- Terminal CLI Prompt Icon -->
    <path d="M 54 54 L 60 59 L 54 64 M 63 64 L 71 64" stroke="#00b4d8" stroke-width="2" stroke-linecap="round" fill="none" />
    <!-- Title Text -->
    <text x="82" y="64" fill="#00b4d8" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="700" letter-spacing="2px">GITHUB ANALYTICS</text>
    
    <!-- Live pulsing status dot -->
    <circle cx="540" cy="60" r="4" fill="none" stroke="#00b4d8" stroke-width="1.5">
      <animate attributeName="r" values="4;8;4" dur="3s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.8;0;0.8" dur="3s" repeatCount="indefinite" />
    </circle>
    <circle cx="540" cy="60" r="4" fill="#00b4d8" />
  </g>

  <!-- Grid Dividers (Low Opacity) -->
  <g id="grid-dividers" stroke="#ffffff" stroke-opacity="0.08" stroke-width="1">
    <!-- Horizontal row separator -->
    <line x1="50" y1="175" x2="550" y2="175" />
    <!-- Row 1 vertical column separators -->
    <line x1="210" y1="95" x2="210" y2="160" />
    <line x1="390" y1="95" x2="390" y2="160" />
    <!-- Row 2 vertical column separator -->
    <line x1="300" y1="190" x2="300" y2="255" />
  </g>

  <!-- Stats Grid Texts -->
  <!-- ROW 1 -->
  <!-- Stars -->
  <g transform="translate(120, 0)">
    <text x="0" y="132" fill="url(#text-grad)" font-family="system-ui, -apple-system, sans-serif" font-size="34" font-weight="800" text-anchor="middle">{stats['total_stars']}</text>
    <text x="0" y="154" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle" letter-spacing="1px">TOTAL STARS</text>
  </g>

  <!-- Commits -->
  <g transform="translate(300, 0)">
    <text x="0" y="132" fill="url(#text-grad)" font-family="system-ui, -apple-system, sans-serif" font-size="34" font-weight="800" text-anchor="middle">{stats['total_commits']}</text>
    <text x="0" y="154" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle" letter-spacing="1px">TOTAL COMMITS</text>
  </g>

  <!-- PRs -->
  <g transform="translate(480, 0)">
    <text x="0" y="132" fill="url(#text-grad)" font-family="system-ui, -apple-system, sans-serif" font-size="34" font-weight="800" text-anchor="middle">{stats['prs']}</text>
    <text x="0" y="154" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle" letter-spacing="1px">PULL REQUESTS</text>
  </g>

  <!-- ROW 2 -->
  <!-- Issues -->
  <g transform="translate(165, 0)">
    <text x="0" y="227" fill="url(#text-grad)" font-family="system-ui, -apple-system, sans-serif" font-size="34" font-weight="800" text-anchor="middle">{stats['issues']}</text>
    <text x="0" y="249" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle" letter-spacing="1px">ISSUES</text>
  </g>

  <!-- Contributed To -->
  <g transform="translate(435, 0)">
    <text x="0" y="227" fill="url(#text-grad)" font-family="system-ui, -apple-system, sans-serif" font-size="34" font-weight="800" text-anchor="middle">{stats['contributed_to']}</text>
    <text x="0" y="249" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle" letter-spacing="1px">CONTRIBUTED TO</text>
  </g>

</svg>"""

    return svg_content

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "glass-stats.svg")
    
    print("Generating glassmorphism GitHub stats card...")
    stats_content = build_stats_card()
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(stats_content)
        
    print(f"Successfully generated glass stats card: {output_path}")

if __name__ == "__main__":
    main()
