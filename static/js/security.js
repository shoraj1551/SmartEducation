/**
 * SmartEducation - Security Center Logic
 * Handles sessions, logs, 2FA, and account deletion.
 */

class SecurityManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.sessionsList = document.getElementById('sessionsList');
        this.activityList = document.getElementById('activityList');

        // Toggles
        this.toggle2FA = document.getElementById('toggle2FA');
        this.toggleLoginAlerts = document.getElementById('toggleLoginAlerts');

        // Modal logic
        this.otpModal = document.getElementById('otpModal');
        this.otpInput = document.getElementById('otpInput');
        this.otpError = document.getElementById('otpError');
        this.confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = '/';
            return;
        }

        this.loadSessions();
        this.loadLogs();
        this.setupToggles();
        this.setupOTPInput();
    }

    // --- SESSIONS ---
    async loadSessions() {
        try {
            const response = await fetch('/api/security/sessions', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const sessions = await response.json();
            this.renderSessions(sessions);
        } catch (err) {
            this.sessionsList.innerHTML = '<div class="error-text">Failed to load active sessions.</div>';
        }
    }

    renderSessions(sessions) {
        if (!sessions || sessions.length === 0) {
            this.sessionsList.innerHTML = '<div class="empty-state">No active sessions found.</div>';
            return;
        }

        this.sessionsList.innerHTML = sessions.map(session => `
            <div class="session-item">
                <div class="session-info">
                    <div class="device-icon"><i class="fas fa-${this.getDeviceIcon(session.device_info)}"></i></div>
                    <div class="session-details">
                        <h4>${session.device_info || 'Unknown Device'} ${session.is_current ? '<span class="current-badge">This Device</span>' : ''}</h4>
                        <p>${session.ip_address} • Logged in ${new Date(session.login_time).toLocaleString()}</p>
                    </div>
                </div>
                ${session.is_current ?
                '<span class="revoke-link disabled" style="opacity: 0.5; cursor: default;">Current</span>' :
                `<a href="#" class="revoke-link" onclick="window.securityManager.handleRevokeSession('${session.id}')">Revoke Access</a>`
            }
            </div>
        `).join('');
    }

    getDeviceIcon(deviceInfo) {
        if (!deviceInfo) return 'desktop';
        const lower = deviceInfo.toLowerCase();
        if (lower.includes('mobile') || lower.includes('android') || lower.includes('iphone')) return 'mobile-alt';
        if (lower.includes('tablet') || lower.includes('ipad')) return 'tablet-alt';
        return 'desktop';
    }

    async handleRevokeSession(sessionId) {
        if (!confirm('Are you sure you want to log out this device?')) return;

        try {
            const res = await fetch('/api/security/sessions/revoke', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ session_id: sessionId })
            });

            if (res.ok) {
                this.loadSessions(); // Refresh
                this.loadLogs(); // Refresh logs to show "Revoke" action
            } else {
                alert('Failed to revoke session.');
            }
        } catch (err) {
            alert('Error revoking session.');
        }
    }

    // --- ACTIVITY LOGS ---
    async loadLogs() {
        try {
            const response = await fetch('/api/security/logs?limit=10', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const logs = await response.json();
            this.renderLogs(logs);
        } catch (err) {
            this.activityList.innerHTML = '<div class="error-text">Failed to load security activity.</div>';
        }
    }

    renderLogs(logs) {
        if (!logs || logs.length === 0) {
            this.activityList.innerHTML = '<div class="empty-state">No recent activity.</div>';
            return;
        }

        this.activityList.innerHTML = logs.map(log => `
            <div class="log-item">
                <div class="log-icon-sm"><i class="fas fa-${this.getLogIcon(log.activity_type)}"></i></div>
                <div class="log-content">
                    <h5>${this.formatLogTitle(log.activity_type)}</h5>
                    <p>${new Date(log.timestamp).toLocaleString()} • ${log.description}</p>
                </div>
            </div>
        `).join('');
    }

    getLogIcon(type) {
        switch (type) {
            case 'login': return 'sign-in-alt';
            case 'password_change': return 'key';
            case 'session_revoked': return 'user-shield';
            case 'security_setting_change': return 'sliders-h';
            default: return 'shield-alt';
        }
    }

    formatLogTitle(type) {
        return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    // --- TOGGLES ---
    setupToggles() {
        if (this.toggle2FA) {
            // Need to fetch current state? For now assume off or fetch profile
            // In a real app we'd fetch settings first.
            this.toggle2FA.addEventListener('change', async (e) => {
                const enable = e.target.checked;
                try {
                    const res = await fetch('/api/security/2fa/toggle', {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${this.token}`,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ enable })
                    });
                    if (res.ok) {
                        this.loadLogs(); // Log the change
                    } else {
                        e.target.checked = !enable; // Revert
                        alert('Failed to update 2FA setting.');
                    }
                } catch (err) {
                    e.target.checked = !enable;
                    alert('Error updating setting.');
                }
            });
        }

        // Login Alerts (Mock for now or implement similarly)
        if (this.toggleLoginAlerts) {
            this.toggleLoginAlerts.addEventListener('change', (e) => {
                // Logic to toggle alerts
            });
        }
    }

    // --- ACCOUNT DELETION ---
    initiateDeleteAccount() {
        // Show modal and request OTP
        this.otpModal.classList.add('active');
        this.requestDeleteOtp();
    }

    async requestDeleteOtp() {
        try {
            const res = await fetch('/api/security/account/delete-otp', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            if (res.ok) {
                console.log('OTP sent');
            } else {
                alert('Failed to send verification OTP.');
            }
        } catch (err) {
            console.error(err);
        }
    }

    setupOTPInput() {
        if (this.otpInput) {
            this.otpInput.addEventListener('input', (e) => {
                // Auto-format or restrict logic
            });
        }
    }

    async confirmDeleteAccount() {
        const otp = this.otpInput.value;
        if (!otp || otp.length < 6) {
            this.otpError.style.display = 'block';
            this.otpError.textContent = 'Please enter a valid 6-digit code.';
            return;
        }

        this.confirmDeleteBtn.disabled = true;
        this.confirmDeleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...';

        try {
            const res = await fetch('/api/security/account/delete', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ otp_code: otp })
            });

            const data = await res.json();

            if (res.ok) {
                alert('Account deleted successfully. You will now be redirected.');
                localStorage.clear();
                window.location.href = '/';
            } else {
                this.otpError.style.display = 'block';
                this.otpError.textContent = data.error || 'Verification failed.';
                this.confirmDeleteBtn.disabled = false;
                this.confirmDeleteBtn.textContent = 'Permanently Delete';
            }
        } catch (err) {
            this.otpError.style.display = 'block';
            this.otpError.textContent = 'Server connection error.';
            this.confirmDeleteBtn.disabled = false;
            this.confirmDeleteBtn.textContent = 'Permanently Delete';
        }
    }

    closeOtpModal() {
        this.otpModal.classList.remove('active');
        this.otpInput.value = '';
        this.otpError.style.display = 'none';
        this.confirmDeleteBtn.disabled = false;
        this.confirmDeleteBtn.textContent = 'Permanently Delete';
    }

    // --- PASSWORD CHANGE ---
    openPasswordModal() {
        document.getElementById('passwordModal').classList.add('active');
    }

    closePasswordModal() {
        document.getElementById('passwordModal').classList.remove('active');
        document.getElementById('changePasswordForm').reset();
        document.getElementById('passwordError').style.display = 'none';
        document.getElementById('submitPasswordBtn').disabled = false;
        document.getElementById('submitPasswordBtn').textContent = 'Update Password';
        // Reset OTP state
        document.getElementById('passwordOtpGroup').style.display = 'none';
        document.getElementById('passwordOtp').value = '';
    }

    async submitChangePassword() {
        const currentPassword = document.getElementById('currentPassword').value;
        const newPassword = document.getElementById('newPassword').value;
        const confirmNewPassword = document.getElementById('confirmNewPassword').value;
        const otpInput = document.getElementById('passwordOtp');
        const otpGroup = document.getElementById('passwordOtpGroup');
        const errorEl = document.getElementById('passwordError');
        const btn = document.getElementById('submitPasswordBtn');

        errorEl.style.display = 'none';

        if (newPassword !== confirmNewPassword) {
            errorEl.textContent = 'New passwords do not match.';
            errorEl.style.display = 'block';
            return;
        }

        if (newPassword.length < 8) {
            errorEl.textContent = 'Password must be at least 8 characters.';
            errorEl.style.display = 'block';
            return;
        }

        // Basic check for OTP if visible
        if (otpGroup.style.display === 'block' && otpInput.value.length < 6) {
            errorEl.textContent = 'Please enter the verification code.';
            errorEl.style.display = 'block';
            return;
        }

        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Processing...';

        const payload = {
            current_password: currentPassword,
            new_password: newPassword,
            otp_code: otpInput.value
        };

        try {
            const res = await fetch('/api/security/password/update', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (res.ok) {
                if (data.status === 'OTP_REQUIRED') {
                    // Show OTP field
                    otpGroup.style.display = 'block';
                    errorEl.style.color = '#fbbf24';
                    errorEl.textContent = data.message;
                    errorEl.style.display = 'block';
                    btn.disabled = false;
                    btn.textContent = 'Verify & Update Password';
                    // Focus OTP
                    otpInput.focus();
                } else {
                    // Success
                    alert('Password updated successfully.');
                    this.closePasswordModal();
                    this.loadLogs(); // Refresh logs
                }
            } else {
                errorEl.style.color = '#ef4444';
                errorEl.textContent = data.error || 'Failed to update password.';
                errorEl.style.display = 'block';
                btn.disabled = false;
                btn.innerHTML = otpGroup.style.display === 'block' ? 'Verify & Update Password' : 'Update Password';
            }
        } catch (err) {
            errorEl.textContent = 'Connection error.';
            errorEl.style.display = 'block';
            btn.disabled = false;
            btn.textContent = 'Update Password';
        }
    }
}

// Global functions for inline HTML calls
window.initiateDeleteAccount = () => window.securityManager.initiateDeleteAccount();
window.closeOtpModal = () => window.securityManager.closeOtpModal();
window.confirmDeleteAccount = () => window.securityManager.confirmDeleteAccount();
window.openPasswordModal = () => window.securityManager.openPasswordModal();
window.closePasswordModal = () => window.securityManager.closePasswordModal();
window.submitChangePassword = () => window.securityManager.submitChangePassword();

document.addEventListener('DOMContentLoaded', () => {
    window.securityManager = new SecurityManager();
});
