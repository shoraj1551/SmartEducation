/**
 * SmartEducation - Global Common Logic
 * Shared across all dashboard pages
 */

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
            window.location.href = 'index.html';
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
        const nameBrief = document.getElementById('userNameBrief');
        const initials = document.getElementById('avatarInitials');

        if (nameBrief) nameBrief.textContent = this.userData.name || 'User';
        if (initials) {
            const parts = (this.userData.name || 'U').split(' ');
            initials.textContent = parts.length > 1
                ? (parts[0][0] + parts[1][0]).toUpperCase()
                : parts[0][0].toUpperCase();
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
                window.location.href = 'index.html';
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
