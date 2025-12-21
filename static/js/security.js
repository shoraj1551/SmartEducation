/**
 * SmartEducation - Security Logic
 */

class SecurityManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = '/';
            return;
        }

        // In a real app, we would fetch active sessions and security logs here
        // For this demo, we'll keep the UI mostly static but log the access
        this.logSecurityAccess();
    }

    async logSecurityAccess() {
        try {
            await fetch('/api/user/log-activity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({
                    type: 'security_audit_view',
                    description: 'User viewed their security audit log'
                })
            });
        } catch (err) {
            console.warn('Failed to log security audit view');
        }
    }

    handleRevokeSession(sessionId) {
        if (confirm('Are you sure you want to log out this device?')) {
            alert('Session revoked. In a production environment, this would invalidate the respective JWT.');
            // Implementation would call /api/auth/revoke-session
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.securityManager = new SecurityManager();
});
