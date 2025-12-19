/**
 * SmartEducation - Profile Management Logic
 */

class ProfileManager {
    constructor() {
        this.userData = JSON.parse(localStorage.getItem('user') || '{}');
        this.token = localStorage.getItem('token');

        // Element Bindings
        this.profileForm = document.getElementById('profileForm');
        this.profileInitials = document.getElementById('profileInitials');
        this.profileNameDisplay = document.getElementById('profileNameDisplay');
        this.profileEmailDisplay = document.getElementById('profileEmailDisplay');

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = 'index.html';
            return;
        }

        await this.fetchProfile();
        this.attachListeners();
    }

    async fetchProfile() {
        try {
            const response = await fetch('/api/user/profile', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const user = await response.json();

            if (response.ok) {
                this.populateForm(user);
                this.updateUI(user);
            } else {
                console.error('Failed to fetch profile:', user.error);
            }
        } catch (err) {
            console.error('Error fetching profile:', err);
        }
    }

    populateForm(user) {
        const fields = [
            'name', 'job_title', 'bio', 'education_info',
            'linkedin_url', 'github_url', 'website_url',
            'learning_goal', 'commitment_level', 'expertise_level'
        ];

        fields.forEach(field => {
            const el = document.getElementById(field);
            if (el) el.value = user[field] || '';
        });

        // Show verified badge for goal if set
        const goalVerified = document.getElementById('goalVerified');
        if (goalVerified) {
            goalVerified.style.display = user.learning_goal ? 'inline' : 'none';
        }

        // Handle interests (Array to Comma String)
        const interestsEl = document.getElementById('interests');
        if (interestsEl && Array.isArray(user.interests)) {
            interestsEl.value = user.interests.join(', ');
        }
    }

    updateUI(user) {
        this.profileNameDisplay.textContent = user.name || 'User';
        this.profileEmailDisplay.textContent = user.email || '';
        this.profileInitials.textContent = (user.name || 'U').charAt(0).toUpperCase();

        // Update local storage if name changed
        const currentLocal = JSON.parse(localStorage.getItem('user') || '{}');
        currentLocal.name = user.name;
        localStorage.setItem('user', JSON.stringify(currentLocal));
    }

    attachListeners() {
        this.profileForm.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    async handleSubmit(e) {
        e.preventDefault();

        const formData = {};
        const fields = [
            'name', 'job_title', 'bio', 'education_info',
            'linkedin_url', 'github_url', 'website_url',
            'learning_goal', 'commitment_level', 'expertise_level'
        ];

        fields.forEach(field => {
            const el = document.getElementById(field);
            if (el) formData[field] = el.value;
        });

        // Handle interests (Comma String to Array)
        const interestsVal = document.getElementById('interests').value;
        formData['interests'] = interestsVal.split(',')
            .map(i => i.trim())
            .filter(i => i !== '');

        const btn = this.profileForm.querySelector('button[type="submit"]');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
        btn.disabled = true;

        try {
            const response = await fetch('/api/user/profile', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                this.updateUI(result.user);
                // Log activity
                await this.logProfileActivity();
                alert('Profile updated successfully!');
            } else {
                alert(result.error || 'Failed to update profile');
            }
        } catch (err) {
            console.error('Error updating profile:', err);
            alert('An error occurred while saving.');
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }

    async logProfileActivity() {
        try {
            await fetch('/api/user/log-activity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({
                    type: 'profile_update',
                    description: 'User updated their profile information'
                })
            });
        } catch (err) {
            console.warn('Failed to log profile activity');
        }
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    new ProfileManager();
});
