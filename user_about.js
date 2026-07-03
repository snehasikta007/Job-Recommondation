document.getElementById("fullname").addEventListener("input", function() {
    this.value = this.value.replace(/[^A-Za-z\s]/g, '');
});
document.getElementById("mobile").addEventListener("input", function() {
    this.value = this.value.replace(/[^0-9]/g, '');
});

document.getElementById("profileForm").addEventListener("submit", function(e){
    e.preventDefault();
    alert("Your details saved successfully!");
});

document.querySelector(".cancel").addEventListener("click", function(){
    window.location.reload();
});