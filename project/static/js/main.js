// GET REFERENCE TO THE DOM ELEMENTS
const signUp = document.getElementById('sign-up'),
    signIn = document.getElementById('sign-in'),
    loginIn = document.getElementById('login-in'),
    loginUp = document.getElementById('login-up');

// ADD EVENT LISTENER
signUp.addEventListener('click', () => {
    // REMOVE CLASSES FIRST IF THEY EXIST
    loginIn.classList.remove('block');
    loginUp.classList.remove('none');

    //ADD CLASSES
    loginIn.classList.toggle('none');
    loginUp.classList.toggle('block');
});

signIn.addEventListener('click', () => {
    // REMOVE CLASSES FIRST IF THEY EXIST
    loginIn.classList.remove('none');
    loginUp.classList.remove('block');

    //ADD CLASSES
    loginIn.classList.toggle('block');
    loginUp.classList.toggle('none');
});