// static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const savePdfBtn = document.getElementById('save-pdf-btn');
    const storyIdeaInput = document.getElementById('story-idea');
    const toneSelect = document.getElementById('tone-select');
    const comicContainer = document.getElementById('comic-strip-container');
    const loader = document.getElementById('loader');

    generateBtn.addEventListener('click', async () => {
        const storyIdea = storyIdeaInput.value.trim();
        const tone = toneSelect.value;

        if (!storyIdea) {
            alert('Please enter a story idea.');
            return;
        }

       
        loader.classList.remove('hidden');
        comicContainer.innerHTML = ''; 
        savePdfBtn.classList.add('hidden');
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ story_idea: storyIdea, tone: tone }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const comicPanels = await response.json();
            displayComic(comicPanels);
            savePdfBtn.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            comicContainer.innerHTML = `<p style="color: red;">Failed to generate comic. Please check the console for details or try again later. Error: ${error.message}</p>`;
        } finally {
           
            loader.classList.add('hidden');
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Comic';
        }
    });

    function displayComic(panels) {
        comicContainer.innerHTML = ''; 
        panels.forEach((panel, index) => {
            const panelElement = document.createElement('div');
            panelElement.classList.add('panel');
            
           g
            const imageSrc = `data:image/png;base64,${panel.image}`;

            panelElement.innerHTML = `
                <img src="${imageSrc}" alt="Comic panel ${index + 1}">
                <div class="caption">${panel.caption}</div>
            `;
            comicContainer.appendChild(panelElement);
        });
    }

    savePdfBtn.addEventListener('click', () => {
        // Use html2canvas to capture the comic container
        html2canvas(comicContainer).then(canvas => {
            const imgData = canvas.toDataURL('image/png');
            
            // Use jsPDF to create and save the PDF
            // Note: window.jspdf may vary based on CDN, check library docs if needed
            const { jsPDF } = window.jspdf;
            const pdf = new jsPDF();
            
            const imgProps= pdf.getImageProperties(imgData);
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

            pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
            pdf.save('ai-comic-strip.pdf');
        });
    });
});