                                            // USER //
const signUpForm = document.getElementById("signupForm");
const profileForm = document.getElementById("profileForm");
const loginForm = document.getElementById("loginForm");
const deleteForm = document.getElementById("deleteForm");

function saveUserDataToLocalStorage(){
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const address = document.getElementById("address").value.trim();
    const phone = document.getElementById("phone").value.trim();

    let valid = true
    let users= JSON.parse(localStorage.getItem("users")) || [];   
    
    const existingUser = users.find(u => u.email === email);
    if( password.length < 8 ||
        !(email.endsWith("@gmail.com")|| email.endsWith("@org.com")) ||
        address.length < 10 ||
        !(phone.length === 11 && phone.startsWith("01")) ||
        existingUser )
    {
        valid = false;
    }
    if(valid){
        const user = {
            username,
            email
        };
        users.push(user);
        localStorage.setItem("users", JSON.stringify(users));
    }
}
if(signUpForm){
    signUpForm.addEventListener("submit", saveUserDataToLocalStorage);
}

if(loginForm){
    loginForm.addEventListener("submit", async function(event){
        event.preventDefault(); 

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const error = document.getElementById("loginError");
        error.textContent = ""; 
        error.style.display = "none"; 
        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const result = await response.json();
            if (result.success) {
                localStorage.setItem("currentUserEmail", result.user.email);
                localStorage.setItem("currentUser", result.user.username);

                window.location.href = "/loggedInHome";
            } else {
                error.textContent = result.message ||"Invalid credentials.";
                error.style.display = "block";
            }
        } catch (error) {
            error.textContent = "Login failed due to a network/server error.";
            error.style.display = "block";
        }
    });  
}

function goToProfile(){
    const email = localStorage.getItem("currentUserEmail");
    if(email){
        document.getElementById("profileLink").href = "/profile?email="+email;
    }
}
function updateUserDataToLocalStorage(){
    const updatedUsername = document.getElementById("username").value;
    const currentEmail = localStorage.getItem("currentUserEmail");

    const updatedPassword = document.getElementById("password").value;
    const updatedAddress = document.getElementById("address").value.trim();
    const updatedPhone = document.getElementById("phone").value.trim();
    const errorDiv = document.getElementById("profileError");
    errorDiv.textContent = "";
    errorDiv.style.display = "none";

    if (updatedUsername.length < 3) {
        errorDiv.textContent = "Username must be at least 3 characters.";
    } else if (updatedPassword.length < 8) {
        errorDiv.textContent = "Password must be at least 8 characters.";
    } else if (updatedAddress.length < 10) {
        errorDiv.textContent = "Address must be at least 10 characters.";
    } else if (!(updatedPhone.length === 11 && updatedPhone.startsWith("01") && /^\d+$/.test(updatedPhone))) {
        errorDiv.textContent = "Invalid phone number. Must be 11 digits and start with '01'.";
    }

    if (errorDiv.textContent) {
        errorDiv.style.display = "block";
        return;
    }

    let users = JSON.parse(localStorage.getItem("users")) || [];
    for(let i = 0; i< users.length; i++){
        if(users[i].email === currentEmail){
            users[i].username = updatedUsername;
            users[i].password = updatedPassword;
            users[i].address = updatedAddress;
            users[i].phone = updatedPhone;
            break;
        }
    }
    localStorage.setItem("users" , JSON.stringify(users));
    localStorage.setItem("currentUser", updatedUsername); 
}
document.addEventListener("DOMContentLoaded", function(){
    if(profileForm){
    profileForm.addEventListener("submit" , updateUserDataToLocalStorage);
    }
});


function logOutAndRedirectToHome() {
    localStorage.removeItem("currentUser");
    localStorage.removeItem("currentUserEmail");
    sessionStorage.clear();
    window.location.href = "/";
}

function enableEdit(fieldId) {
    document.getElementById(fieldId).removeAttribute("readonly");
}

document.addEventListener("DOMContentLoaded", function(){
    const username = localStorage.getItem("currentUser");
    if(username){
        document.getElementById("welcomeUser").textContent = username;
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
    logOutAndRedirectToHome();
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

function removeFromCart(index){
    let cart = getCart();
    cart.splice(index,1);
    saveCart(cart);
    displayCart();
}

function clearCart(){
    saveCart([]);
    displayCart();
}

function displayCart(){
    cartItems.innerHTML = ""; 
    const cart = getCart();
    if(!cartItems) return;
    if(cart.length === 0){
        cartItems.innerHTML = "<p class='no-cart'>Your Cart is empty.</p>"
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
            img.className="cart-item-img";

            const name = document.createElement("h3");
            name.textContent = item.name;
            name.className="cart-item-name";

            const description = document.createElement("p");
            description.textContent = item.description;
            description.className="cart-item-description"

            const price = document.createElement("p");
            price.textContent = "EGP" + item.price;
            price.className="cart-item-price";

            const button = document.createElement("button");
            button.textContent = "Remove";
            button.className ="cart-item-remove-button";
            button.onclick = function(){
                removeFromCart(i);
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

