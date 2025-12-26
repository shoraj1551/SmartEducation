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

        // Avatar Bindings
        this.editAvatarBtn = document.getElementById('editAvatarBtn');
        this.avatarInput = document.getElementById('avatarInput');

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = '/';
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
        this.profileNameDisplay.textContent = user.name || 'User';
        this.profileEmailDisplay.textContent = user.email || '';

        if (user.profile_picture) {
            this.profileInitials.textContent = '';
            this.profileInitials.style.backgroundImage = `url('${user.profile_picture}')`;
            this.profileInitials.style.backgroundSize = 'cover';
            this.profileInitials.style.backgroundPosition = 'center';
        } else {
            this.profileInitials.style.backgroundImage = 'none';
            this.profileInitials.textContent = (user.name || 'U').charAt(0).toUpperCase();
        }

        // Update local storage if name changed
        const currentLocal = JSON.parse(localStorage.getItem('user') || '{}');
        currentLocal.name = user.name;
        localStorage.setItem('user', JSON.stringify(currentLocal));
    }

    attachListeners() {
        this.profileForm.addEventListener('submit', (e) => this.handleSubmit(e));

        // Explicitly bind click events for upload
        if (this.editAvatarBtn && this.avatarInput) {
            this.editAvatarBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.avatarInput.click();
            });
        }

        // Also allow clicking the main avatar to trigger upload (Better UX)
        if (this.profileInitials && this.avatarInput) {
            this.profileInitials.style.cursor = 'pointer';
            this.profileInitials.addEventListener('click', (e) => {
                // Prevent double trigger if clicking the button itself which bubbles
                if (e.target.closest('.edit-avatar-btn')) return;
                this.avatarInput.click();
            });
        }

        if (this.avatarInput) {
            this.avatarInput.addEventListener('change', (e) => this.handleAvatarUpload(e));
        }
    }

    async handleAvatarUpload(e) {
        alert('File selected! Starting upload...');
        const file = e.target.files[0];
        if (!file) {
            alert('No file detected');
            return;
        }

        const formData = new FormData();
        formData.append('profile_picture', file);

        // Visual feedback
        const icon = this.editAvatarBtn.querySelector('i');
        icon.className = 'fas fa-spinner fa-spin';

        try {
            const response = await fetch('/api/user/profile-picture', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                    // Content-Type not set for FormData
                },
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                // Update UI immediately
                this.profileInitials.textContent = '';
                this.profileInitials.style.backgroundImage = `url('${result.url}')`;
                this.profileInitials.style.backgroundSize = 'cover';
                this.profileInitials.style.backgroundPosition = 'center';

                // Update Global User Data
                const currentLocal = JSON.parse(localStorage.getItem('user') || '{}');
                currentLocal.profile_picture = result.url;
                localStorage.setItem('user', JSON.stringify(currentLocal));

                // Try updating global nav if present
                if (window.commonUI) {
                    window.commonUI.userData.profile_picture = result.url;
                    window.commonUI.updateUI();
                }

                alert('Profile picture updated successfully!');
            } else {
                alert(result.error || 'Failed to upload image. Please try a smaller file (max 5MB).');
            }
        } catch (err) {
            console.error(err);
            alert('Upload failed');
        } finally {
            icon.className = 'fas fa-camera';
            this.avatarInput.value = ''; // Reset
        }
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
