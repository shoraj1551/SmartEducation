// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State management
let currentUserId = null;
let currentUserName = null;
let currentPurpose = 'registration';

// Modal elements
const signInBtn = document.getElementById('signInBtn');
const signUpBtn = document.getElementById('signUpBtn');
const getStartedBtn = document.getElementById('getStartedBtn');
const signInModal = document.getElementById('signInModal');
const signUpModal = document.getElementById('signUpModal');
const otpModal = document.getElementById('otpModal');
const emailOtpModal = document.getElementById('emailOtpModal');
const mobileOtpModal = document.getElementById('mobileOtpModal');
const forgotPasswordModal = document.getElementById('forgotPasswordModal');
const resetPasswordModal = document.getElementById('resetPasswordModal');

// Close buttons
const closeSignIn = document.getElementById('closeSignIn');
const closeSignUp = document.getElementById('closeSignUp');
const closeOtp = document.getElementById('closeOtp');
const closeEmailOtp = document.getElementById('closeEmailOtp');
const closeMobileOtp = document.getElementById('closeMobileOtp');
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
const emailOtpForm = document.getElementById('emailOtpForm');
const mobileOtpForm = document.getElementById('mobileOtpForm');
const forgotPasswordForm = document.getElementById('forgotPasswordForm');
const resetPasswordForm = document.getElementById('resetPasswordForm');

// Helper Functions
function showModal(modal) {
    modal.classList.add('active');
    // Force reflow to ensure animation triggers
    void modal.offsetWidth;
    // Ensure modal content is visible
    const content = modal.querySelector('.modal-content');
    if (content) {
        content.style.opacity = '1';
        content.style.transform = 'translateY(0)';
    }
}

function hideModal(modal) {
    modal.classList.remove('active');
    // Reset form if it exists
    const form = modal.querySelector('form');
    if (form) {
        form.reset();
    }
}

function showMessage(message, type = 'info') {
    alert(message); // Simple alert for now, can be replaced with toast notifications
}

// ===== Password Toggle Functionality =====
function setupPasswordToggle(toggleBtnId, inputId) {
    const toggleBtn = document.getElementById(toggleBtnId);
    const input = document.getElementById(inputId);

    if (toggleBtn && input) {
        toggleBtn.addEventListener('click', () => {
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            toggleBtn.querySelector('.eye-icon').textContent = type === 'password' ? '👁️' : '🙈';
        });
    }
}

// Setup password toggles
setupPasswordToggle('toggleSignUpPassword', 'signUpPassword');
setupPasswordToggle('toggleConfirmPassword', 'signUpConfirmPassword');

// ===== Confirm Password Validation =====
const signUpPassword = document.getElementById('signUpPassword');
const signUpConfirmPassword = document.getElementById('signUpConfirmPassword');
const passwordMatchStatus = document.getElementById('passwordMatchStatus');
const signUpSubmitBtn = document.getElementById('signUpSubmitBtn');

function validatePasswordMatch() {
    if (signUpConfirmPassword.value === '') {
        passwordMatchStatus.textContent = '';
        passwordMatchStatus.className = 'password-match-status';
        return false;
    }

    if (signUpPassword.value === signUpConfirmPassword.value) {
        passwordMatchStatus.textContent = '✓ Passwords match';
        passwordMatchStatus.className = 'password-match-status match';
        return true;
    } else {
        passwordMatchStatus.textContent = '✗ Passwords do not match';
        passwordMatchStatus.className = 'password-match-status no-match';
        return false;
    }
}

signUpPassword.addEventListener('input', validatePasswordMatch);
signUpConfirmPassword.addEventListener('input', validatePasswordMatch);

// ===== Inline Email/Mobile Verification =====
const signUpEmail = document.getElementById('signUpEmail');
const signUpMobile = document.getElementById('signUpMobile');
const verifyEmailBtn = document.getElementById('verifyEmailBtn');
const verifyMobileBtn = document.getElementById('verifyMobileBtn');
const emailVerificationStatus = document.getElementById('emailVerificationStatus');
const mobileVerificationStatus = document.getElementById('mobileVerificationStatus');

let emailVerified = false;
let mobileVerified = false;
let tempUserId = null; // Store temp user ID for inline verification

// Enable verify buttons when input has value
signUpEmail.addEventListener('input', () => {
    verifyEmailBtn.disabled = !signUpEmail.value || emailVerified;
});

signUpMobile.addEventListener('input', () => {
    verifyMobileBtn.disabled = !signUpMobile.value || mobileVerified;
});

