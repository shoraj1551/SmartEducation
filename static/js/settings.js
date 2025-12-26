/**
 * settings.js
 * Handles Premium Settings UI interactions and API integrations.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Managers
    new ThemeManager();
    new PreferencesManager();
    new SessionManager();
    new DataManager();
});


/* ===== Theme Manager ===== */
class ThemeManager {
    constructor() {
        this.themeCards = document.querySelectorAll('.theme-card');
        // Force reset to 'dark' if 'sunset' or 'mode-night' was active
        const saved = localStorage.getItem('theme_preference');
        if (saved === 'sunset' || saved === 'night') {
            this.currentTheme = 'dark';
            localStorage.setItem('theme_preference', 'dark');
        } else {
            this.currentTheme = saved || 'dark';
        }

        this.init();
    }

    init() {
        // Set initial active state
        this.setActiveCard(this.currentTheme);

        // Click listeners
        this.themeCards.forEach(card => {
            card.addEventListener('click', () => {
                const theme = card.dataset.theme;
                this.applyTheme(theme);
            });
        });
    }

    setActiveCard(theme) {
        this.themeCards.forEach(c => c.classList.remove('active'));
        const target = document.querySelector(`.theme-card[data-theme="${theme}"]`);
        if (target) target.classList.add('active');
    }

    async applyTheme(theme) {
        // 1. Apply to DOM immediately
        document.body.className = `theme-${theme}`;
        this.currentTheme = theme;
        this.setActiveCard(theme);
        localStorage.setItem('theme_preference', theme);

        // 2. Sync with Backend
        try {
            await fetch('/api/user/preferences', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ theme_preference: theme })
            });
        } catch (err) {
            console.error('Failed to save theme to backend', err);
        }
    }
}

/* ===== Preferences Manager (Timezone, Notifications) ===== */
class PreferencesManager {
    constructor() {
        this.timezoneSelect = document.getElementById('timezone');
        this.toggles = {
            email: document.getElementById('email_notifications'),
            mobile: document.getElementById('mobile_notifications'),
            marketing: document.getElementById('marketing_emails')
        };

        this.loadPreferences();
        this.attachListeners();
    }

    async loadPreferences() {
        try {
            const response = await fetch('/api/user/preferences', {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });
            const data = await response.json();

            // Set Timezone
            // If data.timezone is available, use it. Otherwise, guess local.
            // Note: The API currently returns 'timezone' in profile or prefs?
            // Checking user_routes.py, 'timezone' wasn't strictly in the prefs endpoint list but added to User model.
            // We might need to fetch profile for timezone if it's not in prefs.
            // Let's assume it's synced or we fetch profile. 
            if (data.timezone) this.timezoneSelect.value = data.timezone;
            else this.timezoneSelect.value = Intl.DateTimeFormat().resolvedOptions().timeZone;

            // Set Toggles
            if (this.toggles.email) this.toggles.email.checked = data.email_notifications;
            if (this.toggles.mobile) this.toggles.mobile.checked = data.mobile_notifications;
            if (this.toggles.marketing) this.toggles.marketing.checked = data.marketing_emails;

        } catch (e) { console.error("Error loading prefs", e); }
    }

    attachListeners() {
        // Timezone Change
        this.timezoneSelect.addEventListener('change', (e) => {
            this.savePreference({ timezone: e.target.value });
        });

        // Toggles
        Object.entries(this.toggles).forEach(([key, element]) => {
            if (!element) return;
            element.addEventListener('change', (e) => {
                const payload = {};
                if (key === 'email') payload.email_notifications = e.target.checked;
                if (key === 'mobile') payload.mobile_notifications = e.target.checked;
                if (key === 'marketing') payload.marketing_emails = e.target.checked;
                this.savePreference(payload);
            });
        });
    }

    async savePreference(data) {
        try {
            await fetch('/api/user/preferences', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(data)
            });
            // Optional: Show subtle toast
        } catch (e) { console.error("Save failed", e); }
    }
}

/* ===== Session Manager ===== */
class SessionManager {
    constructor() {
        this.container = document.getElementById('activeSessionsList');
        this.loadSessions();
    }

    async loadSessions() {
        try {
            const response = await fetch('/api/user/sessions', {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });
            const sessions = await response.json();
            this.render(sessions);
        } catch (e) {
            this.container.innerHTML = '<p class="text-danger">Failed to load sessions.</p>';
        }
    }

    render(sessions) {
        if (!sessions || sessions.length === 0) {
            this.container.innerHTML = '<p style="color:var(--text-secondary)">No active sessions found.</p>';
            return;
        }

        this.container.innerHTML = sessions.map(session => `
            <div class="session-item">
                <div class="session-icon">
                    <i class="fas ${this.getDeviceIcon(session.device_info)}"></i>
                </div>
                <div class="session-info">
                    <div class="session-title">
                        ${session.device_info || 'Unknown Device'}
                        ${session.is_current ? '<span style="color:var(--primary); font-size:0.8em; margin-left:0.5rem">(Current)</span>' : ''}
                    </div>
                    <div class="session-meta">
                        ${session.ip_address} • Active ${this.formatDate(session.created_at || session.login_time)}
                    </div>
                </div>
                ${!session.is_current ? `
                    <button class="revoke-btn" onclick="revokeSession('${session.session_id}')">
                        Revoke
                    </button>
                ` : ''}
            </div>
        `).join('');

        // Expose revoke function globally for onclick
        window.revokeSession = (id) => this.revoke(id);
    }

    getDeviceIcon(userAgent) {
        if (!userAgent) return 'fa-desktop';
        if (/mobile/i.test(userAgent)) return 'fa-mobile-alt';
        if (/tablet/i.test(userAgent)) return 'fa-tablet-alt';
        return 'fa-desktop';
    }

    formatDate(dateStr) {
        if (!dateStr) return 'Recently';
        return new Date(dateStr).toLocaleDateString();
    }

    async revoke(sessionId) {
        if (!confirm('Are you sure you want to log out this device?')) return;

        try {
            const res = await fetch(`/api/user/sessions/${sessionId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });
            if (res.ok) {
                this.loadSessions(); // Reload list
            } else {
                alert('Failed to revoke session');
            }
        } catch (e) { alert('Error connecting to server'); }
    }
}

/* ===== Data Manager ===== */
class DataManager {
    constructor() {
        const btn = document.getElementById('exportDataBtn');
        if (btn) btn.addEventListener('click', () => this.exportData());
    }

    async exportData() {
        const btn = document.getElementById('exportDataBtn');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Preparing...';
        btn.disabled = true;

        try {
            const response = await fetch('/api/user/export', {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });

            if (!response.ok) throw new Error('Export failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `smart_education_data_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();

        } catch (e) {
            alert('Failed to export data. Please try again.');
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }
}
