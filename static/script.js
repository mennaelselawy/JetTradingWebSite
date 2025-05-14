                                                   // USER //
const signUpForm = document.getElementById("signupForm");
const profileForm = document.getElementById("profileForm");
const loginForm = document.getElementById("loginForm");
const deleteForm = document.getElementById("deleteForm");

function saveUserDataToLocalStorage(){
    //event.preventDefault(); event   //stop the default browser from submitting the form by html, So do it here manually by javascript
    
      //manually get the form values
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    // const password = document.getElementById("password").value;
    // const address = document.getElementById("address").value.trim();
    // const phone = document.getElementById("phone").value.trim();

    //to build an object in js as a struct in c++
    const user = {
        username,
        email,
        // password,
        // address,
        // phone
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

function storeTheLoggedInUserEmail(){
    const email = document.getElementById("email").value.trim();
    let users = JSON.parse(localStorage.getItem("users")) || [];
    const loggedInUser = users.find(u => u.email === email);
    if(loggedInUser){
        localStorage.setItem("currentUserEmail", loggedInUser.email);
        localStorage.setItem("currentUser", JSON.stringify(loggedInUser)); 
    }
}
if(loginForm){
    loginForm.addEventListener("submit", storeTheLoggedInUserEmail);
}

// clear current user when browser closes
window.addEventListener("beforeunload", function(){
    localStorage.removeItem("currentUser");
    localStorage.removeItem("currentUserEmail");
})

function showUserDataToEdit(){
    // let users= JSON.parse(localStorage.getItem("users")) || [];  
    // const currentUserEmail = localStorage.getItem("currentUserEmail");
    // const user = users.find(u=>u.email === currentUserEmail);
    const user = JSON.parse(localStorage.getItem("currentUser"));
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
        // password: document.getElementById("password").value,
        email: document.getElementById("email").value,
        // address: document.getElementById("address").value,
        // phone: document.getElementById("phone").value
    };

    let users = JSON.parse(localStorage.getItem("users")) || [];
    const currentEmail = localStorage.getItem("currentUserEmail");
    for(let i = 0; i< users.length; i++){
        if(users[i].email === currentEmail){
            users[i] = updatedUser;
            break;
        }
    }
    localStorage.setItem("users" , JSON.stringify(users));
    localStorage.setItem("currentUser", JSON.stringify(updatedUser)); 
}
document.addEventListener("DOMContentLoaded", function(){
    showUserDataToEdit();
    if(profileForm){
    profileForm.addEventListener("submit" , updateUserDataToLocalStorage);
    }
});


function logOutAndRedirectToHome() {
    localStorage.removeItem("currentUser");
    localStorage.removeItem("currentUserEmail");
    window.location.href = "/";
}

function enableEdit(fieldId) {
    document.getElementById(fieldId).removeAttribute("readonly");
}

document.addEventListener("DOMContentLoaded", function(){
    const user = JSON.parse(localStorage.getItem("currentUser"));
    if(user){
        document.getElementById("welcomeUser").textContent = user.username;
    }
});

function deleteCurrentUserFromLocalStorage(){
    const currentEmail = localStorage.getItem("currentUserEmail");
    if(!currentEmail) return;
    let users = JSON.parse(localStorage.getItem("users")) || [];
    let newUsers =[];
    for(let i=0; i<users.length; i++){
        if(users[i].email !== currentEmail){
            newUsers.push(users[i]);
        }
    }
    users = newUsers;
    localStorage.setItem("users", JSON.stringify(users));
    localStorage.removeItem("currentUserEmail");
    localStorage.removeItem("currentUser");
}
function deleteAccount(){
    const currentEmail = localStorage.getItem("currentUserEmail");
    if(!currentEmail) return;
    deleteCurrentUserFromLocalStorage();
    const deleteEmailInput = document.getElementById("deleteEmail");
    if(deleteEmailInput){
        deleteEmailInput.name="email";
        deleteEmailInput.value = currentEmail;
    }
}
if(deleteForm){
    deleteForm.addEventListener("submit", deleteAccount);
}

                                                   // DEVICES //
// const devicesForm = document.getElementById("devicesForm");
// function displayAllDevices(){
//     fetch("/devices")
//     .then(response => response.json())      /* even though Flask sends JSON, the browser receives it as a raw HTTP response */
//     .then(data =>{
//         const deviceList = document.getElementById("devices-grid");
//         if(!deviceList) return;
//         deviceList.innerHTML="";   //clear the html to append mn awl w geded myb2ash feh garbage y3ny
//         data.forEach(device =>{
//             const deviceDiv = document.createElement("div");
//             deviceDiv.className ="device-div";
//             deviceDiv.innerHTML = device.image + "<br>" 
//             + device.name + "<br>" 
//             + device.description + "<br>" + 
//             "EGP"+ device.price;
//             deviceList.appendChild(deviceDiv);
//         })

//     })
// }
// if(devicesForm){
//     devicesForm.addEventListener("submit", displayAllDevices)
// }

                                            // CART //
const cartItems = document.getElementById("cart-items"); 
const buttons = document.querySelectorAll(".add-to-cart-button");

function goToCart(){
    const user = localStorage.getItem("currentUserEmail");
    if(!user){
        window.location.href ="/login";
    }
    else{
        window.location.href = "/cart";
    }
}


function getCurrentUserEmail(){
    return localStorage.getItem("currentUserEmail") || null;
}

function getCart(){
    const email = getCurrentUserEmail();
    if(!email) return [];
    const cartData = sessionStorage.getItem("cart_" + email);
    if(cartData)
    { 
        return JSON.parse(cartData);
    }     
    else{ 
         return[]; 
    }
}

function addToCart(product){
    const cart = getCart();
    cart.push(product);
    saveCart(cart);
}

function removeFromCart(product){
    let oldCart = getCart();
    let newCart = [];
    for(let i=0; i < oldCart.length; i++){
        if(oldCart[i].name !== product){
            newCart.push(oldCart[i]);
        }
    }
    saveCart(newCart);
    displayCart();
}

function clearCart(){
    saveCart([]);
    displayCart();
}

function displayCart(){
    cartItems.innerHTML = ""; //clear the cart first
    const cart = getCart();
    if(!cartItems) return;
    if(cart.length === 0){
        cartItems.innerHTML = "<p>Your Cart is empty.</p>"
        return;
    }
    else{
        for(let i=0; i< cart.length; i++){
            const item = cart[i];
            
            const card = document.createElement("div");
            card.className="device-card";

            const img = document.createElement("img");
            img.src = "static/images/" + item.image;
            img.alt = item.name;

            const name = document.createElement("h3");
            name.textContent = item.name;

            const description = document.createElement("p");
            description.textContent = item.description;

            const price = document.createElement("p");
            price.textContent = "EGP" + item.price;

            const button = document.createElement("button");
            button.textContent = "Remove";
            button.onclick = function(){
                removeFromCart(item.name);
            };

            card.appendChild(img);
            card.appendChild(name);
            card.appendChild(description);
            card.appendChild(price);
            card.appendChild(button);

            cartItems.appendChild(card);
        }
    }
}

function saveCart(cart){
    const email = getCurrentUserEmail();
    if(!email) return;
    sessionStorage.setItem("cart_"+ email , JSON.stringify(cart)); 
}


function addToCartButton(){
    for(let i=0; i< buttons.length; i++){
        buttons[i].addEventListener("click", function(){
            const product = {
                name: buttons[i].dataset.name,
                description: buttons[i].dataset.description,
                price: buttons[i].dataset.price,
                image: buttons[i].dataset.image
            };
            addToCart(product);
        });
    }
}
document.addEventListener("DOMContentLoaded" , function(){
    addToCartButton();
    if(cartItems){
        displayCart();
    }
})

const user = JSON.parse(localStorage.getItem("currentUser"));
if(user){
    document.getElementById("addToCartButton").style.display="inline-block"; 
}