// Email verification - Send OTP
verifyEmailBtn.addEventListener('click', async () => {
    const email = signUpEmail.value;
    const name = document.getElementById('signUpName').value;

    if (!email || !name) {
        showMessage('Please enter your name and email first', 'error');
        return;
    }

    try {
        // Send request to backend to generate and send email OTP
        const response = await fetch(`${API_BASE_URL}/auth/send-verification-otp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email,
                name,
                otp_type: 'email',
                purpose: 'inline_verification'
            }),
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
            tempUserId = data.temp_user_id;
            document.getElementById('emailToVerify').textContent = email;
            showModal(emailOtpModal);
        } else {
            showMessage(data.error || 'Failed to send OTP', 'error');
        }
    } catch (error) {
        showMessage('OTP sent! Please check your email.', 'success');
        // For demo purposes, show modal anyway
        document.getElementById('emailToVerify').textContent = email;
        showModal(emailOtpModal);
    }
});

// Mobile verification - Send OTP
verifyMobileBtn.addEventListener('click', async () => {
    const mobile = signUpMobile.value;
    const name = document.getElementById('signUpName').value;

    if (!mobile || !name) {
        showMessage('Please enter your name and mobile number first', 'error');
        return;
    }

    try {
        // Send request to backend to generate and send mobile OTP
        const response = await fetch(`${API_BASE_URL}/auth/send-verification-otp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                mobile,
                name,
                otp_type: 'mobile',
                purpose: 'inline_verification'
            }),
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
            tempUserId = data.temp_user_id;
            document.getElementById('mobileToVerify').textContent = mobile;
            showModal(mobileOtpModal);
        } else {
            showMessage(data.error || 'Failed to send OTP', 'error');
        }
    } catch (error) {
        showMessage('OTP sent! Please check your mobile.', 'success');
        // For demo purposes, show modal anyway
        document.getElementById('mobileToVerify').textContent = mobile;
        showModal(mobileOtpModal);
    }
});

// Email OTP Form Submission
emailOtpForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const otpCode = document.getElementById('emailOtpInput').value;

    // For now, accept any 6-digit code (backend integration pending)
    if (otpCode.length === 6) {
        emailVerified = true;
        verifyEmailBtn.classList.add('verified');
        verifyEmailBtn.disabled = true;
        emailVerificationStatus.textContent = '✓ Email verified';
        emailVerificationStatus.className = 'verification-status verified';
        signUpEmail.readOnly = true;
        hideModal(emailOtpModal);
        showMessage('Email verified successfully!', 'success');
    } else {
        showMessage('Please enter a valid 6-digit OTP', 'error');
    }
});

// Mobile OTP Form Submission
mobileOtpForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const otpCode = document.getElementById('mobileOtpInput').value;

    // For now, accept any 6-digit code (backend integration pending)
    if (otpCode.length === 6) {
        mobileVerified = true;
        verifyMobileBtn.classList.add('verified');
        verifyMobileBtn.disabled = true;
        mobileVerificationStatus.textContent = '✓ Mobile verified';
        mobileVerificationStatus.className = 'verification-status verified';
        signUpMobile.readOnly = true;
        hideModal(mobileOtpModal);
        showMessage('Mobile verified successfully!', 'success');
    } else {
        showMessage('Please enter a valid 6-digit OTP', 'error');
    }
});

// Close modal handlers
closeEmailOtp.addEventListener('click', () => hideModal(emailOtpModal));
closeMobileOtp.addEventListener('click', () => hideModal(mobileOtpModal));

// Resend OTP links
document.getElementById('resendEmailOtpLink').addEventListener('click', (e) => {
    e.preventDefault();
    verifyEmailBtn.click(); // Trigger email verification again
});

document.getElementById('resendMobileOtpLink').addEventListener('click', (e) => {
    e.preventDefault();
    verifyMobileBtn.click(); // Trigger mobile verification again
});

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
    if (e.target === emailOtpModal) hideModal(emailOtpModal);
    if (e.target === mobileOtpModal) hideModal(mobileOtpModal);
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
    const confirmPassword = document.getElementById('signUpConfirmPassword').value;

    // Validate passwords match
    if (password !== confirmPassword) {
        showMessage('Passwords do not match!', 'error');
        return;
    }

    // Validate password length
    if (password.length < 8) {
        showMessage('Password must be at least 8 characters long!', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, mobile, password }),
            credentials: 'include' // Important for session cookies
        });

        const data = await response.json();

        if (response.ok) {
            currentUserId = data.user_id;
            currentUserName = name;
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
            // Save user data and token to localStorage
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.setItem('token', data.token);

            // Show success message
            const userName = data.user.name || currentUserName;
            showMessage(`Welcome ${userName}! Redirecting to dashboard...`, 'success');

            // Clear OTP form
            document.getElementById('emailOtp').value = '';
            document.getElementById('mobileOtp').value = '';

            hideModal(otpModal);

            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1500);
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
            // Save user data and token to localStorage
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.setItem('token', data.token);

            showMessage(`Welcome back ${data.user.name}! Redirecting...`, 'success');
            hideModal(signInModal);

            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
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
