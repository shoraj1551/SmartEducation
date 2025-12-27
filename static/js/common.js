/**
 * SmartEducation - Global Common Logic
 * Shared across all dashboard pages
 */

// Global XSS Protection Utility
window.escapeHTML = function (str) {
    if (!str) return '';
    return str.toString()
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
};

class CommonUI {
    constructor() {
        this.token = localStorage.getItem('token');
        this.userData = null;

        // UI Bindings
        this.userDropdown = document.getElementById('userDropdown');
        this.userMenuTrigger = document.getElementById('userMenuTrigger');
        this.sidebarLogout = document.getElementById('sidebarLogout');
        this.dropdownLogout = document.getElementById('dropdownLogout');

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = '/';
            return;
        }

        await this.fetchBasicProfile();
        this.setupDropdown();
        this.setupLogout();
        this.highlightActiveNav();
    }

    async fetchBasicProfile() {
        try {
            const response = await fetch('/api/user/profile', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            if (response.ok) {
                this.userData = await response.json();
                localStorage.setItem('user', JSON.stringify(this.userData));
                this.updateUI();
            }
        } catch (err) {
            console.error('Error fetching global profile:', err);
        }
    }

    updateUI() {
        if (!this.userData) return;

        // Update name and avatar initials globally
        // Correct ID from header.html is 'headerUserName'
        const nameBrief = document.getElementById('headerUserName');
        // Correct ID from header.html is 'headerAvatarInitials'
        const avatarInitialsElement = document.getElementById('headerAvatarInitials');

        if (nameBrief) nameBrief.textContent = this.userData.name || 'User';

        if (avatarInitialsElement) {
            if (this.userData.profile_picture) {
                avatarInitialsElement.textContent = ''; // Clear text initials
                avatarInitialsElement.style.backgroundImage = `url('${this.userData.profile_picture}')`;
                avatarInitialsElement.style.backgroundSize = 'cover';
                avatarInitialsElement.style.backgroundPosition = 'center';
                avatarInitialsElement.style.backgroundRepeat = 'no-repeat'; // Ensure no repeat
            } else {
                const parts = (this.userData.name || 'U').split(' ');
                avatarInitialsElement.textContent = parts.length > 1
                    ? (parts[0][0] + parts[1][0]).toUpperCase()
                    : parts[0][0].toUpperCase();
                avatarInitialsElement.style.backgroundImage = 'none'; // Clear background image
            }
        }

        // Apply Global Preferences
        if (this.userData.reduced_motion) {
            document.body.classList.add('reduced-motion');
        } else {
            document.body.classList.remove('reduced-motion');
        }

        if (this.userData.high_contrast) {
            document.body.classList.add('high-contrast');
        } else {
            document.body.classList.remove('high-contrast');
        }

        // Apply Learning Time Theme
        // Remove existing mode classes first
        document.body.classList.remove('mode-morning', 'mode-deep-focus', 'mode-night');

        // Normalize preference string (e.g. "Morning Owl" -> "mode-morning")
        if (this.userData.preferred_learning_time) {
            const pref = this.userData.preferred_learning_time.toLowerCase();
            if (pref.includes('morning')) {
                document.body.classList.add('mode-morning');
            } else if (pref.includes('focus')) {
                document.body.classList.add('mode-deep-focus');
            } else if (pref.includes('night')) {
                document.body.classList.add('mode-night');
            }
        }
    }

    setupDropdown() {
        if (!this.userMenuTrigger || !this.userDropdown) return;

        this.userMenuTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            this.userDropdown.classList.toggle('active');
        });

        document.addEventListener('click', () => {
            this.userDropdown.classList.remove('active');
        });

        this.userDropdown.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    setupLogout() {
        const handleLogout = () => {
            if (confirm('Are you sure you want to log out?')) {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                sessionStorage.clear();
                window.location.href = '/';
            }
        };

        if (this.sidebarLogout) this.sidebarLogout.addEventListener('click', handleLogout);
        if (this.dropdownLogout) this.dropdownLogout.addEventListener('click', handleLogout);
    }

    highlightActiveNav() {
        const currentPath = window.location.pathname.split('/').pop();
        const navItems = document.querySelectorAll('.nav-item');

        navItems.forEach(item => {
            const href = item.getAttribute('href');
            if (href === currentPath) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }
}

// Initialize on Pageload
document.addEventListener('DOMContentLoaded', () => {
    window.commonUI = new CommonUI();
});
