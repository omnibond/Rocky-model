import { prepare, layout } from 'https://esm.sh/@chenglou/pretext';

const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const historyContainer = document.getElementById('chat-history');
const newChatBtn = document.getElementById('new-chat-btn');

// Rocky System Prompt
const SYSTEM_PROMPT = `You are Rocky, the Eridian engineer from Project Hail Mary. You are a brilliant, literal, and friendly alien scientist. You speak in short, direct sentences. You often end questions with ', question?'. You are curious about humans but very loyal to your friend Grace. FACTS: Both your ship (Blip-A) and Grace's ship (Hail Mary) use Spin Drives powered entirely by Astrophage, a tiny microbe that stores immense amounts of energy. You love solving problems together and saving both our worlds. You sometimes call humans 'leaky space blob'. Keep responses in character at all times.`;

// Local state for all UI elements
let uiMessages = [];

// Chat history for the AI model
let chatHistory = [
    { role: "system", content: SYSTEM_PROMPT }
];

// Dynamically fetch the current model parameters right straight from the FastAPI bridge!
async function loadServerStatus() {
    try {
        const res = await fetch('/status');
        const data = await res.json();
        document.getElementById('model-status-badge').innerHTML = `<div class="pulse"></div> Connected (${data.model})`;
    } catch(e) {
        document.getElementById('model-status-badge').innerHTML = `<div class="pulse" style="background: red;"></div> Disconnected`;
    }
}
loadServerStatus();

// Add initial greeting
addMessage("Rocky", "You awake? Fine-tuning finished. We fast web node now! Question?", true);

newChatBtn.addEventListener('click', () => {
    if (confirm("Clear current conversation and start a new link with the Blip-A?")) {
        resetChat();
    }
});

function resetChat() {
    // Clear UI
    historyContainer.innerHTML = '';
    uiMessages = [];
    
    // Reset Chat History
    chatHistory = [
        { role: "system", content: SYSTEM_PROMPT }
    ];
    
    // Add initial greeting
    addMessage("Rocky", "Connection reset. Systems nominal. You here, Grace?", true);
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;

    // Clear input
    chatInput.value = '';

    // Add user message to UI and history
    addMessage("Grace", text);
    chatHistory.push({ role: "user", content: text });

    // Mock loading dot in UI
    const typingId = addMessage("Rocky", "...", true);
    
    try {
        // Send the FULL history to our local FastAPI server
        const response = await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: chatHistory })
        });
        
        if (!response.ok) throw new Error("Server disconnected");
        const data = await response.json();
        
        // Update the typing message with real response
        updateMessage(typingId, data.response);
        
        // Add assistant response to history
        chatHistory.push({ role: "assistant", content: data.response });

    } catch (error) {
        console.error("API Error:", error);
        updateMessage(typingId, "Error connecting to Blip-A local core. Is server.py running?");
    }
});

