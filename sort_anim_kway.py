from browser import document, html, timer
import heapq

def create_bars(arr):
    container = document["container"]
    container.clear()
    max_val = max(arr) if arr else 1
    for val in arr:
        height = (val / max_val) * 300
        bar = html.DIV(Class="bar", style={"height": f"{height}px", "width": "20px"})
        container <= bar

def update_bars(arr, highlight=[]):
    container = document["container"]
    for i, val in enumerate(arr):
        bar = container.children[i]
        bar.style.height = f"{(val / max(arr)) * 300}px"
        bar.style.backgroundColor = "#FF5733" if i in highlight else "#4CAF50"

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

def animate(steps):
    i = 0
    def update():
        nonlocal i
        if i < len(steps):
            update_bars(steps[i])
            i += 1
        else:
            timer.clear_interval(interval_id)
    interval_id = timer.set_interval(update, 300)

def on_sort_trigger(ev):
    raw = document["arrayInput"].value
    try:
        arr = list(map(int, raw.strip().split(',')))
    except:
        alert("Invalid input. Please enter comma-separated integers.")
        return

    create_bars(arr)

    method = document["sortMethod"].value
    if method == "kway":
        k_way_merge_sort(arr, 4, animate)  # Use k=4 for demonstration

document.bind("start_sort", on_sort_trigger)
