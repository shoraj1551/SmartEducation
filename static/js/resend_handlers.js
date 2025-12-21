// Resend Email OTP Link (BUG-009 fix)
const resendEmailOtpLink = document.getElementById('resendEmailOtpLink');
if (resendEmailOtpLink) {
    resendEmailOtpLink.addEventListener('click', async (e) => {
        e.preventDefault();

        try {
            resendEmailOtpLink.style.pointerEvents = 'none';
            resendEmailOtpLink.style.opacity = '0.6';

            showMessage('Resending email OTP...', 'info');

            const response = await fetch(`${API_BASE_URL}/auth/resend-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: tempUserId,
                    otp_type: 'email',
                    purpose: 'registration',
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to resend email OTP');
            }

            showMessage('✅ Email OTP resent successfully!', 'success');

            setTimeout(() => {
                resendEmailOtpLink.style.pointerEvents = 'auto';
                resendEmailOtpLink.style.opacity = '1';
            }, 30000);

        } catch (error) {
            showMessage('❌ Failed to resend email OTP.', 'error');
            console.error('Error:', error);
            resendEmailOtpLink.style.pointerEvents = 'auto';
            resendEmailOtpLink.style.opacity = '1';
        }
    });
}

// Resend Mobile OTP Link (BUG-009 fix)
const resendMobileOtpLink = document.getElementById('resendMobileOtpLink');
if (resendMobileOtpLink) {
    resendMobileOtpLink.addEventListener('click', async (e) => {
        e.preventDefault();

        try {
            resendMobileOtpLink.style.pointerEvents = 'none';
            resendMobileOtpLink.style.opacity = '0.6';

            showMessage('Resending mobile OTP...', 'info');

            const response = await fetch(`${API_BASE_URL}/auth/resend-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: tempUserId,
                    otp_type: 'mobile',
                    purpose: 'registration',
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to resend mobile OTP');
            }

            showMessage('✅ Mobile OTP resent successfully!', 'success');

            setTimeout(() => {
                resendMobileOtpLink.style.pointerEvents = 'auto';
                resendMobileOtpLink.style.opacity = '1';
            }, 30000);

        } catch (error) {
            showMessage('❌ Failed to resend mobile OTP.', 'error');
            console.error('Error:', error);
            resendMobileOtpLink.style.pointerEvents = 'auto';
            resendMobileOtpLink.style.opacity = '1';
        }
    });
}
