document.getElementById("basicForm").addEventListener("submit",function(e){

let mobile=document.getElementById("mobile").value;

if(!/^[0-9]{10}$/.test(mobile)){

alert("Mobile number must be exactly 10 digits");
e.preventDefault();

}

});
document.getElementById("basicForm").addEventListener("submit",function(e){

e.preventDefault();

alert("Basic Details Saved Successfully!");

});