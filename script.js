window.isAnimationRunning = false;
window.animationPaused = false;
let currentTimeoutId = null;

function run_sort() {
    document.dispatchEvent(new Event("start_sort"));
}

function updateInputVisibility() {
    const method = document.getElementById("sortMethod").value;
    const arrayInputFields = document.getElementById("arrayInputFields");
    const kWayFields = document.getElementById("kWayFields");

    if (method === "k-way") {
        arrayInputFields.style.display = "none";
        kWayFields.style.display = "block";
    } else {
        arrayInputFields.style.display = "block";
        kWayFields.style.display = "none";
    }
}

function validateInteger(input) {
    const value = input.value.trim();
    const isValid = /^-?\d+$/.test(value);
    const warning = document.getElementById(input.id + "Warning");

    if (value === "") {
        input.style.borderColor = "";
        warning.style.display = "none";
        if (input.id === "n_pages") {
            updatePageInputs();
        }
    } else if (!isValid) {
        input.style.borderColor = "red";
        warning.style.display = "inline";
    } else {
        input.style.borderColor = "";
        warning.style.display = "none";
        if (input.id === "n_pages") {
            updatePageInputs();
        }
    }
}

function validateIntegerList(input) {
    const value = input.value.trim();
    const isValid = value.split(',').every(num => /^-?\d+$/.test(num.trim()));
    const warning = document.getElementById(input.id + "Warning");

    if (value === "") {
        input.style.borderColor = "";
        warning.style.display = "none";
    } else if (!isValid) {
        input.style.borderColor = "red";
        warning.style.display = "inline";
    } else {
        input.style.borderColor = "";
        warning.style.display = "none";
    }
}

function updatePageInputs() {
    const nPagesInput = document.getElementById("n_pages");
    const container = document.getElementById("pageInputsContainer");
    const warning = document.getElementById("n_pagesWarning");
    const manualCheckbox = document.getElementById("manual_populate");

    container.innerHTML = "";

    const value = nPagesInput.value.trim();
    const isValid = /^-?\d+$/.test(value);
    const nPages = parseInt(value);

    if (value === "" || !isValid || nPages <= 0 || !manualCheckbox.checked) return;

    const divider = document.createElement("hr");
    divider.style.border = "none";
    divider.style.borderTop = "1px solid lightgray";
    divider.style.marginTop = "20px";
    divider.style.marginBottom = "20px";
    container.appendChild(divider);

    for (let i = 0; i < nPages; i++) {
        const wrapper = document.createElement("div");
        wrapper.style.marginTop = "10px";

        const label = document.createElement("label");
        label.innerText = `Page ${i + 1}:`;
        wrapper.appendChild(label);

        const input = document.createElement("input");
        input.type = "text";
        input.placeholder = "Enter numbers e.g. 5,3,8,6";
        input.id = `page_${i + 1}`;
        input.oninput = function() {
            validateIntegerList(this);
        };
        input.className = "w-full p-2 border rounded mt-1";
        wrapper.appendChild(input);

        const span = document.createElement("span");
        span.className = "warning";
        span.id = `page_${i + 1}Warning`;
        span.innerText = "Please enter only comma-separated integers.";
        wrapper.appendChild(span);

        container.appendChild(wrapper);
    }
}

function updateSpeedDisplay() {
    const slider = document.getElementById("speedRange");
    const speedValue = document.getElementById("speedValue");
    animationSpeed = parseInt(slider.value);
    speedValue.textContent = `${animationSpeed} ms`;
}

function toggleAnimation() {
    const btn = document.getElementById("stopResumeBtn");

    if (!window.animationPaused) {
        // Stop animation
        window.animationPaused = true;
        if (currentTimeoutId) {
            clearTimeout(currentTimeoutId);
        }
        btn.textContent = "Resume";
        btn.className = "flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition-colors";
    } else {
        // Resume animation
        window.animationPaused = false;
        btn.textContent = "Stop";
        btn.className = "flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition-colors";
    }
}

window.enableStopButton = function() {
    const btn = document.getElementById("stopResumeBtn");
    btn.disabled = false;
    btn.className = "flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition-colors";
    window.isAnimationRunning = true;
    window.animationPaused = false;
}

window.disableStopButton = function() {
    const btn = document.getElementById("stopResumeBtn");
    btn.disabled = true;
    btn.textContent = "Stop";
    btn.className = "flex-1 bg-gray-400 text-white font-bold py-2 px-4 rounded transition-colors cursor-not-allowed";
    window.isAnimationRunning = false;
    window.animationPaused = false;
}

function clearConsole() {
    document.getElementById("console").innerHTML = "";
}