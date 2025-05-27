from browser import document, html, timer, alert

bar_width = 20
bar_spacing = 5
bar_max_height = 100

#######################
# MAIN MEMORY SORTING #
#######################

def main_create_bars(arr):
    """
    Create bars for main memory sorting.
    """

    container = document["container"]
    container.clear()
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

    callback(steps)


############################
# SECONDARY MEMORY SORTING #
############################

def create_bars(arr):
    """
    Create bars for external sorting.
    """

    # TODO

    return

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
    raw = document["arrayInput"].value
    try:
        arr = list(map(int, raw.strip().split(',')))
    except:
        alert("Invalid input. Please enter comma-separated integers.")
        return

    method = document["sortMethod"].value

    if method == "bubble":
        main_create_bars(arr)
        main_bubble_sort(arr, main_animate)

    elif method == "insertion":
        main_create_bars(arr)
        main_insertion_sort(arr, main_animate)

    elif method == "k-way":
        # create objects
        create_bars(arr)
        k_way_merge_sort(arr, 4, animate)

document.bind("start_sort", on_sort_trigger)
