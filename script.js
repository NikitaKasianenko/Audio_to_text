document.getElementById('selectFileBtn').addEventListener('click', () => {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function () {
    const fileNameElement = document.getElementById('fileName');
    const file = this.files[0];
    
    if (file) {
        fileNameElement.textContent = `Selected file: ${file.name}`;
    } else {
        fileNameElement.textContent = '';
    }
});

document.getElementById('uploadForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files.length) {
        alert('Please select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:5000/transcribe', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        
        if (response.ok) {
            document.getElementById('audioText').value = result.transcription;
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to upload file.');
    }
});
