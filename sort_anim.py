from browser import document, html, timer, alert
import heapq

bar_width = 20
bar_spacing = 5

def create_bars(arr):
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

def update_bars(arr, highlight=[]):
    max_val = max(arr) if arr else 1
    container = document["container"]
    for i, val in enumerate(arr):
        bar = container.children[i]
        height = (val / max_val) * 300
        bar.style.left = f"{i * (bar_width + bar_spacing)}px"
        bar.style.height = f"{height}px"
        bar.style.backgroundColor = "#FF5733" if i in highlight else "#4CAF50"

def bubble_sort(arr, callback):
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

def insertion_sort(arr, callback):
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

def k_way_merge_sort(arr, k, callback):
    if not arr:
        callback([])
        return

    steps = []

    def record(a):
        steps.append(a[:])

    n = len(arr)
    chunk_size = (n + k - 1) // k  # ceil division
    sorted_chunks = [sorted(arr[i*chunk_size:(i+1)*chunk_size]) for i in range(k)]
    heap = []
    pointers = [0] * k

    for i in range(k):
        if pointers[i] < len(sorted_chunks[i]):
            heapq.heappush(heap, (sorted_chunks[i][0], i))

    result = []

    while heap:
        val, i = heapq.heappop(heap)
        result.append(val)
        record(result + sum([sorted_chunks[j][pointers[j]:] for j in range(k)], []))
        pointers[i] += 1
        if pointers[i] < len(sorted_chunks[i]):
            heapq.heappush(heap, (sorted_chunks[i][pointers[i]], i))

    callback(steps)

def my_k_way_merge_sort(arr, k, n, callback):
    """
    arr: original data
    k: number of frames in main memory dedicated to input
    n: amount of elements per page
    """

    # initialize step memory
    steps = []

    # define step recording
    def record(a):
        steps.append(a[:])

    # divide original data in pages
    pages = []
    current_page = []

    for elem in arr:
        if len(current_page) < n:
            current_page.append(elem)
        else:
            pages.append(current_page)
            current_page = []

    # step 0: sort within pages

    for i in range(len(pages)):
        pages[i] = sorted(pages[i])


    callback(steps)

def animate(steps):
    i = 0
    def update():
        nonlocal i
        if i < len(steps):
            state, highlight = steps[i]
            update_bars(state, highlight)
            i += 1
        else:
            timer.clear_interval(interval_id)
    interval_id = timer.set_interval(update, 500)

def on_sort_trigger(ev):
    raw = document["arrayInput"].value
    try:
        arr = list(map(int, raw.strip().split(',')))
    except:
        alert("Invalid input. Please enter comma-separated integers.")
        return

    method = document["sortMethod"].value

    if method == "bubble":
        create_bars(arr)
        bubble_sort(arr, animate)

    elif method == "insertion":
        create_bars(arr)
        insertion_sort(arr, animate)

    elif method == "k-way":
        # create objects
        k_way_merge_sort(arr, 4, animate)

document.bind("start_sort", on_sort_trigger)
