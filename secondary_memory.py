from browser import document, html, timer, window
from utils import *
import copy


bar_max_height = 100
current_arrows = {}


def create_bars(input_pages, output_pages, frames):
    """
    Create bars for external sorting with separate input and output secondary memory.
    """
    container = document["container"]
    container.clear()
    container.style["backgroundColor"] = "#e0f7fa"
    
    # Clear existing arrows
    clear_all_arrows()

    # Calculate max value for scaling
    all_values = []
    for page in input_pages:
        all_values.extend(page)

    for page in output_pages:
        all_values.extend(page)

    for frame in frames:
        all_values.extend(frame)

    max_val = max(all_values) if all_values else 1

    # Create input secondary memory section
    input_elements = []
    for i, page in enumerate(input_pages):
        input_elements.append(render_array(page, f"Page {i+1}", f"input-page-{i}", max_val))

    input_secondary_memory_section = create_section("Secondary Memory - Input Pass 0", input_elements)

    # Create output secondary memory section
    output_elements = []
    for i, page in enumerate(output_pages):
        output_elements.append(render_array(page, f"Page {i+1}", f"output-page-{i}", max_val))

    output_secondary_memory_section = create_section("Secondary Memory - Output Pass 0", output_elements)

    # Create buffer section
    buffer_elements = []
    for i, frame in enumerate(frames):
        buffer_elements.append(render_array(frame, f"Frame {i+1}", f"frame-{i}", max_val))

    buffer_section = create_section("Buffer", buffer_elements)

    # Create flexible layout with buffer in the middle
    layout = html.DIV(Class="memory-layout")
    layout <= input_secondary_memory_section
    layout <= buffer_section
    layout <= output_secondary_memory_section

    # Add arrow layer
    svg = create_arrow_layer()
    
    container <= layout
    container <= svg


def update_bars(state, highlight=set()):
    expanded_highlight = preprocess_highlight(state, highlight)
    
    # Calculate max value for consistent scaling
    all_values = []
    for section, arrays in state.items():
        for arr in arrays:
            all_values.extend(arr)

    max_val = max(all_values) if all_values else 1
    
    for section, arrays in state.items():
        for i, arr in enumerate(arrays):
            for j, val in enumerate(arr):
                if section == "input_pages":
                    bar_id = f"input-page-{i}-bar-{j}"

                elif section == "output_pages":
                    bar_id = f"output-page-{i}-bar-{j}"

                elif section == "frames":
                    bar_id = f"frame-{i}-bar-{j}"

                else:
                    continue
                    
                bar = document.getElementById(bar_id)
                if bar:
                    height = (val / max_val) * bar_max_height
                    bar.style.height = f"{height}px"
                    bar.style.backgroundColor = "#FF5733" if (section, i, j) in expanded_highlight else "#4CAF50"

                if section == "input_pages":
                    text_id = f"input-page-{i}-bar-text-{j}"

                elif section == "output_pages":
                    text_id = f"output-page-{i}-bar-text-{j}"

                elif section == "frames":
                    text_id = f"frame-{i}-bar-text-{j}"

                text_element = document.getElementById(text_id)
                if text_element:
                    if val == 0 or val is None:
                        text_element.innerHTML = ""

                    else:
                        text_element.innerHTML = str(val)


