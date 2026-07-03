document.getElementById("upload").addEventListener("change", function(event) {
    
    const file = event.target.files[0];
    
    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            document.getElementById("profilePreview").src = e.target.result;
            document.querySelector(".overlay").computedStyleMap.display = "none";

        };

         reader.readAsDataURL(file);   
        
    }
});
document.querySelector(".basic-btn").addEventListener("click", function() {
    alert("Go to Basic Details section");
});
document.querySelector("button").addEventListener("click",function(){

alert("Complete your profile to get better AI job recommendations!");

});
