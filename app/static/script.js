document.getElementById('review-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const form = event.target;
    const formData = {
        description: form.assignment_description.value,
        repo_url: form.github_repo_url.value,
        level: form.candidate_level.value
    };

    const submitBtn = document.getElementById('submit-btn');
    const loader = document.getElementById('loading');
    submitBtn.disabled = true;
    loader.style.display = 'block';

    try {
        const response = await fetch('/review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        document.getElementById("review-result").textContent = result.review;
        const filesContainer = document.getElementById("files-review");
        filesContainer.innerHTML = "";

        result.files.forEach(file => {
            const fileElement = document.createElement("div");
            fileElement.textContent = file;
            filesContainer.appendChild(fileElement);
        });
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("review-result").textContent = 'Error occurred while fetching the review.';
    } finally {
        submitBtn.disabled = false;
        loader.style.display = 'none';
    }
});
