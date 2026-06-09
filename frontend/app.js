let currentPenColor = '#1a1a1a';
let canvasHasContent = false;
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d', { willReadFrequently: true });

lucide.createIcons();

function updateVal(id, labelId) {
    document.getElementById(labelId).textContent = document.getElementById(id).value;
}

function setPenColor(element, color) {
    document.querySelectorAll('.color-opt').forEach(el => el.classList.remove('active'));
    element.classList.add('active');
    currentPenColor = color;
}

function showToast(vibe) {
    const toast = document.getElementById('vibeToast');
    document.getElementById('vibeDesc').textContent = `Analyzed vibe: ${vibe}`;
    toast.classList.add('show');
    setTimeout(() => { toast.classList.remove('show'); }, 4000);
}

// ── MLOps AI Integration ────────────────────────────────────────────────────
async function analyzeAndStyle() {
    const text = document.getElementById('textInput').value;
    if (!text.trim()) {
        alert("Please enter text before using the Auto-Styler!");
        return;
    }

    const btn = document.getElementById('aiBtn');
    const originalText = btn.innerHTML;
    btn.classList.add('loading');
    btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Analyzing...';
    lucide.createIcons();

    try {
        const res = await fetch('/api/analyze-text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        if (!res.ok) throw new Error('Network response was not ok');
        const data = await res.json();
        
        // Apply ML Recommendations
        document.getElementById('fontSelect').value = data.font;
        document.getElementById('variation').value = data.flow;
        updateVal('variation', 'variationVal');
        document.getElementById('fontSize').value = data.size;
        updateVal('fontSize', 'fontSizeVal');
        
        // Set Color
        const colorOpts = document.querySelectorAll('.color-opt');
        colorOpts.forEach(el => {
            if (el.dataset.color === data.color) {
                setPenColor(el, data.color);
            }
        });

        showToast(data.vibe);
        
        // Auto-generate
        setTimeout(generateHandwriting, 500);

    } catch (err) {
        console.error(err);
        alert('Failed to connect to the ML service.');
    } finally {
        btn.classList.remove('loading');
        btn.innerHTML = originalText;
        lucide.createIcons();
    }
}

// ── Canvas Generation logic ─────────────────────────────────────────────────
function random(min, max) { return Math.random() * (max - min) + min; }

function drawChar(char, x, y, fontSize, fontFamily, color, variation) {
    ctx.save();
    const tilt = random(-0.02, 0.02) * (variation * 0.5);
    const yWobble = random(-1.5, 1.5) * (variation * 0.3);
    const xWobble = random(-0.8, 0.8) * (variation * 0.2);
    const opacity = random(0.88, 0.98);
    const scale = 0.998 + random(-0.005, 0.005);

    ctx.translate(x + xWobble, y + yWobble);
    ctx.rotate(tilt);
    ctx.scale(scale, 1);
    ctx.translate(-(x + xWobble), -(y + yWobble));

    ctx.fillStyle = color;
    ctx.globalAlpha = opacity * 0.1;
    ctx.font = `${fontSize}px "${fontFamily}"`;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.fillText(char, x + xWobble + 0.5, y + yWobble + 0.5);

    ctx.globalAlpha = opacity;
    ctx.fillText(char, x + xWobble, y + yWobble);
    ctx.restore();
}

async function generateHandwriting() {
    const text = document.getElementById('textInput').value;
    if (!text.trim()) return;

    const fontFamily = document.getElementById('fontSelect').value;
    const fontSize = parseInt(document.getElementById('fontSize').value);
    const variation = parseInt(document.getElementById('variation').value);

    await document.fonts.ready;

    // Canvas background
    ctx.fillStyle = '#faf5f0';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Subtle texture
    for (let i = 0; i < canvas.width; i += 8) {
        for (let j = 0; j < canvas.height; j += 8) {
            ctx.fillStyle = `rgba(0,0,0,${random(0.004, 0.012)})`;
            ctx.fillRect(i + random(-1, 1), j + random(-1, 1), random(2, 4), random(2, 4));
        }
    }

    // Ruled lines
    ctx.strokeStyle = '#d4d4d4';
    ctx.lineWidth = 0.8;
    const lineSpacing = fontSize * 2.3;
    for (let y = 110; y < canvas.height - 60; y += lineSpacing) {
        ctx.globalAlpha = random(0.4, 0.6);
        ctx.beginPath(); ctx.moveTo(65, y); ctx.lineTo(canvas.width - 65, y); ctx.stroke();
    }
    ctx.globalAlpha = 1.0;

    // Margins
    ctx.strokeStyle = '#b8b8b8'; ctx.lineWidth = 1.3;
    ctx.beginPath(); ctx.moveTo(65, 50); ctx.lineTo(65, canvas.height - 50); ctx.stroke();
    ctx.strokeStyle = '#d97777'; ctx.lineWidth = 0.7; ctx.globalAlpha = 0.5;
    ctx.beginPath(); ctx.moveTo(62, 50); ctx.lineTo(62, canvas.height - 50); ctx.stroke();
    ctx.globalAlpha = 1.0;

    // Text rendering
    const margin = 85;
    const lineHeight = fontSize * 2.4;
    let y = margin + fontSize;
    let x = margin;

    ctx.font = `${fontSize}px "${fontFamily}"`;
    const words = text.split(' ');

    for (let wordIdx = 0; wordIdx < words.length; wordIdx++) {
        const word = words[wordIdx];
        let wordWidth = 0;
        for (let char of word) {
            wordWidth += ctx.measureText(char).width + random(0.1, 0.5) * (variation * 0.2);
        }

        if (x !== margin && x + wordWidth > canvas.width - margin) {
            x = margin;
            y += lineHeight;
            if (y > canvas.height - 80) break;
        }

        for (let i = 0; i < word.length; i++) {
            if (y > canvas.height - 80) break;
            const char = word[i];
            drawChar(char, x, y, fontSize, fontFamily, currentPenColor, variation);
            x += ctx.measureText(char).width + random(0.1, 0.8) * (variation * 0.25);
        }

        if (wordIdx < words.length - 1) {
            x += ctx.measureText(' ').width * 0.7 + random(-0.5, 1.5) * (variation * 0.15);
        }

        if (x > canvas.width - margin) {
            x = margin;
            y += lineHeight;
            if (y > canvas.height - 80) break;
        }
    }

    canvasHasContent = true;
    document.getElementById('downloadBtn').disabled = false;
}

function downloadImage() {
    if (!canvasHasContent) return;
    const link = document.createElement('a');
    link.download = `Handwritten-Pro.png`;
    link.href = canvas.toDataURL('image/png', 1.0);
    link.click();
}
