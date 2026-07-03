function analyzeResume() {
    let fileInput = document.getElementById("resumeFile");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please upload your resume first");
        return;
    }

    let formData = new FormData();
    formData.append("resume", file);

    // Get CSRF token from cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    let csrftoken = getCookie('csrftoken');

    // Show loading state
    document.getElementById("resultBox").style.display = "block";
    let scoreBar = document.getElementById("scoreBar");
    scoreBar.innerText = "Analyzing...";
    scoreBar.style.width = "100%";
    scoreBar.classList.add("loading");

    fetch("/analyze/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        scoreBar.classList.remove("loading");
        if (data.error) {
            alert(data.error);
            scoreBar.innerText = "Error";
            scoreBar.style.width = "0%";
            return;
        }

        // Update score (best match)
        let bestMatch = data.jobs && data.jobs.length > 0 ? data.jobs[0].match_score : 0;
        scoreBar.style.width = bestMatch + "%";
        scoreBar.innerText = bestMatch + "%";

        // Show extracted skills
        let skillsDiv = document.getElementById("skills");
        skillsDiv.innerHTML = "";
        if (data.extracted_skills) {
            data.extracted_skills.forEach(skill => {
                let span = document.createElement("span");
                span.innerText = skill;
                skillsDiv.appendChild(span);
            });
        }

        // Missing skills
        let missingDiv = document.getElementById("missingSkills");
        missingDiv.innerHTML = "";
        if (data.missing_skills) {
            data.missing_skills.forEach(skill => {
                let span = document.createElement("span");
                span.innerText = skill;
                missingDiv.appendChild(span);
            });
        }

        // Suggestions
        let sugList = document.getElementById("suggestions");
        sugList.innerHTML = "";
        if (data.suggestions) {
            data.suggestions.forEach(s => {
                let li = document.createElement("li");
                li.innerText = s;
                sugList.appendChild(li);
            });
        }
    })
    .catch(error => {
        scoreBar.classList.remove("loading");
        console.error("Error:", error);
        alert("An error occurred during analysis.");
        scoreBar.innerText = "Failed";
        scoreBar.style.width = "0%";
    });
}