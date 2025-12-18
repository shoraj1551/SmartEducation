// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State management
let currentUserId = null;
let currentPurpose = 'registration';

// Modal elements
const signInBtn = document.getElementById('signInBtn');
const signUpBtn = document.getElementById('signUpBtn');
const getStartedBtn = document.getElementById('getStartedBtn');
const signInModal = document.getElementById('signInModal');
const signUpModal = document.getElementById('signUpModal');
const otpModal = document.getElementById('otpModal');
const forgotPasswordModal = document.getElementById('forgotPasswordModal');
const resetPasswordModal = document.getElementById('resetPasswordModal');

// Close buttons
const closeSignIn = document.getElementById('closeSignIn');
const closeSignUp = document.getElementById('closeSignUp');
const closeOtp = document.getElementById('closeOtp');
const closeForgotPassword = document.getElementById('closeForgotPassword');
const closeResetPassword = document.getElementById('closeResetPassword');

// Links
const switchToSignUp = document.getElementById('switchToSignUp');
const switchToSignIn = document.getElementById('switchToSignIn');
const forgotPasswordLink = document.getElementById('forgotPasswordLink');
const backToSignIn = document.getElementById('backToSignIn');
const resendOtpLink = document.getElementById('resendOtpLink');

// Forms
const signUpForm = document.getElementById('signUpForm');
const signInForm = document.getElementById('signInForm');
const otpForm = document.getElementById('otpForm');
const forgotPasswordForm = document.getElementById('forgotPasswordForm');
const resetPasswordForm = document.getElementById('resetPasswordForm');

// Helper Functions
function showModal(modal) {
    modal.classList.add('active');
}

function hideModal(modal) {
    modal.classList.remove('active');
}

function showMessage(message, type = 'info') {
    alert(message); // Simple alert for now, can be replaced with toast notifications
}

// Open Modals
signInBtn.addEventListener('click', () => showModal(signInModal));
signUpBtn.addEventListener('click', () => showModal(signUpModal));
getStartedBtn.addEventListener('click', () => showModal(signUpModal));

// Close Modals
closeSignIn.addEventListener('click', () => hideModal(signInModal));
closeSignUp.addEventListener('click', () => hideModal(signUpModal));
closeOtp.addEventListener('click', () => hideModal(otpModal));
closeForgotPassword.addEventListener('click', () => hideModal(forgotPasswordModal));
closeResetPassword.addEventListener('click', () => hideModal(resetPasswordModal));

// Switch Modals
switchToSignUp.addEventListener('click', (e) => {
    e.preventDefault();
    hideModal(signInModal);
    showModal(signUpModal);
});

switchToSignIn.addEventListener('click', (e) => {
    e.preventDefault();
    hideModal(signUpModal);
    showModal(signInModal);
});

forgotPasswordLink.addEventListener('click', (e) => {
    e.preventDefault();
    hideModal(signInModal);
    showModal(forgotPasswordModal);
});

backToSignIn.addEventListener('click', (e) => {
    e.preventDefault();
    hideModal(forgotPasswordModal);
    showModal(signInModal);
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === signInModal) hideModal(signInModal);
    if (e.target === signUpModal) hideModal(signUpModal);
    if (e.target === otpModal) hideModal(otpModal);
    if (e.target === forgotPasswordModal) hideModal(forgotPasswordModal);
    if (e.target === resetPasswordModal) hideModal(resetPasswordModal);
});

// Sign Up Handler
signUpForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('signUpName').value;
    const email = document.getElementById('signUpEmail').value;
    const mobile = document.getElementById('signUpMobile').value;
    const password = document.getElementById('signUpPassword').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, mobile, password }),
        });

        const data = await response.json();

        if (response.ok) {
            currentUserId = data.user_id;
            currentPurpose = 'registration';
            showMessage(data.message, 'success');
            hideModal(signUpModal);
            showModal(otpModal);
        } else {
            showMessage(data.error, 'error');
        }
    } catch (error) {
        showMessage('Registration failed. Please try again.', 'error');
        console.error('Error:', error);
    }
});

// OTP Verification Handler
otpForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const emailOtp = document.getElementById('emailOtp').value;
    const mobileOtp = document.getElementById('mobileOtp').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/verify-otp`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUserId,
                email_otp: emailOtp,
                mobile_otp: mobileOtp,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('Account verified successfully!', 'success');
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            hideModal(otpModal);
            // Redirect to dashboard or home page
            window.location.reload();
        } else {
            showMessage(data.error, 'error');
        }
    } catch (error) {
        showMessage('Verification failed. Please try again.', 'error');
        console.error('Error:', error);
    }
});

// Resend OTP Handler
resendOtpLink.addEventListener('click', async (e) => {
    e.preventDefault();

    try {
        // Resend email OTP
        await fetch(`${API_BASE_URL}/auth/resend-otp`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUserId,
                otp_type: 'email',
                purpose: currentPurpose,
            }),
        });

        // Resend mobile OTP
        await fetch(`${API_BASE_URL}/auth/resend-otp`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUserId,
                otp_type: 'mobile',
                purpose: currentPurpose,
            }),
        });

        showMessage('OTP resent successfully!', 'success');
    } catch (error) {
        showMessage('Failed to resend OTP. Please try again.', 'error');
        console.error('Error:', error);
    }
});

// Sign In Handler
signInForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const identifier = document.getElementById('signInIdentifier').value;
    const password = document.getElementById('signInPassword').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ identifier, password }),
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('Login successful!', 'success');
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            hideModal(signInModal);
            // Redirect to dashboard or home page
            window.location.reload();
        } else {
            showMessage(data.error, 'error');
        }
    } catch (error) {
        showMessage('Login failed. Please try again.', 'error');
        console.error('Error:', error);
    }
});

// Forgot Password Handler
forgotPasswordForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const identifier = document.getElementById('resetIdentifier').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/forgot-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ identifier }),
        });

        const data = await response.json();

        if (response.ok) {
            currentUserId = data.user_id;
            currentPurpose = 'reset';
            showMessage(data.message, 'success');
            hideModal(forgotPasswordModal);
            showModal(resetPasswordModal);
        } else {
            showMessage(data.error, 'error');
        }
    } catch (error) {
        showMessage('Request failed. Please try again.', 'error');
        console.error('Error:', error);
    }
});

// Reset Password Handler
resetPasswordForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const emailOtp = document.getElementById('resetEmailOtp').value;
    const mobileOtp = document.getElementById('resetMobileOtp').value;
    const newPassword = document.getElementById('newPassword').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/reset-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUserId,
                email_otp: emailOtp,
                mobile_otp: mobileOtp,
                new_password: newPassword,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('Password reset successfully!', 'success');
            hideModal(resetPasswordModal);
            showModal(signInModal);
        } else {
            showMessage(data.error, 'error');
        }
    } catch (error) {
        showMessage('Password reset failed. Please try again.', 'error');
        console.error('Error:', error);
    }
});

// Parallax effect for background shapes
let mouseX = 0;
let mouseY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX / window.innerWidth;
    mouseY = e.clientY / window.innerHeight;

    const shapes = document.querySelectorAll('.shape');
    shapes.forEach((shape, index) => {
        const speed = (index + 1) * 0.5;
        const x = (mouseX - 0.5) * speed * 50;
        const y = (mouseY - 0.5) * speed * 50;
        shape.style.transform = `translate(${x}px, ${y}px)`;
    });
});

console.log('SmartEducation - Welcome! 🚀');
console.log('API Base URL:', API_BASE_URL);
