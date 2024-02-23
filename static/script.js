document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const results = document.getElementById('results');
    const loadingOverlay = document.getElementById('loading-overlay');


    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const file = formData.get('audio_file');

        if (file) {
            loadingOverlay.style.display = 'flex';
            const response = await fetch('/upload', { method: 'POST', body: formData });
            const data = await response.json();

            const cloudFunctionResponse = await fetch('/call_cloud_function');
            const cloudFunctionData = await cloudFunctionResponse.json();
           
            console.log(cloudFunctionResponse);

            loadingOverlay.style.display = 'none';

            if (cloudFunctionData.transcript) {
                document.getElementById('transcript').textContent = cloudFunctionData.transcript;
            }
            if (cloudFunctionData.summary) {
                document.getElementById('summary').textContent = cloudFunctionData.summary;
            }
            if (cloudFunctionData.sentiment) {
                document.getElementById('sentiment').textContent = cloudFunctionData.sentiment;
            }
        }
    });
});