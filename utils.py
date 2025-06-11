from browser import document, html


bar_max_height = 100
height_per_block = 150
current_arrows = {}


def preprocess_highlight(state, highlight):
    expanded_highlight = set()

    for section, arrays in state.items():
        for i, arr in enumerate(arrays):
            for hl in highlight:
                sec, idx, bar = hl

                if sec == section and idx == i:
                    if bar == "all":
                        for j in range(len(arr)):
                            expanded_highlight.add((sec, i, j))

                    elif isinstance(bar, int):
                        expanded_highlight.add((sec, i, bar))

    return expanded_highlight


def create_section(title_text, content_elements, height_px=None):
    section = html.DIV(Class="section")
    title = html.H3(title_text, Class="section-title")

    section <= title

    for elem in content_elements:
        section <= elem

    return section


def render_array(arr, label, base_id, max_val, run_info=None):
    array_container = html.DIV(Class="array-container")
    array_container.id = f"{base_id}-container"
    
    if label:
        array_label = html.DIV(label, Class="array-label")
        array_container <= array_label

    # Calculate width and spacing as percentage of container
    num_bars = len(arr)
    if num_bars > 0:
        bar_width_percent = 80 / num_bars  # Use 80% of container, leaving 20% for spacing
        spacing_percent = 20 / (num_bars + 1)  # Distribute remaining 20% as spacing

    else:
        bar_width_percent = 0
        spacing_percent = 0

    for i, val in enumerate(arr):
        height = (val / max_val) * bar_max_height
        left_position = spacing_percent + i * (bar_width_percent + spacing_percent)
        
        bar = html.DIV(
            Class="bar",
            style={
                "height": f"{height}px",
                "left": f"{left_position}%",
                "width": f"{bar_width_percent}%"
            },
            id=f"{base_id}-bar-{i}"
        )

        # Add text element for the value
        bar_text = html.DIV(
            str(val) if val != 0 else "",
            Class="bar-text",
            id=f"{base_id}-bar-text-{i}"
        )

        bar <= bar_text
        array_container <= bar

    return array_container


def create_arrow_layer():
    """Create SVG layer for arrows"""
    svg = document.createElementNS("http://www.w3.org/2000/svg", "svg")
    svg.setAttribute("class", "arrow-svg")
    svg.id = "arrowLayer"
    
    # Create defs for arrowhead marker
    defs = document.createElementNS("http://www.w3.org/2000/svg", "defs")
    marker = document.createElementNS("http://www.w3.org/2000/svg", "marker")
    marker.setAttribute("id", "arrowhead")
    marker.setAttribute("markerWidth", "10")
    marker.setAttribute("markerHeight", "7")
    marker.setAttribute("refX", "9")
    marker.setAttribute("refY", "3.5")
    marker.setAttribute("orient", "auto")
    
    polygon = document.createElementNS("http://www.w3.org/2000/svg", "polygon")
    polygon.setAttribute("points", "0 0, 10 3.5, 0 7")
    polygon.setAttribute("fill", "#000000")
    
    marker.appendChild(polygon)
    defs.appendChild(marker)
    svg.appendChild(defs)
    
    return svg


def draw_arrow(from_id, to_id, arrow_id):
    """Draw arrow between two elements"""
    from_el = document.getElementById(from_id)
    to_el = document.getElementById(to_id)
    
    if not from_el or not to_el:
        return
    
    svg = document.getElementById("arrowLayer")
    if not svg:
        return
    
    # Remove existing arrow if it exists
    existing_arrow = document.getElementById(arrow_id)
    if existing_arrow:
        existing_arrow.remove()
    
    # Get container bounds for relative positioning
    container = document.getElementById("container")
    container_rect = container.getBoundingClientRect()
    
    # Get element bounds
    from_rect = from_el.getBoundingClientRect()
    to_rect = to_el.getBoundingClientRect()
    
    # Calculate relative positions
    x1 = from_rect.left - container_rect.left + from_rect.width
    y1 = from_rect.top - container_rect.top + from_rect.height / 2
    x2 = to_rect.left - container_rect.left
    y2 = to_rect.top - container_rect.top + to_rect.height / 2
    
    # Create arrow line
    line = document.createElementNS("http://www.w3.org/2000/svg", "line")
    line.setAttribute("id", arrow_id)
    line.setAttribute("x1", str(x1))
    line.setAttribute("y1", str(y1))
    line.setAttribute("x2", str(x2))
    line.setAttribute("y2", str(y2))
    line.setAttribute("stroke", "#000000")
    line.setAttribute("stroke-width", "3")
    line.setAttribute("marker-end", "url(#arrowhead)")
    line.setAttribute("opacity", "0.8")
    
    svg.appendChild(line)
    current_arrows[arrow_id] = line


def remove_arrow(arrow_id):
    """Remove an arrow"""
    if arrow_id in current_arrows:
        current_arrows[arrow_id].remove()
        del current_arrows[arrow_id]


def clear_all_arrows():
    """Clear all arrows"""
    for arrow_id in list(current_arrows.keys()):
        remove_arrow(arrow_id)


def log_to_console(message, newline=True):
    """
    Log a message to the console display.
    If newline=False, the message will be added to the current line.
    """
    console = document["console"]
    if newline:
        console.innerHTML += f"<div>{message}</div>"
    else:
        # Get the last div or create one if none exists
        divs = console.querySelectorAll("div")
        if divs.length > 0:
            last_div = divs[divs.length - 1]
            last_div.innerHTML += f" {message}"
        else:
            console.innerHTML += f"<div>{message}</div>"
    console.scrollTop = console.scrollHeight


def create_run_outlines(state, memory_run_info):
    """Create outlined boxes around pages belonging to the same run"""
    # Clear existing outlines
    existing_outlines = document.querySelectorAll('.run-outline')
    for outline in existing_outlines:
        outline.remove()
    
    if not memory_run_info:
        return
    
    container = document.getElementById("container")
    
    for section_type in ['input', 'output']:
        if section_type not in memory_run_info:
            continue
            
        run_assignments = memory_run_info[section_type]
        
        # Group pages by run number
        runs = {}
        for page_idx, run_num in run_assignments.items():
            if run_num not in runs:
                runs[run_num] = []
            runs[run_num].append(page_idx)
        
        # Create outline for each run with multiple pages
        for run_num, page_indices in runs.items():
            if len(page_indices) > 1:  # Only outline runs with multiple pages
                # Find the bounding box of all pages in this run
                first_page_idx = min(page_indices)
                last_page_idx = max(page_indices)
                
                first_container = document.getElementById(f"{section_type}-page-{first_page_idx}-container")
                last_container = document.getElementById(f"{section_type}-page-{last_page_idx}-container")
                
                if first_container and last_container:
                    # Get positions relative to the main container
                    container_rect = container.getBoundingClientRect()
                    first_rect = first_container.getBoundingClientRect()
                    last_rect = last_container.getBoundingClientRect()
                    
                    # Calculate outline dimensions
                    left = first_rect.left - container_rect.left - 10
                    top = first_rect.top - container_rect.top - 10
                    right = last_rect.right - container_rect.left + 10
                    bottom = last_rect.bottom - container_rect.top + 10
                    
                    # Create outline element
                    outline = html.DIV(Class="run-outline")
                    outline.style.left = f"{left}px"
                    outline.style.top = f"{top}px"
                    outline.style.width = f"{right - left}px"
                    outline.style.height = f"{bottom - top}px"
                    
                    container <= outline