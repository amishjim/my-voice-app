document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileStatus = document.getElementById('file-status');
    const processBtn = document.getElementById('process-btn');
    const lyricsToggle = document.getElementById('lyrics-only');
    const resultArea = document.getElementById('result-area');
    const successMessage = document.getElementById('success-message');
    const downloadBtn = document.getElementById('download-btn');

    let jsonFiles = [];

    // Drag & Drop events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        handleFiles(e.dataTransfer.files);
    });

    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    function handleFiles(files) {
        // Accept any JSON files
        for (const file of files) {
            if (file.name.endsWith('.json')) {
                // Check if file already exists in the list
                if (!jsonFiles.some(f => f.name === file.name)) {
                    jsonFiles.push(file);
                }
            }
        }
        updateStatus();
    }

    function updateStatus() {
        if (jsonFiles.length > 0) {
            const fileNames = jsonFiles.map(f => f.name).join(', ');
            fileStatus.textContent = `Ready: ${jsonFiles.length} file(s) - ${fileNames}`;
            fileStatus.style.color = '#10b981'; // Success color
            processBtn.disabled = false;
        } else {
            fileStatus.textContent = 'Waiting for JSON files...';
            fileStatus.style.color = '#94a3b8'; // Muted color
            processBtn.disabled = true;
        }
    }

    processBtn.addEventListener('click', async () => {
        if (jsonFiles.length === 0) return;

        processBtn.disabled = true;
        processBtn.textContent = 'Processing...';

        const formData = new FormData();
        jsonFiles.forEach(file => {
            formData.append('files', file);
        });
        formData.append('lyrics_only', lyricsToggle.checked);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                successMessage.textContent = data.message || 'Processing complete!';
                downloadBtn.href = data.download_url;
                resultArea.classList.remove('hidden');
                processBtn.textContent = 'Done';
            } else {
                alert(`Error: ${data.error}`);
                processBtn.disabled = false;
                processBtn.textContent = 'Process Files';
            }

        } catch (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred.');
            processBtn.disabled = false;
            processBtn.textContent = 'Process Files';
        }
    });
});
