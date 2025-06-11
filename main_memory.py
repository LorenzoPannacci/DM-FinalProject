from browser import document, html, timer, window
from utils import *

height_per_block = 150


def main_create_bars(arr):
    """
    Create bars for main memory sorting.
    """

    container = document["container"]
    container.clear()
    container.style["backgroundColor"] = "#e0f7fa"

    max_val = max(arr) if arr else 1

    # create section
    main_elements = []
    main_elements.append(render_array(arr, None, f"main", max_val))

    main_memory_section = create_section("Main Memory", main_elements)

    # Create flexible layout
    layout = html.DIV(Class="memory-layout")
    layout <= main_memory_section

    container <= layout


def main_update_bars(arr, highlight=[]):
    """
    Update bars for main memory soring.
    """

    max_val = max(arr) if arr else 1
    
    # Calculate width and spacing as percentage
    num_bars = len(arr)
    if num_bars > 0:
        bar_width_percent = 80 / num_bars
        spacing_percent = 20 / (num_bars + 1)

    else:
        bar_width_percent = 0
        spacing_percent = 0

    for i, val in enumerate(arr):
        bar_id = f"main-bar-{i}"
        bar = document.getElementById(bar_id)

        height = (val / max_val) * 100
        left_position = spacing_percent + i * (bar_width_percent + spacing_percent)
        
        bar.style.left = f"{left_position}%"
        bar.style.width = f"{bar_width_percent}%"
        bar.style.height = f"{height}px"
        bar.style.backgroundColor = "#FF5733" if i in highlight else "#4CAF50"

        text_element = document.getElementById(f"main-bar-text-{i}")
        if text_element:
            text_element.innerHTML = str(val)


def main_animate(steps):

    i = 0

    def update():

        nonlocal i
        if i < len(steps):
            paused = window.animationPaused if hasattr(window, 'animationPaused') else False
            if not paused:
                if len(steps[i]) == 3:  # New format with log
                    state, highlight, log_message = steps[i]

                else:  # Old format without log
                    state, highlight = steps[i]
                    log_message = None
                
                main_update_bars(state, highlight)
                if log_message:
                    log_to_console(log_message)
                
                i += 1
                if i < len(steps):
                    speed = int(document["speedRange"].value)
                    timer.set_timeout(update, speed)

                else:
                    window.disableStopButton()
            else:
                timer.set_timeout(update, 100)
    
    window.enableStopButton()
    update()


def main_bubble_sort(arr, callback):
    """
    Main memory Bubblesort
    """
    steps = []

    def record(a, highlight=[], log_message=None):
        steps.append((a[:], highlight[:], log_message))

    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                record(a, [j, j + 1])

    record(a)
    callback(steps)


def main_insertion_sort(arr, callback):
    """
    Main memory insertion sort.
    """

    steps = []

    def record(a, highlight=[], log_message=None):
        steps.append((a[:], highlight[:], log_message))

    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
            record(a, [j + 1, j + 2])
            
        a[j + 1] = key
        record(a, [j + 1])

    record(a)
    callback(steps)