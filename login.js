document.getElementById("loginForm").addEventListener("submit", function(e){
    e.preventDefault();

    let email = this.querySelector('input[name="email"]').value;
    let password = this.querySelector('input[name="password"]').value;

    fetch("/login/", {
        method: "POST",
        body: JSON.stringify({
            email: email,
            password: password
        }),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.querySelector('input[name="csrfmiddlewaretoken"]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert("Login successful! Welcome back.");
            // redirect to dashboard
            window.location.href = "/dashboard/";
        } else {
            alert("Login Failed: " + (data.message || "Invalid credentials"));
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred during login.");
    });
});