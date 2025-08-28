// Login Form JavaScript Enhancement
document.addEventListener('DOMContentLoaded', function() {
    console.log('Login form loaded');
    
    // Get login form elements
    const loginForm = document.querySelector('.login-form');
    const usernameField = document.querySelector('input[name="username"]');
    const passwordField = document.querySelector('input[name="password"]');
    const loginButton = document.querySelector('.login-btn');
    
    if (loginForm) {
        // Add form validation
        loginForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Clear previous error styling
            clearErrors();
            
            // Validate username
            if (!usernameField.value.trim()) {
                showFieldError(usernameField, 'Username is required');
                isValid = false;
            }
            
            // Validate password
            if (!passwordField.value.trim()) {
                showFieldError(passwordField, 'Password is required');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
                return false;
            }
            
            // Show loading state
            showLoadingState();
        });
        
        // Add real-time validation
        usernameField.addEventListener('blur', function() {
            if (!this.value.trim()) {
                showFieldError(this, 'Username is required');
            } else {
                clearFieldError(this);
            }
        });
        
        passwordField.addEventListener('blur', function() {
            if (!this.value.trim()) {
                showFieldError(this, 'Password is required');
            } else {
                clearFieldError(this);
            }
        });
        
        // Add input focus effects
        const inputs = loginForm.querySelectorAll('input');
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
        const inputs = loginForm.querySelectorAll('input');
        inputs.forEach(input => {
            clearFieldError(input);
        });
    }
    
    function showLoadingState() {
        if (loginButton) {
            loginButton.disabled = true;
            loginButton.textContent = 'Signing In...';
            loginButton.classList.add('loading');
        }
    }
    
    // Auto-hide alert messages
    const alerts = document.querySelectorAll('.login-error, .login-success');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Enter key submits form
        if (e.key === 'Enter' && (usernameField.matches(':focus') || passwordField.matches(':focus'))) {
            loginForm.dispatchEvent(new Event('submit'));
        }
    });
});
