document.getElementById("skillsForm").addEventListener("submit", function(e){
    e.preventDefault();

    let skills = this.querySelector('input[type="text"]').value;

    fetch("/skills/", {
        method: "POST",
        body: JSON.stringify({
            skills: skills
        }),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert("Skills saved successfully!");
            window.location.href = "/dashboard/";
        } else {
            alert("Failed to save skills.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred.");
    });
});