/**
 * SmartEducation - Preferences Logic
 */

class PreferencesManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.saveBtn = document.getElementById('savePrefs');
        this.timeOptions = document.querySelectorAll('.time-option');

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = 'index.html';
            return;
        }

        await this.loadPreferences();
        this.attachListeners();
    }

    async loadPreferences() {
        try {
            const response = await fetch('/api/user/preferences', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();

            if (response.ok) {
                // Populate multi-selects and toggles
                this.populateUI(data);
            }
        } catch (err) {
            console.error('Error loading preferences:', err);
        }
    }

    populateUI(data) {
        // Theme / Time logic would go here
        // For now let's handle the checkboxes
        const checkboxes = ['daily_reminders', 'ai_insights', 'community_milestones', 'reduced_motion', 'high_contrast'];
        checkboxes.forEach(id => {
            const el = document.getElementById(id);
            if (el && data[id] !== undefined) el.checked = data[id];
        });

        // Set active time option
        if (data.preferred_learning_time) {
            this.timeOptions.forEach(opt => {
                opt.classList.toggle('active', opt.dataset.time === data.preferred_learning_time);
            });
        }
    }

    attachListeners() {
        // Time selection
        this.timeOptions.forEach(opt => {
            opt.addEventListener('click', () => {
                this.timeOptions.forEach(o => o.classList.remove('active'));
                opt.classList.add('active');
            });
        });

        // Save
        this.saveBtn.addEventListener('click', () => this.handleSave());
    }

    async handleSave() {
        const activeTime = document.querySelector('.time-option.active')?.dataset.time;
        const prefs = {
            preferred_learning_time: activeTime,
            daily_reminders: document.getElementById('daily_reminders')?.checked,
            ai_insights: document.getElementById('ai_insights')?.checked,
            community_milestones: document.getElementById('community_milestones')?.checked,
            reduced_motion: document.getElementById('reduced_motion')?.checked,
            high_contrast: document.getElementById('high_contrast')?.checked,
        };

        const originalText = this.saveBtn.textContent;
        this.saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Syncing...';
        this.saveBtn.disabled = true;

        try {
            const response = await fetch('/api/user/preferences', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify(prefs)
            });

            if (response.ok) {
                alert('Preferences synchronized successfully!');
            } else {
                alert('Failed to save preferences.');
            }
        } catch (err) {
            console.error('Error saving preferences:', err);
        } finally {
            this.saveBtn.innerHTML = originalText;
            this.saveBtn.disabled = false;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new PreferencesManager();
});
