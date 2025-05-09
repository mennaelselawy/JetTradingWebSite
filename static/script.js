const signUpForm = document.getElementById("signupForm");
const profileForm = document.getElementById("profileForm");

function saveUserDataToLocalStorage(){
    //event.preventDefault(); event   //stop the default browser from submitting the form by html, So do it here manually by javascript
    
      //manually get the form values
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const address = document.getElementById("address").value.trim();
    const phone = document.getElementById("phone").value.trim();

    
    //to build an object in js as a struct in c++
    const user = {
        username,
        email,
        password,
        address,
        phone
    };

    let users= JSON.parse(localStorage.getItem("users")) || [];   //oring it with curly brackets to start with empty array if no users

    //check if user already exist by email so not to save it 
    const existingUser = users.find(u => u.email === email);
    if(!existingUser){
        users.push(user);
        localStorage.setItem("users", JSON.stringify(users));
    }
}

if(signUpForm){
    signUpForm.addEventListener("submit", saveUserDataToLocalStorage);
}




function showUserDataToEdit(){
    let users= JSON.parse(localStorage.getItem("users")) || [];  
    const currentUserEmail = localStorage.getItem("email");
    const user = users.find(u=>u.email === currentUserEmail);
    if(user){
        document.getElementById("username").value = user.username;
        document.getElementById("email").value = user.email;
        document.getElementById("password").value = user.password;
        document.getElementById("address").value = user.address;
        document.getElementById("phone").value = user.phone;
    }
}

function updateUserDataToLocalStorage(){
    const updatedUser ={
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
        email: document.getElementById("email").value,
        address: document.getElementById("address").value,
        phone: document.getElementById("phone").value
    };

    let users = JSON.parse(localStorage.getItem("users")) || [];
    
}

if(profileForm){
    showUserDataToEdit();
    profileForm.addEventListener("submit" , updateUserDataToLocalStorage);
}

