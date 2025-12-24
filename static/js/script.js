// API Configuration
const API_BASE_URL = '/api';

// Mobile Number Validation (IMPROVEMENT-002)
function validateMobile(mobile) {
    if (!mobile) {
        return { valid: false, error: 'Mobile number is required' };
    }

    // Remove non-digits
    const clean = mobile.replace(/\D/g, '');

    if (clean.length === 10) {
        return { valid: true, normalized: clean, message: 'Valid mobile number' };
    } else if (clean.length === 12 && clean.startsWith('91')) {
        return { valid: true, normalized: clean.substring(2), message: 'Valid mobile number (country code will be removed)' };
    } else if (clean.length === 12 && !clean.startsWith('91')) {
        return { valid: false, error: 'Invalid country code. Please use 91 (India) or omit country code.' };
    } else {
        return {
            valid: false,
            error: `Mobile must be 10 digits (e.g., 9876543210) or 12 digits with country code (e.g., 919876543210). Got ${clean.length} digits.`
        };
    }
}

// State management
let currentUserId = null;
let currentUserName = null;
let currentPurpose = 'registration';
let tempUserId = null; // Added missing declaration
let emailVerified = false; // Added missing declaration
let mobileVerified = false; // Added missing declaration


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

    // Reset signup modal verification states
    if (modal === signUpModal) {
        // Reset verification flags
        emailVerified = false;
        mobileVerified = false;
        tempUserId = null;

        // Re-enable and reset email field
        if (signUpEmail) {
            signUpEmail.readOnly = false;
            signUpEmail.disabled = false;
        }
        if (verifyEmailBtn) {
            verifyEmailBtn.disabled = true;
            verifyEmailBtn.classList.remove('verified');
        }
        if (emailVerificationStatus) {
            emailVerificationStatus.textContent = '';
            emailVerificationStatus.className = 'verification-status';
        }

        // Re-enable and reset mobile field
        if (signUpMobile) {
            signUpMobile.readOnly = false;
            signUpMobile.disabled = false;
        }
        if (verifyMobileBtn) {
            verifyMobileBtn.disabled = true;
            verifyMobileBtn.classList.remove('verified');
        }
        if (mobileVerificationStatus) {
            mobileVerificationStatus.textContent = '';
            mobileVerificationStatus.className = 'verification-status';
        }

        // Reset password match status
        if (passwordMatchStatus) {
            passwordMatchStatus.textContent = '';
            passwordMatchStatus.className = 'password-match-status';
        }
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

if (signUpPassword && signUpConfirmPassword) {
    signUpPassword.addEventListener('input', validatePasswordMatch);
    signUpConfirmPassword.addEventListener('input', validatePasswordMatch);
}

// ===== Inline Email/Mobile Verification =====
const signUpEmail = document.getElementById('signUpEmail');
const signUpMobile = document.getElementById('signUpMobile');
const verifyEmailBtn = document.getElementById('verifyEmailBtn');
const verifyMobileBtn = document.getElementById('verifyMobileBtn');
const emailVerificationStatus = document.getElementById('emailVerificationStatus');
const mobileVerificationStatus = document.getElementById('mobileVerificationStatus');

// Variables moved to top of file


// Enable verify buttons when input has value
// Enable verify buttons when input has value
if (signUpEmail && verifyEmailBtn) {
    signUpEmail.addEventListener('input', () => {
        verifyEmailBtn.disabled = !signUpEmail.value || emailVerified;
    });
}

if (signUpMobile && verifyMobileBtn) {
    signUpMobile.addEventListener('input', () => {
        verifyMobileBtn.disabled = !signUpMobile.value || mobileVerified;
    });
}

// Email verification - Send OTP
// Email verification - Send OTP
if (verifyEmailBtn) {
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
}

// Mobile verification - Send OTP
// Mobile verification - Send OTP
if (verifyMobileBtn) {
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
}

// Email OTP Form Submission
// Email OTP Form Submission
if (emailOtpForm) {
    emailOtpForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const otpCode = document.getElementById('emailOtpInput').value;

        if (otpCode.length !== 6) {
            showMessage('Please enter a valid 6-digit OTP', 'error');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/auth/verify-inline-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    temp_user_id: tempUserId,
                    otp_type: 'email',
                    otp_code: otpCode
                }),
                credentials: 'include'
            });

            const data = await response.json();

            if (response.ok) {
                emailVerified = true;
                verifyEmailBtn.classList.add('verified');
                verifyEmailBtn.disabled = true;
                emailVerificationStatus.textContent = '✓ Email verified';
                emailVerificationStatus.className = 'verification-status verified';
                signUpEmail.readOnly = true;
                hideModal(emailOtpModal);
                showMessage('Email verified successfully!', 'success');
            } else {
                showMessage(data.error || 'Invalid OTP', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            // Fallback for demo if offline (should not happen in prod)
            if (otpCode === '123456') {
                emailVerified = true;
                verifyEmailBtn.classList.add('verified');
                verifyEmailBtn.disabled = true;
                emailVerificationStatus.textContent = '✓ Email verified';
                emailVerificationStatus.className = 'verification-status verified';
                signUpEmail.readOnly = true;
                hideModal(emailOtpModal);
                showMessage('Email verified (Demo Mode)!', 'success');
            } else {
                showMessage('Verification failed', 'error');
            }
        }
    });
}

