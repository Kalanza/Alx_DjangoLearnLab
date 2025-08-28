// Register Form JavaScript Enhancement
document.addEventListener('DOMContentLoaded', function() {
    console.log('Register form loaded');
    
    // Get register form elements
    const registerForm = document.querySelector('.register-form');
    const usernameField = document.querySelector('input[name="username"]');
    const emailField = document.querySelector('input[name="email"]');
    const firstNameField = document.querySelector('input[name="first_name"]');
    const lastNameField = document.querySelector('input[name="last_name"]');
    const password1Field = document.querySelector('input[name="password1"]');
    const password2Field = document.querySelector('input[name="password2"]');
    const registerButton = document.querySelector('.register-btn');
    
    if (registerForm) {
        // Add form validation
        registerForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Clear previous error styling
            clearErrors();
            
            // Validate required fields
            if (!usernameField.value.trim()) {
                showFieldError(usernameField, 'Username is required');
                isValid = false;
            } else if (usernameField.value.length < 3) {
                showFieldError(usernameField, 'Username must be at least 3 characters');
                isValid = false;
            }
            
            if (!emailField.value.trim()) {
                showFieldError(emailField, 'Email is required');
                isValid = false;
            } else if (!isValidEmail(emailField.value)) {
                showFieldError(emailField, 'Please enter a valid email address');
                isValid = false;
            }
            
            if (!password1Field.value) {
                showFieldError(password1Field, 'Password is required');
                isValid = false;
            } else if (password1Field.value.length < 8) {
                showFieldError(password1Field, 'Password must be at least 8 characters');
                isValid = false;
            }
            
            if (!password2Field.value) {
                showFieldError(password2Field, 'Password confirmation is required');
                isValid = false;
            } else if (password1Field.value !== password2Field.value) {
                showFieldError(password2Field, 'Passwords do not match');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
                return false;
            }
            
            // Show loading state
            showLoadingState();
        });
        
        // Real-time validation
        usernameField.addEventListener('blur', function() {
            if (!this.value.trim()) {
                showFieldError(this, 'Username is required');
            } else if (this.value.length < 3) {
                showFieldError(this, 'Username must be at least 3 characters');
            } else {
                clearFieldError(this);
            }
        });
        
        emailField.addEventListener('blur', function() {
            if (!this.value.trim()) {
                showFieldError(this, 'Email is required');
            } else if (!isValidEmail(this.value)) {
                showFieldError(this, 'Please enter a valid email address');
            } else {
                clearFieldError(this);
            }
        });
        
        password1Field.addEventListener('input', function() {
            const password = this.value;
            updatePasswordStrength(password);
            
            if (password2Field.value && password !== password2Field.value) {
                showFieldError(password2Field, 'Passwords do not match');
            } else if (password2Field.value) {
                clearFieldError(password2Field);
            }
        });
        
        password2Field.addEventListener('blur', function() {
            if (!this.value) {
                showFieldError(this, 'Password confirmation is required');
            } else if (this.value !== password1Field.value) {
                showFieldError(this, 'Passwords do not match');
            } else {
                clearFieldError(this);
            }
        });
        
        // Add input focus effects
        const inputs = registerForm.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
            });
        });
    }
    
    // Utility functions
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    function updatePasswordStrength(password) {
        const strengthIndicator = document.querySelector('.password-strength');
        if (!strengthIndicator) {
            createPasswordStrengthIndicator();
        }
        
        let strength = 0;
        const checks = [
            password.length >= 8,
            /[a-z]/.test(password),
            /[A-Z]/.test(password),
            /\d/.test(password),
            /[!@#$%^&*(),.?":{}|<>]/.test(password)
        ];
        
        strength = checks.filter(check => check).length;
        
        const indicator = document.querySelector('.password-strength');
        if (indicator) {
            indicator.className = 'password-strength';
            if (strength < 2) indicator.classList.add('weak');
            else if (strength < 4) indicator.classList.add('medium');
            else indicator.classList.add('strong');
            
            const strengthText = strength < 2 ? 'Weak' : strength < 4 ? 'Medium' : 'Strong';
            indicator.textContent = `Password Strength: ${strengthText}`;
        }
    }
    
    function createPasswordStrengthIndicator() {
        const strengthDiv = document.createElement('div');
        strengthDiv.className = 'password-strength';
        password1Field.parentElement.appendChild(strengthDiv);
    }
    
    function showFieldError(field, message) {
        clearFieldError(field);
        field.classList.add('error');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error-message';
        errorDiv.textContent = message;
        field.parentElement.appendChild(errorDiv);
    }
    
    function clearFieldError(field) {
        field.classList.remove('error');
        const errorDiv = field.parentElement.querySelector('.field-error-message');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    function clearErrors() {
        const inputs = registerForm.querySelectorAll('input');
        inputs.forEach(input => {
            clearFieldError(input);
        });
    }
    
    function showLoadingState() {
        if (registerButton) {
            registerButton.disabled = true;
            registerButton.textContent = 'Creating Account...';
            registerButton.classList.add('loading');
        }
    }
    
    // Auto-hide alert messages
    const alerts = document.querySelectorAll('.register-error, .register-success');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
    
    // Add character counter for username
    if (usernameField) {
        const counter = document.createElement('div');
        counter.className = 'char-counter';
        usernameField.parentElement.appendChild(counter);
        
        usernameField.addEventListener('input', function() {
            counter.textContent = `${this.value.length}/150 characters`;
        });
    }
});
