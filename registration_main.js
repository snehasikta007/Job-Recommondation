document.getElementById("registerForm").addEventListener("submit", function(e){
    e.preventDefault();

    let full_name = this.querySelector('input[name="full_name"]').value;
    let email = this.querySelector('input[name="email"]').value;
    let password = this.querySelector('input[name="password"]').value;
    let phone = this.querySelector('input[name="phone"]').value;

    fetch("/register/", {
        method: "POST",
        body: JSON.stringify({
            full_name: full_name,
            email: email,
            password: password,
            phone: phone
        }),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.querySelector('input[name="csrfmiddlewaretoken"]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert("Registration Successful! Welcome to AI Job Recommendation System.");
            // redirect to education page
            window.location.href = "/education/";
        } else {
            alert("Registration Failed: " + (data.message || "Unknown error"));
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred during registration.");
    });
});