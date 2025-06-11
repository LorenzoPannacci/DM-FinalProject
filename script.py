from browser import document, alert
from utils import *
from main_memory import *
from secondary_memory import *
import random


def get_manual_inputs():
    n_pages = int(document["n_pages"].value)
    pages = []

    for i in range(1, n_pages + 1):
        input_id = f"page_{i}"
        if input_id in document:
            raw_input = document[input_id].value.strip()

            if raw_input:
                try:
                    numbers = [int(x.strip()) for x in raw_input.split(",")]
                    pages.append(numbers)

                except ValueError:
                    alert(f"Invalid input in Page {i}. Please enter only integers.")
                    return
                
            else:
                pages.append([])
        else:
            pages.append([])

    return pages


def on_sort_trigger(ev):
    method = document["sortMethod"].value
    document.getElementById("console").innerHTML = ""

    if method == "k-way":
        try:
            n_pages = int(document["n_pages"].value)
            n_frames = int(document["n_frames"].value)
            elements_per_page = int(document["elements_per_page"].value)

        except ValueError:
            alert("Please enter valid integers for all K-way merge sort parameters.")
            return

        if n_frames <= 2:
            alert("Number of frames in the buffer must be at least 3!")
            return

        if n_pages <= 1:
            alert("Number of pages must be at least 2!")
            return

        if not document["manual_populate"].checked:
            input_pages = []
            for i in range(n_pages, 0, -1):
                page = [random.randint(1, elements_per_page * n_pages * 10) for _ in range(elements_per_page)]
                input_pages.append(page)

        else:
            input_pages = get_manual_inputs()
            if not input_pages:
                return

        # Initialize output pages with same structure as input but empty values
        output_pages = [[0] * elements_per_page for _ in range(n_pages)]
        frames = [[0] * elements_per_page for _ in range(n_frames)]
        
        create_bars(input_pages, output_pages, frames)
        k_way_merge_sort(input_pages, output_pages, frames, n_pages, n_frames, elements_per_page, animate)
    
    else:
        raw = document["arrayInput"].value
        try:
            arr = list(map(int, raw.strip().split(',')))

        except:
            alert("Invalid input. Please enter comma-separated integers.")
            return

        if method == "bubble":
            main_create_bars(arr)
            main_bubble_sort(arr, main_animate)
            
        elif method == "insertion":
            main_create_bars(arr)
            main_insertion_sort(arr, main_animate)


document.bind("start_sort", on_sort_trigger)