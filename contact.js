document.getElementById("contactForm").addEventListener("submit", function(e) {

    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;

    if(name === "" || email === "" || message === "") {
        alert("❌ Please fill all required fields");
        return;
    }

    alert("✅ Your issue has been submitted successfully!");

});