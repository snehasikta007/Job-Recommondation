document.getElementById("educationForm").addEventListener("submit", function(e){

    e.preventDefault();

    alert("Education details saved successfully!");

    // redirect to skills page
    window.location.href = "../registation2/skills.html";

});