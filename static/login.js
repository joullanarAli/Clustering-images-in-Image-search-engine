const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnlogin-popup');
const iconClose = document.querySelector('.icon-close');
const loginButton = document.querySelector('#loginButton');
const logoutButton = document.querySelector('#logoutButton');
const loginError = document.getElementById('loginError');
const registerError = document.getElementById('registerError');
registerLink.addEventListener('click',() => {
    wrapper.classList.add('active');
});

loginLink.addEventListener('click',() => {
    wrapper.classList.remove('active');
});

btnPopup.addEventListener('click',() => {
    document.getElementById('search').style.display = 'none';
    wrapper.classList.add('active-popup');
    
});
iconClose.addEventListener('click',() => {
    document.getElementById('search').style.display = 'block';
    wrapper.classList.remove('active-popup');
    
});


async function loginUser() {
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('loggedIn', 'true'); // Save login state
        document.getElementById('loginButton').style.display = 'none';
        document.getElementById('logoutButton').style.display = 'block';
        window.location.href = '/static/index.html';
    } else {
        const error = await response.json();
        loginError.textContent = 'Login failed: ' + error.detail;
        
    }
}

async function registerUser() {
    
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('registerConfirmPassword').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
    });

    if (response.ok) {
        const data = await response.json();
        loginButton.style.display = 'none';
        localStorage.setItem('loggedIn', 'true'); // Save login state
        document.getElementById('loginButton').style.display = 'none';
        document.getElementById('logoutButton').style.display = 'block';
        window.location.href = '/static/index.html';
        
    } else {
        const error = await response.json();
        registerError.textContent = 'Registration failed: ' + error.detail;
        
    }
}

function logoutUser() {
    localStorage.setItem('loggedIn', 'false'); // Set login state to false
    document.getElementById('loginButton').style.display = 'block';
    document.getElementById('logoutButton').style.display = 'none';
    window.location.href = '/static/index.html'; // Redirect to home page
}

window.onload = () => {
    const loggedIn = localStorage.getItem('loggedIn') === 'true';
    console.log('LoggedIn:', loggedIn); // Debug log
    if (loggedIn) {
        document.getElementById('loginButton').style.display = 'none';
        document.getElementById('logoutButton').style.display = 'block';
    } else {
        document.getElementById('loginButton').style.display = 'block';
        document.getElementById('logoutButton').style.display = 'none';
    }
};