function scrollToUpload(){

document.getElementById("upload").scrollIntoView({

behavior:"smooth"

});

}


document.getElementById("resumeForm").addEventListener("submit",function(e){

e.preventDefault();

let file=document.getElementById("resumeFile").files[0];

if(!file){

alert("Please upload your resume");

return;

}

alert("Resume uploaded successfully! AI analysis will start.");
window.location.href = "/analyze/";

});