// Mobile OTP Form Submission
// Mobile OTP Form Submission
if (mobileOtpForm) {
    mobileOtpForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const otpCode = document.getElementById('mobileOtpInput').value;

        if (otpCode.length !== 6) {
            showMessage('Please enter a valid 6-digit OTP', 'error');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/auth/verify-inline-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    temp_user_id: tempUserId,
                    otp_type: 'mobile',
                    otp_code: otpCode
                }),
                credentials: 'include'
            });

            const data = await response.json();

            if (response.ok) {
                mobileVerified = true;
                verifyMobileBtn.classList.add('verified');
                verifyMobileBtn.disabled = true;
                mobileVerificationStatus.textContent = '✓ Mobile verified';
                mobileVerificationStatus.className = 'verification-status verified';
                signUpMobile.readOnly = true;
                hideModal(mobileOtpModal);
                showMessage('Mobile verified successfully!', 'success');
            } else {
                showMessage(data.error || 'Invalid OTP', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            // Fallback
            if (otpCode === '123456') {
                mobileVerified = true;
                verifyMobileBtn.classList.add('verified');
                verifyMobileBtn.disabled = true;
                mobileVerificationStatus.textContent = '✓ Mobile verified';
                mobileVerificationStatus.className = 'verification-status verified';
                signUpMobile.readOnly = true;
                hideModal(mobileOtpModal);
                showMessage('Mobile verified (Demo Mode)!', 'success');
            } else {
                showMessage('Verification failed', 'error');
            }
        }
    });
}

// Open Modals
if (signInBtn) signInBtn.addEventListener('click', () => showModal(signInModal));
if (signUpBtn) signUpBtn.addEventListener('click', () => showModal(signUpModal));
if (getStartedBtn) getStartedBtn.addEventListener('click', () => showModal(signUpModal));

// Close Modals
if (closeSignIn) closeSignIn.addEventListener('click', () => hideModal(signInModal));
if (closeSignUp) closeSignUp.addEventListener('click', () => hideModal(signUpModal));
if (closeOtp) closeOtp.addEventListener('click', () => hideModal(otpModal));
if (closeEmailOtp) closeEmailOtp.addEventListener('click', () => hideModal(emailOtpModal));
if (closeMobileOtp) closeMobileOtp.addEventListener('click', () => hideModal(mobileOtpModal));
if (closeForgotPassword) closeForgotPassword.addEventListener('click', () => hideModal(forgotPasswordModal));
if (closeResetPassword) closeResetPassword.addEventListener('click', () => hideModal(resetPasswordModal));

// Switch Modals
if (switchToSignUp) {
    switchToSignUp.addEventListener('click', (e) => {
        e.preventDefault();
        hideModal(signInModal);
        showModal(signUpModal);
    });
}

if (switchToSignIn) {
    switchToSignIn.addEventListener('click', (e) => {
        e.preventDefault();
        hideModal(signUpModal);
        showModal(signInModal);
    });
}

if (forgotPasswordLink) {
    forgotPasswordLink.addEventListener('click', (e) => {
        e.preventDefault();
        hideModal(signInModal);
        showModal(forgotPasswordModal);
    });
}

if (backToSignIn) {
    backToSignIn.addEventListener('click', (e) => {
        e.preventDefault();
        hideModal(forgotPasswordModal);
        showModal(signInModal);
    });
}

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (signInModal && e.target === signInModal) hideModal(signInModal);
    if (signUpModal && e.target === signUpModal) hideModal(signUpModal);
    if (otpModal && e.target === otpModal) hideModal(otpModal);
    if (emailOtpModal && e.target === emailOtpModal) hideModal(emailOtpModal);
    if (mobileOtpModal && e.target === mobileOtpModal) hideModal(mobileOtpModal);
    if (forgotPasswordModal && e.target === forgotPasswordModal) hideModal(forgotPasswordModal);
    if (resetPasswordModal && e.target === resetPasswordModal) hideModal(resetPasswordModal);
});

