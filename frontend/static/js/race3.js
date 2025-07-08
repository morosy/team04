let currentPanel = 0;

function showPanel(index) {
    const panels = document.querySelectorAll('.horse-panel');
    panels.forEach((panel, i) => {
        panel.style.display = (i === index) ? 'block' : 'none';
    });

    // n着予想のnを更新
    const placeLabel = document.getElementById('place-label');
    if (placeLabel) {
        placeLabel.textContent = `${index + 1}着予想`;
    }

    currentPanel = index;
}

function nextPanel() {
    showPanel((currentPanel + 1) % 3);
}

function prevPanel() {
    showPanel((currentPanel + 2) % 3);
}

document.addEventListener('DOMContentLoaded', () => {
    showPanel(0);
});