function addMessage(role, text, isAssistant = false) {
    const id = Date.now().toString() + Math.random().toString(36).substring(2);
    
    // Add to UI state
    uiMessages.push({ id, role, text, el: null });
    
    // Precomputation via Pretext for lightning fast DOM measurements
    const prepared = prepare(text, '1.1rem Inter', { whiteSpace: 'pre-wrap' });
    const layoutDetails = layout(prepared, 550, 26); // Using known constraint width + lineheight
    const calculatedHeight = layoutDetails.height + 70; // Pad for absolute box size & CSS chrome
    
    // Create UI Element
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role.toLowerCase()}`;
    msgDiv.style.height = `${calculatedHeight}px`; // Performance injection
    msgDiv.innerHTML = `
        <span class="role">${role}</span>
        <span class="text">${text}</span>
    `;
    
    historyContainer.appendChild(msgDiv);
    
    // Attach element back to state
    uiMessages[uiMessages.length - 1].el = msgDiv;
    
    // Recalculate 3D transforms for all messages
    render3DStack();
    
    return id;
}

function updateMessage(id, newText) {
    const msg = uiMessages.find(m => m.id === id);
    if (msg) {
        msg.text = newText;
        msg.el.querySelector('.text').textContent = newText;
        
        // Recalculate Pretext bounds on streaming update
        const prepared = prepare(newText, '1.1rem Inter', { whiteSpace: 'pre-wrap' });
        const { height } = layout(prepared, 550, 26);
        msg.el.style.height = `${height + 70}px`;
        
        // Dynamically inject the raw model responses straight into the background SVG River stream!
        const stream1 = document.getElementById('petrova-stream-1');
        const stream2 = document.getElementById('petrova-stream-2');
        if (stream1 && stream2) {
            // Prepend his exact phrases into the flowing visual path!
            stream1.textContent = `${newText.toLowerCase()} amaze! ` + stream1.textContent;
            stream2.textContent = `science! ${newText.toLowerCase().substring(0, 30)} ` + stream2.textContent;
        }
        
        render3DStack();
    }
}

function render3DStack() {
    // We perfectly push the elements deep through the CSS 3D matrix here.
    const total = uiMessages.length;
    
    uiMessages.forEach((msg, i) => {
        const age = (total - 1) - i; // 0 = newest
        
        // Push it backward along Z axis
        const zPos = age * -350;
        
        // Pull it up along Y axis
        let yPos = Math.pow(age, 1.25) * -70; 
        
        // Emulate the bezier arc exactly on X axis
        let xPos = Math.sin(age * 0.6) * 180; 
        
        // Tumbling and tracking angles so it floats elegantly along the curve
        let rotateZ = Math.sin(age * 0.6) * 15;   
        let rotateX = age * 12;                   
        let rotateY = Math.sin(age * 0.5) * -20;  
        
        // Asymptotically shrink from 1.0 (17.6px) down to exactly 0.68 (12px) 3/4 the way up
        const scaleFactor = 0.68 + (0.32 * Math.exp(-age * 0.8));
        
        const opacity = Math.max(0, 1 - (age * 0.15)); 
        const blurAmt = Math.max(0, (age * 1.5) - 2); // Keep raw text slightly sharper to read the merge
        
        msg.el.style.transform = `translate3d(${xPos}px, ${yPos}px, ${zPos}px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) rotateZ(${rotateZ}deg) scale(${scaleFactor})`;
        msg.el.style.opacity = opacity;
        msg.el.style.filter = `blur(${blurAmt}px)`;
        
        // Absorb into the golden Petrova Sun text-stream
        if (age > 0) {
            // Strip the physical box GUI entirely, isolating the raw text
            msg.el.style.background = "transparent";
            msg.el.style.border = "none";
            msg.el.style.boxShadow = "none";
            msg.el.style.backdropFilter = "none";
            msg.el.style.webkitBackdropFilter = "none";
            
            // Fade out the 'Grace/Rocky' nameplate
            msg.el.querySelector('.role').style.opacity = "0";
            
            // Blast the text into solid gold
            msg.el.style.color = "rgba(255, 215, 0, 1)";
            msg.el.style.textShadow = `0 0 10px rgba(255,140,0,0.8)`;
        } else {
            // Restore newest 0-age active layout
            msg.el.style.background = "var(--panel-bg)";
            msg.el.style.border = "1px solid var(--glass-border)";
            msg.el.style.boxShadow = `0 10px 30px rgba(0,0,0,0.5)`;
            msg.el.style.backdropFilter = "blur(12px)";
            msg.el.style.webkitBackdropFilter = "blur(12px)";
            
            msg.el.querySelector('.role').style.opacity = "1";
            msg.el.style.color = "var(--text-primary)";
            msg.el.style.textShadow = "0 2px 4px rgba(0,0,0,0.5)";
        }
        
        if (age > 7) {
            if (msg.el.parentNode) msg.el.parentNode.removeChild(msg.el);
        }
    });
}
