document.getElementById("educationForm").addEventListener("submit", function(e){
    e.preventDefault();

    let formData = new FormData(this);

    fetch("/education/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": formData.get("csrfmiddlewaretoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert("Education details saved successfully!");
            // redirect to skills page
            window.location.href = "/skills/";
        } else {
            alert("Failed to save education details: " + (data.error || "Unknown error"));
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while saving education details.");
    });
});