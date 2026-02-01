// Wait for the DOM to load before attaching events
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('generateBtn');
    
    btn.addEventListener('click', generate);
});

async function generate() {
    const memoryInput = document.getElementById('memory');
    const outputDiv = document.getElementById('output');
    const btn = document.getElementById('generateBtn');
    
    const memory = memoryInput.value.trim();
    
    // Validation
    if (!memory) {
        outputDiv.innerText = "Please write a memory first! ❤️";
        outputDiv.style.color = "#d63384";
        return;
    }
    
    // UI Loading State
    outputDiv.style.color = "#444";
    outputDiv.innerText = "Consulting the love algorithms...";
    btn.disabled = true;
    btn.innerText = "Thinking...";
    
    try {
        // Call the Backend API
        const res = await fetch('/api/index', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({memory: memory})
        });
        
        const data = await res.json();
        
        // Display Result
        outputDiv.innerText = data.message;
        
    } catch (err) {
        outputDiv.innerText = "Something went wrong. But I still love you.";
        console.error(err);
    } finally {
        // Reset Button
        btn.disabled = false;
        btn.innerText = "Generate Gift";
    }
}