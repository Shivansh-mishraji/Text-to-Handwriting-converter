const API_URL = "/api/analyze-text";
let canvas, ctx;
let currentVibe = null;

document.addEventListener("DOMContentLoaded", () => {
    lucide.createIcons();
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");
    
    // Initial draw to show paper background
    drawPaperBackground();
});

function drawPaperBackground() {
    // Fill off-white paper
    ctx.fillStyle = "#faf5f0";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw ruled lines
    ctx.strokeStyle = "rgba(0, 150, 255, 0.15)";
    ctx.lineWidth = 1;
    
    for (let y = 100; y < canvas.height; y += 40) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
    
    // Margin line
    ctx.strokeStyle = "rgba(255, 0, 0, 0.2)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(80, 0);
    ctx.lineTo(80, canvas.height);
    ctx.stroke();
}

async function analyzeAndStyle() {
    const text = document.getElementById("textInput").value;
    const btn = document.getElementById("aiBtn");
    
    if (!text.trim()) {
        showToast("Please enter some text first!", "warning");
        return;
    }
    
    btn.classList.add("loading");
    btn.innerHTML = `<i data-lucide="loader-2" class="animate-spin"></i> Analyzing...`;
    lucide.createIcons();
    
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) throw new Error("API Error");
        
        const data = await response.json();
        
        // Update UI
        document.getElementById("fontSelect").value = data.font;
        document.getElementById("fontSize").value = data.size;
        document.getElementById("fontSizeVal").textContent = data.size;
        document.getElementById("variation").value = data.flow;
        document.getElementById("variationVal").textContent = data.flow;
        
        // Update color
        document.querySelectorAll(".color-opt").forEach(opt => {
            if (opt.dataset.color === data.color) {
                opt.classList.add("active");
            } else {
                opt.classList.remove("active");
            }
        });
        
        showToast(`AI Auto-Styler Applied! Vibe: ${data.vibe}`, "success");
        currentVibe = data.vibe;
        
        // Auto generate
        generateHandwriting(data.color);
        
    } catch (error) {
        console.error("API Error (Likely running as static site):", error);
        showToast("Static Mode: Defaulting to standard style", "warning");
        generateHandwriting();
    } finally {
        btn.classList.remove("loading");
        btn.innerHTML = `<i data-lucide="sparkles"></i> Auto-Style with AI`;
        lucide.createIcons();
    }
}

function updateVal(inputId, displayId) {
    document.getElementById(displayId).textContent = document.getElementById(inputId).value;
}

function setPenColor(element, color) {
    document.querySelectorAll(".color-opt").forEach(opt => opt.classList.remove("active"));
    element.classList.add("active");
    // Generate immediately if text exists
    if (document.getElementById("textInput").value.trim()) {
        generateHandwriting(color);
    }
}

function getActiveColor() {
    const activeOpt = document.querySelector(".color-opt.active");
    return activeOpt ? activeOpt.dataset.color : "#1a1a1a";
}

function wrapText(context, text, x, y, maxWidth, lineHeight, flowVariation) {
    const paragraphs = text.split('\n');
    let currentY = y;
    
    for (let p = 0; p < paragraphs.length; p++) {
        let words = paragraphs[p].split(' ');
        let line = '';
        
        for (let n = 0; n < words.length; n++) {
            let testLine = line + words[n] + ' ';
            let metrics = context.measureText(testLine);
            let testWidth = metrics.width;
            
            if (testWidth > maxWidth && n > 0) {
                // Apply subtle random offset for natural flow
                let yOffset = (Math.random() - 0.5) * flowVariation;
                context.fillText(line, x, currentY + yOffset);
                line = words[n] + ' ';
                currentY += lineHeight;
            } else {
                line = testLine;
            }
        }
        let yOffset = (Math.random() - 0.5) * flowVariation;
        context.fillText(line, x, currentY + yOffset);
        currentY += lineHeight * 1.5; // Paragraph spacing
    }
}

function generateHandwriting(overrideColor = null) {
    const text = document.getElementById("textInput").value;
    if (!text.trim()) {
        showToast("Please enter some text to generate handwriting.", "warning");
        return;
    }
    
    drawPaperBackground();
    
    const fontName = document.getElementById("fontSelect").value;
    const fontSize = parseInt(document.getElementById("fontSize").value);
    const color = overrideColor || getActiveColor();
    const flow = parseInt(document.getElementById("variation").value);
    
    ctx.font = `${fontSize}px "${fontName}", cursive`;
    ctx.fillStyle = color;
    
    // Add subtle shadow for ink bleed effect
    ctx.shadowColor = color;
    ctx.shadowBlur = 0.5;
    ctx.shadowOffsetX = 0.2;
    ctx.shadowOffsetY = 0.2;
    
    const startX = 100; // After margin
    const startY = 90; // Align with first ruled line
    const maxWidth = canvas.width - startX - 40;
    
    // Line height closely matches the ruled lines (40px)
    const lineHeight = 40; 
    
    wrapText(ctx, text, startX, startY, maxWidth, lineHeight, flow);
    
    // Enable download
    const dlBtn = document.getElementById("downloadBtn");
    dlBtn.disabled = false;
    dlBtn.classList.remove("btn-secondary");
    dlBtn.classList.add("btn-primary");
}

function downloadImage() {
    const link = document.createElement('a');
    link.download = 'handwriting.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
}

function showToast(message, type) {
    const toast = document.getElementById("vibeToast");
    const title = document.getElementById("vibeTitle");
    const desc = document.getElementById("vibeDesc");
    
    toast.style.borderColor = type === 'error' ? 'var(--danger)' : 'var(--accent)';
    
    if (type === 'success') {
        title.textContent = "AI Auto-Styler Applied";
        desc.textContent = message;
    } else if (type === 'warning') {
        title.textContent = "Attention Needed";
        desc.textContent = message;
    } else {
        title.textContent = "Error";
        desc.textContent = message;
    }
    
    toast.classList.add("show");
    
    setTimeout(() => {
        toast.classList.remove("show");
    }, 4000);
}
