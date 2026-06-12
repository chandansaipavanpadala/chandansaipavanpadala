#!/usr/bin/env python3
import os
import sys

# Reconfigure stdout to use UTF-8 to prevent encoding errors on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def build_terminal_svg():
    width = 600
    height = 300
    
    # Timing variables (total loop duration D = 10s)
    D = 10.0
    t_reset = 8.5
    
    # Helper to generate character-by-character animation
    def make_char_xml(char, t_appear, fill_color=None):
        kt_appear = t_appear / D
        kt_reset = t_reset / D
        fill_attr = f' fill="{fill_color}"' if fill_color else ''
        # Looping animate: invisible -> visible at t_appear -> invisible at t_reset
        return f'<tspan opacity="0"{fill_attr}>{char}<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{kt_appear:.3f};{kt_appear+0.005:.3f};{kt_reset:.3f};1" dur="{D}s" repeatCount="indefinite" /></tspan>'

    # Helper to generate instant line appearance
    def make_instant_line_xml(text_content, t_appear, fill_color="#ffffff", is_prompt=False):
        kt_appear = t_appear / D
        kt_reset = t_reset / D
        # If it is a prompt, highlight the first two characters ($ ) in cyan
        if is_prompt and text_content.startswith("$ "):
            prompt_part = f'<tspan fill="#00b4d8" font-weight="bold">$ </tspan>'
            text_part = text_content[2:]
            text_body = f'{prompt_part}<tspan fill="{fill_color}">{text_part}</tspan>'
        else:
            text_body = f'<tspan fill="{fill_color}">{text_content}</tspan>'
            
        return f'<g opacity="0">{text_body}<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{kt_appear:.3f};{kt_appear+0.005:.3f};{kt_reset:.3f};1" dur="{D}s" repeatCount="indefinite" /></g>'

    # Generate Line 1: $ whoami
    line1_text = "$ whoami"
    line1_xml = []
    # Prompt "$ " appears at 0.2s
    line1_xml.append(make_char_xml("$", 0.2, "#00b4d8"))
    line1_xml.append(make_char_xml(" ", 0.3, "#00b4d8"))
    # Command types at 0.1s intervals
    for idx, char in enumerate("whoami"):
        line1_xml.append(make_char_xml(char, 0.4 + idx * 0.1))
    line1_str = "".join(line1_xml)

    # Cursor 1 (Blinks on Line 1 from t=0.2s to t=1.1s, then disappears)
    # Blinks: 0.2s (on), 0.5s (off), 0.8s (on), 1.1s (off/freeze)
    cursor1_xml = f"""<tspan fill="#00b4d8" opacity="0">█<animate attributeName="opacity" values="0;0;1;0;1;0;0" keyTimes="0;0.020;0.021;0.050;0.080;0.110;1" dur="{D}s" repeatCount="indefinite" /></tspan>"""

    # Line 2 (Output: Chandan Sai Pavan Padala) - Appears instantly at 1.3s
    line2_str = make_instant_line_xml("Chandan Sai Pavan Padala", 1.3, "#ffffff")

    # Generate Line 3: $ cat skills.txt
    line3_text = "$ cat skills.txt"
    line3_xml = []
    # Prompt "$ " appears at 1.7s
    line3_xml.append(make_char_xml("$", 1.7, "#00b4d8"))
    line3_xml.append(make_char_xml(" ", 1.8, "#00b4d8"))
    # Command types at 0.08s intervals
    for idx, char in enumerate("cat skills.txt"):
        line3_xml.append(make_char_xml(char, 1.9 + idx * 0.08))
    line3_str = "".join(line3_xml)

    # Cursor 3 (Blinks on Line 3 from t=1.7s to t=3.3s)
    cursor3_xml = f"""<tspan fill="#00b4d8" opacity="0">█<animate attributeName="opacity" values="0;0;1;0;1;0;1;0;0" keyTimes="0;0.170;0.171;0.210;0.250;0.290;0.330;0.340;1" dur="{D}s" repeatCount="indefinite" /></tspan>"""

    # Line 4 (Output: FreeRTOS, ESP32, STM32, ARM Cortex-M4...) - Appears instantly at 3.5s
    line4_str = make_instant_line_xml("FreeRTOS, ESP32, STM32, ARM Cortex-M4...", 3.5, "#8b949e")

    # Generate Line 5: $ status
    line5_text = "$ status"
    line5_xml = []
    # Prompt "$ " appears at 3.9s
    line5_xml.append(make_char_xml("$", 3.9, "#00b4d8"))
    line5_xml.append(make_char_xml(" ", 4.0, "#00b4d8"))
    # Command types at 0.1s intervals
    for idx, char in enumerate("status"):
        line5_xml.append(make_char_xml(char, 4.1 + idx * 0.1))
    line5_str = "".join(line5_xml)

    # Cursor 5 (Blinks on Line 5 from t=3.9s to t=4.8s)
    cursor5_xml = f"""<tspan fill="#00b4d8" opacity="0">█<animate attributeName="opacity" values="0;0;1;0;1;0;0" keyTimes="0;0.390;0.391;0.420;0.450;0.480;0.490;1" dur="{D}s" repeatCount="indefinite" /></tspan>"""

    # Line 6 (Output: Building defence-grade embedded systems...) - Appears instantly at 5.0s
    line6_str = make_instant_line_xml("Building defence-grade embedded systems...", 5.0, "#8b949e")

    # Line 7 (Final prompt and infinite blinking cursor starting at t=5.4s)
    line7_prompt_xml = make_instant_line_xml("$ ", 5.4, "#00b4d8")
    cursor7_xml = f"""<tspan fill="#00b4d8" opacity="0">█<animate attributeName="opacity" values="0;0;1;0;1;0;1;0;0" keyTimes="0;0.540;0.550;0.620;0.700;0.780;0.850;0.860;1" dur="{D}s" repeatCount="indefinite" /></tspan>"""

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- Soft drop shadow for terminal window -->
    <filter id="window-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.55" />
    </filter>
  </defs>

  <!-- Dark Space Canvas -->
  <rect width="{width}" height="{height}" fill="#0d1117" rx="16" />

  <!-- Terminal Window Chrome with Drop Shadow -->
  <g filter="url(#window-shadow)">
    <!-- Base body panel -->
    <rect x="20" y="20" width="560" height="260" rx="10" ry="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />
    
    <!-- Header bar panel with top rounded corners -->
    <path d="M 20.6 20.6 L 579.4 20.6 A 9.4 9.4 0 0 1 579.4 50 L 20.6 50 A 9.4 9.4 0 0 1 20.6 20.6 Z" fill="#161b22" />
    <!-- Header dividing line -->
    <line x1="20" y1="50" x2="580" y2="50" stroke="#30363d" stroke-width="1.2" />

    <!-- macOS Traffic Lights (Red, Yellow, Green) -->
    <circle cx="45" cy="35" r="6" fill="#ff5f56" />
    <circle cx="65" cy="35" r="6" fill="#ffbd2e" />
    <circle cx="85" cy="35" r="6" fill="#27c93f" />

    <!-- Window Title -->
    <text x="300" y="39" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle" letter-spacing="0.5px">bash — whoami — 80×24</text>
  </g>

  <!-- Monospace CLI Text Contents -->
  <!-- Using Fira Code, Courier New, Consolas, or general monospace for terminal style -->
  <g font-family="'Fira Code', 'Consolas', 'Courier New', Courier, monospace" font-size="14" font-weight="500">
    <!-- Line 1: $ whoami -->
    <text x="40" y="80" fill="#ffffff">
      {line1_str}{cursor1_xml}
    </text>

    <!-- Line 2: Output -->
    <text x="40" y="110">
      {line2_str}
    </text>

    <!-- Line 3: $ cat skills.txt -->
    <text x="40" y="140" fill="#ffffff">
      {line3_str}{cursor3_xml}
    </text>

    <!-- Line 4: Output -->
    <text x="40" y="170">
      {line4_str}
    </text>

    <!-- Line 5: $ status -->
    <text x="40" y="200" fill="#ffffff">
      {line5_str}{cursor5_xml}
    </text>

    <!-- Line 6: Output -->
    <text x="40" y="230">
      {line6_str}
    </text>

    <!-- Line 7: Final active prompt -->
    <text x="40" y="260">
      {line7_prompt_xml}{cursor7_xml}
    </text>
  </g>
</svg>"""

    return svg_content

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "terminal-widget.svg")
    
    print("Generating animated macOS terminal widget SVG...")
    terminal_content = build_terminal_svg()
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(terminal_content)
        
    print(f"Successfully generated terminal widget SVG: {output_path}")

if __name__ == "__main__":
    main()
