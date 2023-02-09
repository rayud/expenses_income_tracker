const showPasswordField = document.querySelector('.showPasswordToggle'); 
const PasswordField = document.querySelector('#passwordField'); 

const handleToggleInput = (e) => {
    if (showPasswordField.textContent == "SHOW") {
        PasswordField.setAttribute('type', 'text')
        showPasswordField.textContent = "HIDE"
    } else {
        PasswordField.setAttribute('type', 'password')
        showPasswordField.textContent = "SHOW"
    }
}

showPasswordField.addEventListener('click', handleToggleInput);
