from browser import document, html, timer

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

def bubble_sort(arr, callback):
    steps = []

    def record(a):
        steps.append(a[:])

    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                record(a)

    callback(steps)

def insertion_sort(arr, callback):
    steps = []

    def record(a):
        steps.append(a[:])

    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
            record(a)
        a[j + 1] = key
        record(a)

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
    if method == "bubble":
        bubble_sort(arr, animate)
    elif method == "insertion":
        insertion_sort(arr, animate)

document.bind("start_sort", on_sort_trigger)