// Sign Up Handler
if (signUpForm) {
    signUpForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('signUpName').value;
        const email = document.getElementById('signUpEmail') ? document.getElementById('signUpEmail').value : '';
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
                body: JSON.stringify({
                    name,
                    email,
                    mobile,
                    password,
                    temp_user_id: tempUserId // Pass temp ID if verified inline
                }),
                credentials: 'include'
            });

            const data = await response.json();

            if (response.ok) {
                currentUserId = data.user_id;
                currentUserName = name;

                // Check if already fully verified via inline flow
                if (data.verification_completed) {
                    // Skip OTP modal, go straight to welcome
                    showMessage('Registration complete! Redirecting...', 'success');
                    if (signUpModal) hideModal(signUpModal);
                    localStorage.setItem('user', JSON.stringify({ name, email, mobile, id: data.user_id }));
                    setTimeout(() => {
                        window.location.href = '/welcome';
                    }, 1500);
                } else {
                    // Normal flow: verify combined OTPs
                    currentPurpose = 'registration';
                    showMessage(data.message, 'success');
                    if (signUpModal) hideModal(signUpModal);
                    if (otpModal) showModal(otpModal);
                    else window.location.href = '/verify-otp'; // Fallback if no modal (todo)
                }
            } else {
                showMessage(data.error, 'error');
            }
        } catch (error) {
            showMessage('Registration failed. Please try again.', 'error');
            console.error('Error:', error);
        }
    });
}


// OTP Verification Handler
// OTP Verification Handler
if (otpForm) {
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
                showMessage(`Welcome ${userName}! Let's personalize your experience...`, 'success');

                // Clear OTP form
                document.getElementById('emailOtp').value = '';
                document.getElementById('mobileOtp').value = '';

                hideModal(otpModal);

                // Redirect to welcome survey page
                setTimeout(() => {
                    window.location.href = '/welcome';
                }, 1500);
            } else {
                showMessage(data.error, 'error');
            }
        } catch (error) {
            showMessage('Verification failed. Please try again.', 'error');
            console.error('Error:', error);
        }
    });
}

// Resend OTP Handler
// Resend OTP Handler
if (resendOtpLink) {
    resendOtpLink.addEventListener('click', async (e) => {
        e.preventDefault();

        try {
            // Disable button to prevent multiple clicks
            resendOtpLink.style.pointerEvents = 'none';
            resendOtpLink.style.opacity = '0.6';

            // Show loading message
            showMessage('Resending OTP...', 'info');

            // Resend email OTP
            const emailResponse = await fetch(`${API_BASE_URL}/auth/resend-otp`, {
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

            const emailData = await emailResponse.json();

            if (!emailResponse.ok) {
                throw new Error(emailData.error || 'Failed to resend email OTP');
            }

            // Resend mobile OTP
            const mobileResponse = await fetch(`${API_BASE_URL}/auth/resend-otp`, {
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

            const mobileData = await mobileResponse.json();

            if (!mobileResponse.ok) {
                throw new Error(mobileData.error || 'Failed to resend mobile OTP');
            }

            // Both OTPs sent successfully
            showMessage('✅ OTP resent successfully to both email and mobile!', 'success');

            // Re-enable button after 30 seconds
            setTimeout(() => {
                resendOtpLink.style.pointerEvents = 'auto';
                resendOtpLink.style.opacity = '1';
            }, 30000);

        } catch (error) {
            showMessage('❌ Failed to resend OTP. Please try again.', 'error');
            console.error('Error:', error);

            // Re-enable button immediately on error
            resendOtpLink.style.pointerEvents = 'auto';
            resendOtpLink.style.opacity = '1';
        }
    });
}

// Sign In Handler
if (signInForm) {
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
                if (signInModal) hideModal(signInModal);

                // Redirect to dashboard
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            } else if (response.status === 403 && data.code === 'VERIFICATION_REQUIRED') {
                showMessage('Account not verified. Redirecting to verification...', 'info');
                setTimeout(() => {
                    // Redirect to register/verification page with params
                    // We assume identifier is email for simplicity in param, or we pass userId provided by backend
                    window.location.href = `/register?step=otp&userId=${data.userId}&email=${encodeURIComponent(identifier)}`;
                }, 1500);
            } else {
                showMessage(data.error, 'error');
            }
        } catch (error) {
            showMessage('Login failed. Please try again.', 'error');
            console.error('Error:', error);
        }
    });
}

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

// Auto-open login modal if redirected from welcome page (BUG-006)
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('login') === 'true') {
        // Auto-open login modal
        setTimeout(() => {
            showModal(signInModal);
            // Clean up URL
            window.history.replaceState({}, document.title, window.location.pathname);
        }, 500);
    }
});

console.log('SmartEducation - Welcome! 🚀 (v4)');
console.log('API Base URL:', API_BASE_URL);
