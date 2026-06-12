#!/usr/bin/env python3
import os
import sys
import math

# Reconfigure stdout to use UTF-8 to prevent encoding errors on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def build_orbit_svg():
    width = 800
    height = 800
    cx = 400
    cy = 400
    r_orbit = 250
    duration = 25  # 25 seconds for a complete rotation

    # Icon definitions (paths scaled and centered for 24x24 viewBox unless custom SVG is used)
    # Simple-icons paths are wrapped in a group translated to center the icon (-12, -12) inside the node.
    icon_c = """<path fill="#00b4d8" d="M24 0c-13.255 0-24 10.745-24 24s10.745 24 24 24c5.632 0 10.796-1.944 14.88-5.184l-4.128-4.128c-3.072 2.304-6.864 3.712-10.752 3.712-9.264 0-16.8-7.536-16.8-16.8s7.536-16.8 16.8-16.8c3.888 0 7.68 1.408 10.752 3.712l4.128-4.128c-4.084-3.24-9.248-5.184-14.88-5.184z" />"""
    
    icon_cpp = """<path fill="#00b4d8" d="M21.996 11.233H18.78V8.016h-1.637v3.217h-3.217v1.637h3.217v3.217H18.78v-3.217h3.217v-1.637zm-7.79 0H10.99V8.016H9.352v3.217H6.136v1.637h3.216v3.217H10.99v-3.217h3.217v-1.637zM11.968.03c-6.6 0-11.945 5.345-11.945 11.945s5.345 11.946 11.945 11.946 11.945-5.346 11.945-11.946S18.57.03 11.968.03zm0 21.579c-5.318 0-9.633-4.316-9.633-9.634 0-5.318 4.315-9.633 9.633-9.633 5.318 0 9.634 4.315 9.634 9.633 0 5.318-4.316 9.634-9.634 9.634z" />"""
    
    icon_python = """<path fill="#00b4d8" d="M14.25.18a8.8 8.8 0 0 0-3.71.74l-.4.21c-.48.29-.9.69-1.2 1.18-.39.6-.57 1.34-.51 2.08h6v.75H6.26a4.2 4.2 0 0 0-2.8 1.1 4.5 4.5 0 0 0-1.2 3c-.04 1.13.28 2.24.93 3.16.58.74 1.36 1.29 2.25 1.58l.62.18v-2.3a2.3 2.3 0 0 1 1.76-2.19c1.66-.45 3.39-.45 5.06 0A2.3 2.3 0 0 1 14.63 12v3.13c0 .38-.13.76-.38 1.05-.28.32-.67.53-1.1.61L12.5 17c-1.34.18-2.69.07-4-.33l-.8-.24a3.8 3.8 0 0 0 2 2.36 4.7 4.7 0 0 0 2.2.49h1.1a4.2 4.2 0 0 0 2.8-1.1 4.5 4.5 0 0 0 1.2-3c.04-1.13-.28-2.24-.93-3.16a5.2 5.2 0 0 0-2.25-1.58l-.62-.18v2.3a2.3 2.3 0 0 1-1.76 2.19c-1.66.45-3.39.45-5.06 0A2.3 2.3 0 0 1 5.37 12V8.87c0-.38.13-.76.38-1.05.28-.32.67-.53 1.1-.61l.65-.11c1.34-.18 2.69-.07 4 .33l.8.24A3.8 3.8 0 0 0 10.3 5.3a4.7 4.7 0 0 0-2.2-.49H7A8.8 8.8 0 0 0 3.29.18" />"""
    
    icon_git = """<path fill="#00b4d8" d="M23.384 11.228L12.772.616a1.2 1.2 0 0 0-1.696 0L9.432 2.26a1.2 1.2 0 0 0 0 1.696l2.132 2.132H8.384a3 3 0 0 0-3 3v2.856a2.4 2.4 0 0 0-1.2 2.072c0 1.328 1.072 2.4 2.4 2.4s2.4-1.072 2.4-2.4c0-.98-.588-1.808-1.44-2.188v-2.74a1.2 1.2 0 0 1 1.2-1.2h3.18l-1.92 1.92a1.2 1.2 0 0 0 0 1.696l1.644 1.644a1.2 1.2 0 0 0 1.696 0l3.836-3.836a1.2 1.2 0 0 0 0-1.696L15.06 7.644l1.92-1.92v4.88a2.4 2.4 0 0 0-1.2 2.072c0 1.328 1.072 2.4 2.4 2.4s2.4-1.072 2.4-2.4a2.4 2.4 0 0 0-1.2-2.072V5.124l1.968 1.968a1.2 1.2 0 0 0 1.696 0l2.64-2.64a1.2 1.2 0 0 0 0-1.696z" />"""
    
    icon_linux = """<path fill="#00b4d8" d="M12 .003c-.116.002-.232.008-.344.02-.756.082-1.58.552-2.1 1.185-.705.86-1.077 2.05-1.072 3.428.005 1.558.463 3.013.916 4.316.064.183.133.364.204.544a4.137 4.137 0 0 0-.822.42c-.524.348-.962.836-1.258 1.4-.298.566-.414 1.206-.328 1.83.085.623.385 1.196.84 1.623.426.4.996.65 1.597.747.534.086 1.082.022 1.602-.152-.008.2-.012.4-.012.603 0 1.233.155 2.453.487 3.52.348 1.12.923 2.052 1.737 2.68.78.604 1.77.94 2.875.94 1.106 0 2.095-.336 2.875-.94.814-.628 1.39-1.56 1.738-2.68.332-1.067.487-2.287.487-3.52 0-.203-.004-.403-.012-.603.52.174 1.068.238 1.602.152.602-.097 1.17-.347 1.598-.747.455-.427.755-1 .84-1.623.086-.624-.03-1.264-.328-1.83-.296-.564-.734-1.052-1.258-1.4a4.137 4.137 0 0 0-.822-.42c.07-.18.14-.36.204-.544.453-1.303.91-2.758.916-4.316.005-1.378-.367-2.568-1.072-3.428-.52-.633-1.344-1.103-2.1-1.185a5.556 5.556 0 0 0-.344-.02c-.886-.008-1.835.347-2.63.92-.128.093-.25.195-.366.304-.116-.109-.238-.21-.366-.303-.795-.573-1.744-.928-2.63-.92zm0 1.625c.575.006 1.176.242 1.684.608.188.136.353.3.497.48.067.085.127.176.18.27.054-.094.113-.185.18-.27.144-.18.31-.344.497-.48.508-.366 1.11-.602 1.684-.608.356.004.707.135.978.466.452.55.705 1.488.7 2.65-.005 1.397-.428 2.766-.867 4.025a18.23 18.23 0 0 1-.502 1.297c-.36-.088-.734-.14-1.114-.15-.098-.003-.197-.003-.295-.003H12.04c-.097 0-.197 0-.295.003-.38.01-.754.062-1.114.15a18.23 18.23 0 0 1-.502-1.297c-.44-1.26-.862-2.628-.867-4.025-.005-1.162.248-2.1.7-2.65.27-.33.62-.462.978-.466zm-3.344 9.125c.245.163.454.38.606.634.152.253.23.542.228.835v.004c-.002.293-.08.582-.23.836a1.728 1.728 0 0 1-.604.634 1.54 1.54 0 0 1-.794.218c-.287 0-.57-.077-.818-.224a1.733 1.733 0 0 1-.606-.634c-.152-.254-.23-.543-.228-.836v-.004c.002-.293.08-.582.23-.835a1.728 1.728 0 0 1 .604-.634c.25-.15.53-.227.818-.228.286 0 .57.078.818.228a1.54 1.54 0 0 1 .794-.214zm6.688 0c.245.163.454.38.606.634.152.253.23.542.228.835v.004c-.002.293-.08.582-.23.836a1.728 1.728 0 0 1-.604.634 1.54 1.54 0 0 1-.794.218c-.287 0-.57-.077-.818-.224a1.733 1.733 0 0 1-.606-.634c-.152-.254-.23-.543-.228-.836v-.004c.002-.293.08-.582.23-.835a1.728 1.728 0 0 1 .604-.634c.25-.15.53-.227.818-.228.286 0 .57.078.818.228a1.54 1.54 0 0 1 .794-.214z" />"""

    # Custom chip vector design for ESP32
    esp32_design = """
    <!-- Chip body -->
    <rect x="-14" y="-14" width="28" height="28" rx="3" fill="#1f2937" stroke="#00b4d8" stroke-width="1.5" />
    <!-- Outer pins -->
    <path d="M-10 -16 V-14 M-5 -16 V-14 M0 -16 V-14 M5 -16 V-14 M10 -16 V-14
             M-10 14 V16 M-5 14 V16 M0 14 V16 M5 14 V16 M10 14 V16
             M-16 -10 H-14 M-16 -5 H-14 M-16 0 H-14 M-16 5 H-14 M-16 10 H-14
             M14 -10 H16 M14 -5 H16 M14 0 H16 M14 5 H16 M14 10 H16" 
          stroke="#00b4d8" stroke-width="1.2" stroke-linecap="round" />
    <!-- WiFi signal icon -->
    <path d="M-4 -3 A 6 6 0 0 1 4 -3 M-2.5 -1.2 A 3.8 3.8 0 0 1 2.5 -1.2 M-1 .5 A 1.5 1.5 0 0 1 1 .5" fill="none" stroke="#00b4d8" stroke-width="1" stroke-linecap="round" />
    <!-- Text label inside chip -->
    <text x="0" y="8" fill="#ffffff" font-family="system-ui, sans-serif" font-size="6" font-weight="800" text-anchor="middle" letter-spacing="0.5px">ESP32</text>
    """

    # Custom chip vector design for STM32
    stm32_design = """
    <!-- Chip body -->
    <rect x="-14" y="-14" width="28" height="28" rx="3" fill="#1f2937" stroke="#00b4d8" stroke-width="1.5" />
    <!-- Outer pins -->
    <path d="M-10 -16 V-14 M-5 -16 V-14 M0 -16 V-14 M5 -16 V-14 M10 -16 V-14
             M-10 14 V16 M-5 14 V16 M0 14 V16 M5 14 V16 M10 14 V16
             M-16 -10 H-14 M-16 -5 H-14 M-16 0 H-14 M-16 5 H-14 M-16 10 H-14
             M14 -10 H16 M14 -5 H16 M14 0 H16 M14 5 H16 M14 10 H16" 
          stroke="#00b4d8" stroke-width="1.2" stroke-linecap="round" />
    <!-- ARM core flash bolt -->
    <path d="M-2.5 -6.5 L2.5 -2.5 L-0.5 0.5 L3.5 6.5 L-2.5 1.5 L0.5 -1.5 Z" fill="#00b4d8" />
    <!-- Text label inside chip -->
    <text x="0" y="9" fill="#ffffff" font-family="system-ui, sans-serif" font-size="5.5" font-weight="800" text-anchor="middle" letter-spacing="0.5px">STM32</text>
    """

    # Custom scheduler task design for FreeRTOS
    freertos_design = """
    <!-- Circular scheduler dial outline -->
    <circle cx="0" cy="0" r="11" fill="none" stroke="#00b4d8" stroke-width="1.2" />
    <!-- Task execution rows -->
    <path d="M-7 -4 H1 M-4 0 H4 M-1 4 H7" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" />
    <!-- Preemption dispatch sync arrows -->
    <path d="M-4 -4 V0 M-1 0 V4" stroke="#00b4d8" stroke-width="0.8" stroke-linecap="round" />
    <!-- Labels -->
    <text x="0" y="-7.5" fill="#ffffff" font-family="system-ui, sans-serif" font-size="5" font-weight="800" text-anchor="middle" letter-spacing="0.5px">FREE</text>
    <text x="0" y="10" fill="#00b4d8" font-family="system-ui, sans-serif" font-size="5.5" font-weight="800" text-anchor="middle" letter-spacing="0.5px">RTOS</text>
    """

    # Assign each node an icon/graphic
    # 8 nodes spaced at 45 degree intervals around the circle
    nodes = [
        {"name": "C", "graphic": f'<g transform="translate(-13, -13) scale(1.08)">{icon_c}</g>'},
        {"name": "ESP32", "graphic": esp32_design},
        {"name": "C++", "graphic": f'<g transform="translate(-13, -13) scale(1.08)">{icon_cpp}</g>'},
        {"name": "STM32", "graphic": stm32_design},
        {"name": "FreeRTOS", "graphic": freertos_design},
        {"name": "Linux", "graphic": f'<g transform="translate(-12, -12) scale(1.0)">{icon_linux}</g>'},
        {"name": "Python", "graphic": f'<g transform="translate(-12, -12) scale(1.0)">{icon_python}</g>'},
        {"name": "Git", "graphic": f'<g transform="translate(-12, -12) scale(1.0)">{icon_git}</g>'}
    ]

    # Generate paths for nodes (so they stay upright during orbit)
    # They start at their respective offsets (0, 45, 90, 135, 180, 225, 270, 315) and traverse in a circle
    orbit_paths_xml = ""
    orbiting_groups_xml = ""
    
    for i, node in enumerate(nodes):
        angle_deg = i * 45
        angle_rad = math.radians(angle_deg)
        
        # Start coordinates at angle_rad (centered at 400,400 with radius 250)
        # 0 degrees is straight up (400, 150)
        x0 = cx + r_orbit * math.sin(angle_rad)
        y0 = cy - r_orbit * math.cos(angle_rad)
        
        # Opposite coordinate for semicircle path
        x1 = cx - r_orbit * math.sin(angle_rad)
        y1 = cy + r_orbit * math.cos(angle_rad)
        
        # Absolute circular path starting at (x0, y0) and loops
        path_str = f"M {x0:.2f},{y0:.2f} A {r_orbit},{r_orbit} 0 1,1 {x1:.2f},{y1:.2f} A {r_orbit},{r_orbit} 0 1,1 {x0:.2f},{y0:.2f} Z"
        
        orbit_paths_xml += f'    <!-- Path for {node["name"]} -->\n'
        orbit_paths_xml += f'    <path id="path-node-{i}" d="{path_str}" fill="none" />\n'
        
        # Orbiting node markup
        # Inside the group, elements are centered at (0,0) because animateMotion moves the group's local origin.
        orbiting_groups_xml += f"""
  <!-- Orbiting Node: {node["name"]} -->
  <g>
    <!-- Animate along its custom offset circle path -->
    <animateMotion path="{path_str}" dur="{duration}s" repeatCount="indefinite" />
    
    <!-- Outer glassmorphism glowing circle bounds -->
    <circle cx="0" cy="0" r="32" fill="#151d28" fill-opacity="0.95" stroke="#00b4d8" stroke-width="1.5" filter="url(#node-shadow)" />
    <circle cx="0" cy="0" r="32" fill="none" stroke="#00b4d8" stroke-width="4" stroke-opacity="0.25" filter="url(#node-glow-blur)" />
    
    <!-- Render the graphics centered at (0,0) -->
    {node["graphic"]}
    
    <!-- Label shown on hover or subtly below -->
    <text x="0" y="46" fill="#8b949e" font-family="system-ui, sans-serif" font-size="10" font-weight="600" text-anchor="middle" letter-spacing="0.5px">{node["name"]}</text>
  </g>"""

    # Sync lines with rotating group
    lines_xml = ""
    for i in range(8):
        angle_deg = i * 45
        lines_xml += f"""    <line x1="400" y1="400" x2="400" y2="150" transform="rotate({angle_deg} 400 400)" stroke="#00b4d8" stroke-opacity="0.25" stroke-width="1.8" stroke-dasharray="8 12">
      <animate attributeName="stroke-dashoffset" values="40;0" dur="2s" repeatCount="indefinite" />
    </line>\n"""

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- Soft glow filter for the central core initials -->
    <filter id="core-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Glowing filter for node borders -->
    <filter id="node-glow-blur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="blur" />
    </filter>

    <!-- Node drop shadow -->
    <filter id="node-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#000000" flood-opacity="0.6" />
    </filter>

    <!-- Radial gradient for background space glow -->
    <radialGradient id="bg-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00b4d8" stop-opacity="0.06" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </radialGradient>

    <!-- Central core gradient -->
    <radialGradient id="core-gradient" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00b4d8" stop-opacity="0.25" />
      <stop offset="70%" stop-color="#0077b6" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Dark Space Background -->
  <rect width="{width}" height="{height}" fill="#0d1117" rx="24" />
  
  <!-- Subtle cosmic background glow -->
  <circle cx="400" cy="400" r="350" fill="url(#bg-glow)" />

  <!-- Dotted Orbit Track ring for reference -->
  <circle cx="400" cy="400" r="{r_orbit}" fill="none" stroke="#00b4d8" stroke-opacity="0.08" stroke-width="2" stroke-dasharray="6 6" />

  <!-- Dynamic Rotating Data lines (synced exactly with the duration of the nodes) -->
  <g>
    <!-- Rotate group clockwise around center -->
    <animateTransform attributeName="transform" type="rotate" from="0 400 400" to="360 400 400" dur="{duration}s" repeatCount="indefinite" />
{lines_xml}  </g>

  <!-- Central Glowing Processor Core -->
  <g id="core-group">
    <!-- Radial fill glow -->
    <circle cx="400" cy="400" r="80" fill="url(#core-gradient)" />
    
    <!-- Outer core glowing breathing shell -->
    <circle cx="400" cy="400" r="70" fill="none" stroke="#00b4d8" stroke-width="2.5" opacity="0.8">
      <animate attributeName="r" values="70;82;70" dur="4s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.8;0.2;0.8" dur="4s" repeatCount="indefinite" />
    </circle>
    
    <!-- Solid inner core boundary -->
    <circle cx="400" cy="400" r="68" fill="#111827" stroke="#0077b6" stroke-width="1.5" />
    
    <!-- Central Initials with subtle glow -->
    <text x="400" y="410" fill="#ffffff" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="900" text-anchor="middle" letter-spacing="3px" filter="url(#core-glow)">
      PCSP
    </text>
  </g>

  <!-- Orbiting Tech stack nodes -->
{orbiting_groups_xml}
</svg>"""

    return svg_content

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "tech-orbit.svg")
    
    print("Generating dynamic tech stack orbit SVG...")
    orbit_content = build_orbit_svg()
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(orbit_content)
        
    print(f"Successfully generated tech orbit SVG: {output_path}")

if __name__ == "__main__":
    main()
