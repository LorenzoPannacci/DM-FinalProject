from browser import document, html, timer, alert

bar_width = 20
bar_spacing = 5
bar_max_height = 100
height_per_block = 150

#######################
# MAIN MEMORY SORTING #
#######################

def main_create_bars(arr):
    """
    Create bars for main memory sorting.
    """

    container = document["container"]
    container.clear()

    # set the background color of the container
    container.style["backgroundColor"] = "#fafafa"

    max_val = max(arr) if arr else 1

    for i, val in enumerate(arr):
        height = (val / max_val) * 300
        bar = html.DIV(
            Class="bar",
            style={
                "height": f"{height}px",
                "left": f"{i * (bar_width + bar_spacing)}px"
            },
            id=f"bar-{i}"
        )

        container <= bar


def main_update_bars(arr, highlight=[]):
    """
    Update bars for main memory soring.
    """

    max_val = max(arr) if arr else 1
    container = document["container"]

    for i, val in enumerate(arr):
        bar = container.children[i]
        height = (val / max_val) * 300
        bar.style.left = f"{i * (bar_width + bar_spacing)}px"
        bar.style.height = f"{height}px"
        bar.style.backgroundColor = "#FF5733" if i in highlight else "#4CAF50"


def main_animate(steps):
    """
    Script for animation for main memory sorting.
    """

    i = 0
    def update():
        nonlocal i
        if i < len(steps):
            state, highlight = steps[i]
            main_update_bars(state, highlight)
            i += 1
        else:
            timer.clear_interval(interval_id)
    interval_id = timer.set_interval(update, 500)


def main_bubble_sort(arr, callback):
    """
    Main memory Bubblesort
    """

    steps = []

    def record(a, highlight=[]):
        steps.append((a[:], highlight[:]))

    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                record(a, [j, j + 1])

    # remove highlight
    record(a)

    callback(steps)


def main_insertion_sort(arr, callback):
    """
    Main memory insertion sort.
    """

    steps = []

    def record(a, highlight=[]):
        steps.append((a[:], highlight[:]))

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

    # remove highlight
    record(a)

    callback(steps)


############################
# SECONDARY MEMORY SORTING #
############################

def create_bars(pages=[[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]], frames=[[0,0,0,0],[0,0,0,0],[0,0,0,0]]):
    """
    Create bars for external sorting.
    """

    container = document["container"]
    container.clear()

    # helper to create a titled section
    secondary_height = max(len(pages) * height_per_block, 300)
    buffer_height = max(len(frames) * height_per_block, 300)

    def create_section(title_text, content_elements, height_px):
        section = html.DIV(Class="section", style={"height": f"{height_px}px"})
        title = html.H3(title_text, Class="section-title")
        section <= title
        for elem in content_elements:
            section <= elem
        return section

    # render a single array as bars with a label
    def render_array(arr, label, base_id):
        max_val = max(arr) if arr else 1

        # handle "empty" array
        if max_val == 0:
            max_val = 1

        array_container = html.DIV(Class="array-container")
        array_label = html.DIV(label, Class="array-label")
        array_container <= array_label

        for i, val in enumerate(arr):
            height = (val / max_val) * bar_max_height
            bar = html.DIV(
                Class="bar",
                style={
                    "height": f"{height}px",
                    "left": f"{i * (bar_width + bar_spacing)}px"
                },
                id=f"{base_id}-bar-{i}"
            )
            array_container <= bar

        return array_container

    # secondary memory (pages)
    secondary_elements = []
    for i, page in enumerate(pages):
        label = f"Page {i+1}"
        section = render_array(page, label, f"page-{i+1}")
        secondary_elements.append(section)

    secondary_memory_section = create_section("Secondary Memory", secondary_elements, secondary_height)

    # buffer (frames)
    buffer_elements = []
    for i, frame in enumerate(frames):
        label = f"Frame {i+1}"
        section = render_array(frame, label, f"frame-{i+1}")
        buffer_elements.append(section)

    buffer_section = create_section("Buffer", buffer_elements, buffer_height)

    # overall layout
    layout = html.DIV(Class="layout")
    layout <= secondary_memory_section
    layout <= buffer_section

    container <= layout


def update_bars(arr, highlight=[]):
    """
    Update bars for external sorting
    """

    # TODO

    return


def animate(steps):
    """
    Script for animation for external sorting.
    """

    # TODO

    return


def k_way_merge_sort(arr, k, n, callback):
    """
    arr: original data
    k: number of frames in main memory dedicated to input
    n: amount of elements per page
    """

    # initialize step memory
    steps = []

    # define step recording
    def record(highlight=[]):
        """
        Structure of highlight is a tuple of two elements.

        First is a dictionary that for each frame in the buffer says which element of
        the frame to highlight.

        Second is a dictionary that for each page in pages says which element of the page
        to highlight.
        """

        steps.append((pages, buffer, highlight))

    # divide original data in pages
    pages = []
    current_page = []

    for elem in arr:
        if len(current_page) < n:
            current_page.append(elem)
        else:
            pages.append(current_page)
            current_page = []

    # initialize buffer
    buffer = [[] for _ in range(k)]

    # record initial state
    record()

    # step 0: sort within pages

    for i in range(len(pages)):
        # load page into buffer
        buffer[0] = pages[i]
        record(highlight=({0: "all"}, {i: "all"}))

        # sort page in buffer (Bubblesort for visual clarity)
        for i in range(buffer[0]):
            for j in range(buffer[0] - i - 1):
                if buffer[0][j] > buffer[0][j + 1]:
                    buffer[0][j], buffer[0][j + 1] = buffer[0][j + 1], buffer[0][j]

                    record(highlight=({0: (j, j+1)},{}))

        # write back into page
        pages[i] = buffer[0]
        record(highlight=({0: "all"}, {i: "all"}))

    # steps k: merge pages

    # TODO

    callback(steps)


###############
# MAIN SCRIPT #
###############

def on_sort_trigger(ev):
    method = document["sortMethod"].value

    if method == "k-way":
        # create objects
        create_bars()
        k_way_merge_sort(arr, 4, animate)
    
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