def animate(steps):

    i = 0

    def update():
        nonlocal i
        if i < len(steps):
            paused = window.animationPaused if hasattr(window, 'animationPaused') else False

            if not paused:
                state, highlight, arrows, log_message, swap, memory_run_info, buffer_run_info = steps[i]
                update_bars(state, highlight)
                
                if log_message:
                    log_to_console(log_message)
               
                # handle arrows
                if arrows:
                    for arrow_info in arrows:
                        if arrow_info["action"] == "draw":
                            speed = int(document["speedRange"].value)
                            delay = min(100, speed // 2)
                            timer.set_timeout(lambda: draw_arrow(arrow_info["from"], arrow_info["to"], arrow_info["id"]), delay)

                        elif arrow_info["action"] == "remove":
                            remove_arrow(arrow_info["id"])

                if swap:
                    sections = document.querySelectorAll('.section')
                    for section in sections:
                        title_element = section.querySelector('.section-title')
                        if title_element:
                            if 'Input Pass' in title_element.innerHTML:
                                title_element.innerHTML = f"Secondary Memory - Input Pass {swap}"

                            elif 'Output Pass' in title_element.innerHTML:
                                title_element.innerHTML = f"Secondary Memory - Output Pass {swap}"
                
                if memory_run_info:
                    if 'input' in memory_run_info:
                        for page_idx, run_num in memory_run_info['input'].items():
                            container = document.getElementById(f"input-page-{page_idx}-container")

                            if container:
                                label_element = container.querySelector('.array-label')

                                if label_element:
                                    label_element.innerHTML = f"Page {page_idx+1} (Run {run_num})"
                    
                    if 'output' in memory_run_info:
                        for page_idx, run_num in memory_run_info['output'].items():
                            container = document.getElementById(f"output-page-{page_idx}-container")

                            if container:
                                label_element = container.querySelector('.array-label')

                                if label_element:
                                    label_element.innerHTML = f"Page {page_idx+1} (Run {run_num})"

                    create_run_outlines(state, memory_run_info)
                
                if buffer_run_info:
                    for frame_idx, run_num in buffer_run_info.items():
                        container = document.getElementById(f"frame-{frame_idx}-container")

                        if container:
                            label_element = container.querySelector('.array-label')

                            if label_element:
                                if run_num == "output":
                                    label_element.innerHTML = f"Frame {frame_idx+1} (Output)"

                                else:
                                    label_element.innerHTML = f"Frame {frame_idx+1} (Run {run_num})"

                i += 1
                if i < len(steps):
                    speed = int(document["speedRange"].value)
                    timer.set_timeout(update, speed)

                else:
                    window.disableStopButton()

            else:
                timer.set_timeout(update, 100)

        if i >= len(steps):
            for section_idx, section in enumerate(document.querySelectorAll('.section')):
                title_element = section.querySelector('.section-title')

                if title_element and 'Output Pass' in title_element.innerHTML:
                    # Find all bars in this output section
                    bars = section.querySelectorAll('.bar')

                    for bar in bars:
                        bar.style.backgroundColor = "#6ca6d6"  # Light blue color

    window.enableStopButton()

    update()


def k_way_merge_sort(input_pages, output_pages, frames, n_pages, n_frames, elements_per_page, callback):

    steps = []
    frames = [[] for _ in range(n_frames)]
    n_accesses = 0

    def record(highlight=set(), arrows=None, log_message=None, swap=False, memory_run_info=None, buffer_run_info=None):
        input_pages_copy = copy.deepcopy(input_pages)
        output_pages_copy = copy.deepcopy(output_pages)
        frames_copy = copy.deepcopy(frames)
        highlight_copy = copy.deepcopy(highlight)
        arrows_copy = copy.deepcopy(arrows) if arrows else []
        steps.append(({"input_pages": input_pages_copy,
                        "output_pages": output_pages_copy,
                        "frames": frames_copy},
                        highlight_copy,
                        arrows_copy,
                        log_message,
                        swap,
                        memory_run_info,
                        buffer_run_info))

    # Check if sorting page-by-page
    sort_page_by_page = document["sort_page_by_page"].checked

    if sort_page_by_page:
        record(log_message="Pass 0: sort each page.")
        
        for l in range(n_pages):
            # load page into frame
            frames[0] = copy.deepcopy(input_pages[l])
            n_accesses += 1

            arrow_info = [{
                "action": "draw",
                "from": f"input-page-{l}-container",
                "to": f"frame-0-container",
                "id": f"arrow-input-page-{l}-frame-0"
            }]

            record(highlight=(("input_pages", l, "all"),
                            ("frames", 0, "all")),
                            arrows=arrow_info,
                            log_message=f"Input {l+1} loaded in frame 1.")

            # sort the frame using bubble sort
            for i in range(len(frames[0])):
                for j in range(len(frames[0]) - i - 1):
                    if frames[0][j] > frames[0][j + 1]:
                        frames[0][j], frames[0][j + 1] = frames[0][j + 1], frames[0][j]
                        record(highlight=(("frames", 0, j), ("frames", 0, j+1)))

            # write sorted frame to output page
            output_pages[l] = copy.deepcopy(frames[0])
            n_accesses += 1

            arrow_remove_input = [{
                "action": "remove",
                "id": f"arrow-input-page-{l}-frame-0"
            }]

            arrow_to_output = [{
                "action": "draw",
                "from": f"frame-0-container",
                "to": f"output-page-{l}-container",
                "id": f"arrow-frame-0-output-page-{l}"
            }]

            record(highlight=(("frames", 0, "all"),
                            ("output_pages", l, "all")),
                            arrows=arrow_remove_input + arrow_to_output,
                            log_message=f"Frame 1 written in output {l+1}.")
            
            # remove arrow to output after a brief moment
            arrow_remove_output = [{
                "action": "remove",
                "id": f"arrow-frame-0-output-page-{l}"
            }]

            record(arrows=arrow_remove_output)

    else:

        output_run_assignments = {}

        for i in range(len(output_pages)):
            output_run_assignments[i] = (i // n_frames) + 1

        run_info = {
            'output': output_run_assignments
        }

        record(log_message="Pass 0: fill buffer and perform in-place sort.", memory_run_info=run_info)
        
        # Process pages in groups
        for group_start in range(0, n_pages, n_frames):
            group_end = min(group_start + n_frames, n_pages)
            current_group_size = group_end - group_start
            
            # Load pages into frames
            current_arrows = []
            for i in range(current_group_size):
                page_idx = group_start + i
                frames[i] = copy.deepcopy(input_pages[page_idx])
                n_accesses += 1
                
                arrow_id = f"arrow-input-page-{page_idx}-frame-{i}"
                current_arrows.append(arrow_id)
                
                arrow_info = [{
                    "action": "draw",
                    "from": f"input-page-{page_idx}-container",
                    "to": f"frame-{i}-container",
                    "id": arrow_id
                }]
                
                record(highlight=(("input_pages", page_idx, "all"),
                                ("frames", i, "all")),
                                arrows=arrow_info,
                                log_message=f"Input {page_idx + 1} loaded in frame {i + 1}.")
            
            # Create a single array combining all elements from loaded frames
            combined_elements = []
            for i in range(current_group_size):
                combined_elements.extend(frames[i])
            
            # Perform bubble sort on the combined array with visualization
            total_elements = len(combined_elements)
            for i in range(total_elements):
                for j in range(total_elements - i - 1):
                    if combined_elements[j] > combined_elements[j + 1]:
                        combined_elements[j], combined_elements[j + 1] = combined_elements[j + 1], combined_elements[j]
                        
                        # Update frames to reflect the swap
                        # Determine which frames and positions correspond to indices j and j+1
                        frame_j = j // elements_per_page
                        pos_j = j % elements_per_page
                        frame_j1 = (j + 1) // elements_per_page
                        pos_j1 = (j + 1) % elements_per_page
                        
                        if frame_j < current_group_size and frame_j1 < current_group_size:
                            frames[frame_j][pos_j], frames[frame_j1][pos_j1] = frames[frame_j1][pos_j1], frames[frame_j][pos_j]
                            record(highlight=(("frames", frame_j, pos_j), ("frames", frame_j1, pos_j1)))
            
            # Write sorted frames back to output pages
            for i in range(current_group_size):
                page_idx = group_start + i
                output_pages[page_idx] = copy.deepcopy(frames[i])
                n_accesses += 1
                
                # Remove input arrow and add output arrow
                arrow_remove_input = [{
                    "action": "remove",
                    "id": current_arrows[i]
                }]
                
                arrow_to_output = [{
                    "action": "draw",
                    "from": f"frame-{i}-container",
                    "to": f"output-page-{page_idx}-container",
                    "id": f"arrow-frame-{i}-output-page-{page_idx}"
                }]
                
                record(highlight=(("frames", i, "all"),
                                ("output_pages", page_idx, "all")),
                                arrows=arrow_remove_input + arrow_to_output,
                                log_message=f"Frame {i + 1} written to output {page_idx + 1}.")
                
                # Remove output arrow
                arrow_remove_output = [{
                    "action": "remove",
                    "id": f"arrow-frame-{i}-output-page-{page_idx}"
                }]

                record(arrows=arrow_remove_output)


    record(log_message="Pass 0 completed.")

    # merge passes
    k = n_frames - 1

    if sort_page_by_page:
        old_runs_size = 1
    
    else:
        old_runs_size = n_frames
    
    current_runs_size = old_runs_size
    pass_num = 0

    while current_runs_size < n_pages:
        current_runs_size *= k
        pass_num += 1

        # swap input and output secondary memory
        input_pages, output_pages = output_pages, input_pages

        # reset output page
        output_pages = [[0] * elements_per_page for _ in range(n_pages)]

        # Calculate run assignments for this pass
        input_run_assignments = {}
        output_run_assignments = {}

        for i in range(len(input_pages)):
            input_run_assignments[i] = (i // old_runs_size) + 1

        for i in range(len(output_pages)):
            output_run_assignments[i] = (i // current_runs_size) + 1

        run_info = {
            'input': input_run_assignments,
            'output': output_run_assignments
        }

        record(log_message=f"Starting Pass {pass_num}.", swap=pass_num, memory_run_info=run_info)

        # divide into runs
        runs = [input_pages[i:i + old_runs_size] for i in range(0, len(input_pages), old_runs_size)]

        # divide into executions
        executions = [runs[i:i + k] for i in range(0, len(runs), k)]

        output_page_idx = 0

        # perform each execution
        for exec_idx, execution in enumerate(executions):
            record(log_message=f"Starting Run {exec_idx+1}.")

            run_info = {}
            run_info[k] = "output"

            for frame in range(n_frames-1):
                run_info[frame] = k * exec_idx + frame + 1

            record(buffer_run_info=run_info)

            # Initialize frame pointers and page pointers for each run
            frame_pointers = [0] * len(execution)  # Points to current element in each frame
            page_pointers = [0] * len(execution)   # Points to current page in each run
            output_frame_pointer = 0
            
            # Track current arrow IDs for each frame
            current_arrow_ids = [None] * len(execution)
            
            # Initialize output frame with zeros
            frames[-1] = [0] * elements_per_page
            
            # load first page of each run into buffer frames
            for j in range(len(execution)):
                frames[j] = copy.deepcopy(execution[j][0])
                n_accesses += 1
                
                # Calculate the global page index for the first page of this run
                global_page_idx = exec_idx * k * old_runs_size + j * old_runs_size
                current_arrow_ids[j] = f"arrow-input-page-{global_page_idx}-frame-{j}"

                arrow_info = [{
                    "action": "draw",
                    "from": f"input-page-{global_page_idx}-container",
                    "to": f"frame-{j}-container",
                    "id": current_arrow_ids[j]
                }]

                record(highlight=(("input_pages", global_page_idx, "all"),
                                ("frames", j, "all")),
                                arrows=arrow_info,
                                log_message=f"Input {global_page_idx + 1} loaded in frame {j + 1}.")

            # perform merging pass
            # until there are no more elements left in any frame
            while any(frame_pointers[i] < len(frames[i]) or 
                    page_pointers[i] < len(execution[i]) - 1 
                    for i in range(len(execution))):

                # find minimum between first non-processed element of each input frame
                min_val = float('inf')
                min_frame = -1
                
                for i in range(len(execution)):
                    if frame_pointers[i] < len(frames[i]) and frames[i][frame_pointers[i]] != 0:
                        if frames[i][frame_pointers[i]] < min_val:
                            min_val = frames[i][frame_pointers[i]]
                            min_frame = i

                if min_frame == -1:
                    break

                # write minimum in the output frame and mark as processed in input frame
                frames[-1][output_frame_pointer] = min_val
                output_frame_pointer += 1
                
                record(highlight=(("frames", min_frame, frame_pointers[min_frame]),
                                ("frames", n_frames-1, output_frame_pointer-1)))
                
                frames[min_frame][frame_pointers[min_frame]] = 0
                frame_pointers[min_frame] += 1

                # if output frame is full write it in the output secondary memory and empty it
                if output_frame_pointer == elements_per_page:
                    output_pages[output_page_idx] = copy.deepcopy(frames[-1])
                    n_accesses += 1
                    
                    arrow_to_output = [{
                        "action": "draw",
                        "from": f"frame-{n_frames-1}-container",
                        "to": f"output-page-{output_page_idx}-container",
                        "id": f"arrow-output-frame-page-{output_page_idx}"
                    }]
                    
                    record(highlight=(("frames", n_frames-1, "all"),
                                    ("output_pages", output_page_idx, "all")),
                            arrows=arrow_to_output,
                            log_message=f"Output page {output_page_idx + 1} written.")
                    
                    arrow_remove_output = [{
                        "action": "remove",
                        "id": f"arrow-output-frame-page-{output_page_idx}"
                    }]
                    
                    record(arrows=arrow_remove_output)
                    
                    # Reset output frame with zeros
                    frames[-1] = [0] * elements_per_page
                    output_frame_pointer = 0
                    output_page_idx += 1

                # if an input frame is exhausted, load next page of the same run
                if frame_pointers[min_frame] >= len(frames[min_frame]):
                    if page_pointers[min_frame] < len(execution[min_frame]) - 1:
                        page_pointers[min_frame] += 1
                        page_in_run = page_pointers[min_frame]
                        global_page_idx = exec_idx * k * old_runs_size + min_frame * old_runs_size + page_in_run
                        
                        if global_page_idx < len(input_pages):
                            frames[min_frame] = copy.deepcopy(execution[min_frame][page_in_run])
                            n_accesses += 1
                            frame_pointers[min_frame] = 0
                            
                            # Remove the current arrow using the tracked ID
                            arrow_remove_old = [{
                                "action": "remove",
                                "id": current_arrow_ids[min_frame]
                            }]
                            
                            # Create new arrow and update the tracked ID
                            new_arrow_id = f"arrow-input-page-{global_page_idx}-frame-{min_frame}"
                            current_arrow_ids[min_frame] = new_arrow_id
                            
                            arrow_new = [{
                                "action": "draw",
                                "from": f"input-page-{global_page_idx}-container",
                                "to": f"frame-{min_frame}-container",
                                "id": new_arrow_id
                            }]
                            
                            record(highlight=(("input_pages", global_page_idx, "all"),
                                            ("frames", min_frame, "all")),
                                    arrows=arrow_remove_old + arrow_new,
                                    log_message=f"Input {global_page_idx + 1} loaded in frame {min_frame + 1}.")

            # write remaining elements in output frame if any
            if output_frame_pointer > 0:
                output_pages[output_page_idx] = copy.deepcopy(frames[-1])
                n_accesses += 1
                
                arrow_to_output = [{
                    "action": "draw",
                    "from": f"frame-{n_frames-1}-container",
                    "to": f"output-page-{output_page_idx}-container",
                    "id": f"arrow-output-frame-page-{output_page_idx}"
                }]
                
                record(highlight=(("frames", n_frames-1, "all"),
                                ("output_pages", output_page_idx, "all")),
                        arrows=arrow_to_output,
                        log_message=f"Final output page {output_page_idx + 1} written.")
                
                arrow_remove_output = [{
                    "action": "remove",
                    "id": f"arrow-output-frame-page-{output_page_idx}"
                }]
                record(arrows=arrow_remove_output)
                
                output_page_idx += 1

            # remove all remaining input arrows for this execution
            for j in range(len(execution)):
                if current_arrow_ids[j]:  # Only remove if arrow exists
                    arrow_remove = [{
                        "action": "remove",
                        "id": current_arrow_ids[j]
                    }]
                    record(arrows=arrow_remove)

            record(log_message=f"Run {exec_idx+1} completed.")

        # update next run size
        old_runs_size = current_runs_size

        record(log_message=f"Pass {pass_num} completed.")


    record(log_message="Sorting completed.")

    record(log_message="‎")
    record(log_message=f"Passes: {pass_num} (+ sort pass).")
    record(log_message=f"Memory accesses: {n_accesses}.")

    callback(steps)