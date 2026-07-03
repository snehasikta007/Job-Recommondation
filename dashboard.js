document.querySelectorAll(".job-card button").forEach(btn=>{
    btn.addEventListener("click",(e)=>{
        const jobCard = e.target.closest('.job-card');
        const jobId = jobCard.dataset.jobId;
        
        if (jobId) {
            fetch(`/apply/${jobId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    alert("Application Submitted Successfully!");
                    e.target.innerText = "Applied";
                    e.target.disabled = true;
                }
            });
        } else {
            alert("Application Submitted! (Demo Mode)");
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}