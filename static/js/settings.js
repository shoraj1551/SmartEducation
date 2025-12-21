/**
 * SmartEducation - Settings & Preferences Management
 */

class SettingsManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.preferences = {};

        // Element Bindings
        this.themeOptions = document.querySelectorAll('.theme-option');
        this.toggles = {
            email_notifications: document.getElementById('email_notifications'),
            mobile_notifications: document.getElementById('mobile_notifications'),
            marketing_emails: document.getElementById('marketing_emails')
        };

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = '/';
            return;
        }

        await this.fetchPreferences();
        this.attachListeners();
    }

    async fetchPreferences() {
        try {
            const response = await fetch('/api/user/preferences', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();

            if (response.ok) {
                this.preferences = data;
                this.applyPreferences();
            }
        } catch (err) {
            console.error('Error fetching preferences:', err);
        }
    }

    applyPreferences() {
        // Apply theme selection UI
        this.themeOptions.forEach(opt => {
            opt.classList.toggle('active', opt.dataset.theme === this.preferences.theme_preference);
        });

        // Apply toggle states
        Object.keys(this.toggles).forEach(key => {
            if (this.toggles[key]) {
                this.toggles[key].checked = this.preferences[key];
            }
        });

        // Apply actual theme to body (for preview)
        this.applyThemeToBody(this.preferences.theme_preference);
    }

    applyThemeToBody(theme) {
        document.body.className = ''; // Reset
        if (theme === 'midnight') {
            document.body.style.background = '#000000';
        } else if (theme === 'glassy') {
            document.body.style.background = 'linear-gradient(135deg, #1e293b, #0f172a)';
        } else {
            document.body.style.background = '#0f172a';
        }
    }

    attachListeners() {
        // Theme selection
        this.themeOptions.forEach(opt => {
            opt.addEventListener('click', () => {
                const theme = opt.dataset.theme;
                this.updatePreference('theme_preference', theme);

                // UI feedback
                this.themeOptions.forEach(o => o.classList.remove('active'));
                opt.classList.add('active');
                this.applyThemeToBody(theme);
            });
        });

        // Toggle switches
        Object.keys(this.toggles).forEach(key => {
            this.toggles[key].addEventListener('change', (e) => {
                this.updatePreference(key, e.target.checked);
            });
        });
    }

    async updatePreference(key, value) {
        try {
            const response = await fetch('/api/user/preferences', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ [key]: value })
            });

            if (response.ok) {
                this.preferences[key] = value;
                // Optional: log activity for significant changes
                if (key === 'theme_preference') {
                    this.logActivity('theme_change', `Changed theme to ${value}`);
                }
            } else {
                console.error('Failed to update preference');
            }
        } catch (err) {
            console.error('Error updating preference:', err);
        }
    }

    async logActivity(type, desc) {
        try {
            await fetch('/api/user/log-activity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ type, description: desc })
            });
        } catch (err) {
            console.warn('Failed to log setting activity');
        }
    }
}

function handleDeleteAccount() {
    if (confirm('CRITICAL: Are you sure you want to delete your account? This action is permanent and cannot be undone.')) {
        if (confirm('Final confirmation: All your data will be wiped.')) {
            alert('Account deletion request received. In a real system, this would call DELETE /api/user/account and redirect to landing page.');
            // For now, just logout
            localStorage.clear();
            window.location.href = '/';
        }
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    new SettingsManager();
});
