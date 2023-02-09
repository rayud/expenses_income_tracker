const usernameField=document.querySelector('#usernameField'); 
const username_feedBackArea = document.querySelector('.invalid-feedback');
const emailField = document.querySelector('#emailField');
const email_feedback_area = document.querySelector('.emailFeedBackArea');
const submitBtn = document.querySelector('.submit-btn');
emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value

    if (emailVal.length > 0) {
        fetch('/authentication/validate-email', {
            method: 'POST', 
            body: JSON.stringify({email: emailVal}), 
        })
        .then(response => response.json())
        .then((data) => {
            if(data.email_error) {

                submitBtn.disabled = true;
                if(emailField.classList.contains("is-valid")) {
                    emailField.classList.remove("is-valid"); 
                    email_feedback_area.classList.remove('valid-feedback');
                } 
                emailField.classList.add("is-invalid"); 
                email_feedback_area.classList.add('invalid-feedback');
                email_feedback_area.style.display = 'block';
                email_feedback_area.innerHTML = `<p>${data.email_error}</p>`;
            } 
            if(data.email_valid) {
                if(emailField.classList.contains("is-invalid")) {
                    emailField.classList.remove("is-invalid"); 
                    email_feedback_area.classList.remove('invalid-feedback');
                }
                emailField.classList.add("is-valid"); 
                email_feedback_area.classList.add('valid-feedback');
                email_feedback_area.style.display = 'block';
                email_feedback_area.innerHTML = `<p>${data.email_valid}</p>`;
                emailsubmit = true;
                submitBtn.disabled = false;
            }
        })
    }
})


usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value 
    console.log('username', usernameVal)
    
    if (usernameVal.length > 0) {
        fetch('/authentication/validate-username', {
            method: 'POST',
            body: JSON.stringify({ username: usernameVal}), 
        })
        .then(response => response.json())
        .then((data) => {
            console.log(data);

            if(data.username_error) {
                submitBtn.disabled = true;
                if(usernameField.classList.contains('is-valid')) {
                    usernameField.classList.remove('is-valid');
                    username_feedBackArea.classList.remove('valid-feedback');
                }
                usernameField.classList.add("is-invalid");
                username_feedBackArea.classList.add('invalid-feedback');
                username_feedBackArea.style.display = 'block'
                username_feedBackArea.innerHTML=`<p>${data.username_error}</p>`
            }

            if(data.username_valid) {
                if(usernameField.classList.contains('is-invalid')) {
                    usernameField.classList.remove('is-invalid');
                    username_feedBackArea.classList.remove('invalid-feedback');
                }
                usernameField.classList.add("is-valid");
                username_feedBackArea.classList.add('valid-feedback');
                username_feedBackArea.style.display = 'block'
                username_feedBackArea.innerHTML=`<p>${data.username_valid}</p>`
                submitBtn.disabled = false;
            }
        });
    }
});


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
