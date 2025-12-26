class PreferenceManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.timeOptions = document.querySelectorAll('.time-option');
        this.saveBtn = document.getElementById('savePrefs');

        // Engagement Toggles
        this.dailyReminders = document.getElementById('daily_reminders');
        this.aiInsights = document.getElementById('ai_insights');
        this.communityMilestones = document.getElementById('community_milestones');

        // UI Toggles
        this.reducedMotion = document.getElementById('reduced_motion');
        this.highContrast = document.getElementById('high_contrast');

        // Explanation Data
        this.explanations = {
            'Morning': {
                title: 'Morning Owl Architecture',
                text: 'Designed for early risers. We suppress non-critical alerts after 12 PM.',
                rules: ['Active Window: 05:00 - 11:00', 'Prioritizes planning tasks', 'Evening silence enforced']
            },
            'Deep Focus': {
                title: 'Deep Focus Architecture',
                text: 'Minimizes interruptions. Notifications are batched to avoid breaking your flow.',
                rules: ['Active Window: 09:00 - 17:00 (Configurable)', 'Batch notifications', 'Long-form content priority']
            },
            'Night': {
                title: 'Night Owl Architecture',
                text: 'Optimize for late-night learning. Morning pings are suppressed.',
                rules: ['Active Window: 19:00 - 01:00', 'Video & Practice priority', 'Morning silence enforced']
            }
        };

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = '/login';
            return;
        }

        // Load current config
        await this.loadPreferences();

        this.attachListeners();
    }

    async loadPreferences() {
        try {
            const res = await fetch('/api/preferences/config', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await res.json();

            if (data.prefs) {
                // Set Time Logic
                const userTime = data.prefs.time || 'morning';
                // Convert db format (morning, deep_focus, night) to UI format (Morning, Deep Focus, Night)
                let uiTime = 'Morning';
                if (userTime === 'deep_focus') uiTime = 'Deep Focus';
                if (userTime === 'night') uiTime = 'Night';

                this.setActiveTimeOption(uiTime);

                // Set Toggles
                if (this.dailyReminders) this.dailyReminders.checked = data.prefs.reminders;
                if (this.aiInsights) this.aiInsights.checked = data.prefs.ai_insights;
                // Add others if returned by API
            }
        } catch (e) {
            console.error("Failed to load prefs", e);
        }
    }

    setActiveTimeOption(timeName) {
        this.timeOptions.forEach(opt => {
            opt.classList.remove('active');
            if (opt.dataset.time === timeName) {
                opt.classList.add('active');
            }
        });
        this.updateExplanation(timeName);
    }

    updateExplanation(timeName) {
        const data = this.explanations[timeName] || this.explanations['Morning'];
        document.getElementById('explainerTitle').textContent = data.title;
        document.getElementById('explainerBody').textContent = data.text;

        const list = document.getElementById('explainerRules');
        list.innerHTML = data.rules.map(r => `<li><i class="fas fa-check"></i> ${r}</li>`).join('');
        list.style.display = 'block';
    }

    attachListeners() {
        // Time selection
        this.timeOptions.forEach(opt => {
            opt.addEventListener('click', () => {
                this.setActiveTimeOption(opt.dataset.time);
            });
        });

        // Save Button
        this.saveBtn.addEventListener('click', () => this.savePreferences());
    }

    async savePreferences() {
        const activeTimeEl = document.querySelector('.time-option.active');
        const selectedTime = activeTimeEl ? activeTimeEl.dataset.time : 'Morning';

        this.saveBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Syncing...';
        this.saveBtn.disabled = true;

        const payload = {
            preferred_learning_time: selectedTime,
            daily_reminders: this.dailyReminders ? this.dailyReminders.checked : true,
            ai_insights: this.aiInsights ? this.aiInsights.checked : true,
            community_milestones: this.communityMilestones ? this.communityMilestones.checked : false,
            reduced_motion: this.reducedMotion ? this.reducedMotion.checked : false,
            high_contrast: this.highContrast ? this.highContrast.checked : false
        };

        try {
            const res = await fetch('/api/preferences/update', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (res.ok) {
                // Show Success
                this.saveBtn.innerHTML = '<i class="fas fa-check"></i> Synced';
                this.saveBtn.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)'; // Success Green

                // INSTANTLY APPLY STYLES
                if (this.reducedMotion && this.reducedMotion.checked) {
                    document.body.classList.add('reduced-motion');
                } else {
                    document.body.classList.remove('reduced-motion');
                }

                if (this.highContrast && this.highContrast.checked) {
                    document.body.classList.add('high-contrast');
                } else {
                    document.body.classList.remove('high-contrast');
                }

                // Apply Learning Time Theme
                document.body.classList.remove('mode-morning', 'mode-deep-focus', 'mode-night');
                if (selectedTime === 'Morning') document.body.classList.add('mode-morning');
                if (selectedTime === 'Deep Focus') document.body.classList.add('mode-deep-focus');
                if (selectedTime === 'Night') document.body.classList.add('mode-night');

                // Update global commonUI if it exists
                if (window.commonUI && window.commonUI.userData) {
                    window.commonUI.userData.reduced_motion = this.reducedMotion.checked;
                    window.commonUI.userData.high_contrast = this.highContrast.checked;
                    window.commonUI.userData.preferred_learning_time = selectedTime;
                }

                setTimeout(() => {
                    this.saveBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Sync Preferences';
                    this.saveBtn.style.background = ''; // Reset
                    this.saveBtn.disabled = false;
                }, 2000);
            } else {
                alert('Failed to save preferences');
                this.saveBtn.innerHTML = 'Try Again';
                this.saveBtn.disabled = false;
            }
        } catch (e) {
            console.error(e);
            this.saveBtn.innerHTML = 'Error';
            this.saveBtn.disabled = false;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.preferenceManager = new PreferenceManager();
});
