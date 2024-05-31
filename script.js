function generateImage() {
    const prompt = document.getElementById('prompt').value;
    const resultDiv = document.getElementById('result');
    const img = document.getElementById('generated-image');

    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        img.src = url;
        resultDiv.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to generate image. Please try again.');
    });
}
 
