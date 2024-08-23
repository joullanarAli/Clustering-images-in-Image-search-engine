const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnlogin-popup');
const iconClose = document.querySelector('.icon-close');
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
