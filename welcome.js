
/**
 * SmartEducation - Premium Survey Wizard Logic
 */

class SurveyWizard {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 4;
        this.surveyData = {};

        // Element Bindings
        this.steps = document.querySelectorAll('.survey-step');
        this.progressBar = document.getElementById('progress-bar');
        this.progressText = document.getElementById('progress-text');
        this.dots = document.querySelectorAll('.dot');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.skipBtn = document.getElementById('skip-btn');

        // Overlays
        this.successOverlay = document.getElementById('success-overlay');
        this.allSetOverlay = document.getElementById('all-set-overlay');
        this.userDisplayName = document.getElementById('user-display-name');

        this.init();
    }

    init() {
        // 1. Set User Name from session/localStorage
        const userData = JSON.parse(localStorage.getItem('user') || '{}');
        this.userDisplayName.textContent = userData.name || 'Learner';

        // 2. Play Initial Entrance Animation
        this.playEntrance();

        // 3. Attach Event Listeners
        this.attachListeners();

        // 4. Update UI to Initial State
        this.updateUI();
    }

    playEntrance() {
        // Show success overlay for 2 seconds then fade into survey
        setTimeout(() => {
            this.successOverlay.style.opacity = '0';
            setTimeout(() => {
                this.successOverlay.style.display = 'none';
                document.querySelector('.welcome-container').style.opacity = '1';
            }, 500);
        }, 2500);
    }

    attachListeners() {
        // Option Card Clicks
        document.querySelectorAll('.option-card').forEach(card => {
            card.addEventListener('click', () => this.handleOptionClick(card));
        });

        // Navigation
        this.prevBtn.addEventListener('click', () => this.goToPrevStep());
        this.nextBtn.addEventListener('click', () => this.goToNextStep());
        this.skipBtn.addEventListener('click', () => this.goToNextStep()); // Skip is just next without selection
    }

    handleOptionClick(card) {
        const stepEl = card.closest('.survey-step');
        const stepIndex = parseInt(stepEl.dataset.step);
        const type = stepEl.dataset.type; // 'single' or 'multi'
        const value = card.dataset.value;

        if (type === 'single') {
            // Remove selection from all cards in this step
            stepEl.querySelectorAll('.option-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            this.surveyData[stepIndex] = value;

            // Auto advance for single select
            setTimeout(() => this.goToNextStep(), 400);
        } else {
            // Toggle selection for multi
            card.classList.toggle('selected');

            // Collect all selected values
            const selectedCards = stepEl.querySelectorAll('.option-card.selected');
            this.surveyData[stepIndex] = Array.from(selectedCards).map(c => c.dataset.value);
        }
    }

    goToNextStep() {
        if (this.currentStep < this.totalSteps) {
            this.currentStep++;
            this.updateUI();
        } else {
            this.completeSurvey();
        }
    }

    goToPrevStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateUI();
        }
    }

    updateUI() {
        // 1. Update Step Visibility with animation
        this.steps.forEach((step, index) => {
            const stepNum = index + 1;
            step.classList.remove('active', 'exit-left');

            if (stepNum === this.currentStep) {
                step.classList.add('active');
            } else if (stepNum < this.currentStep) {
                step.classList.add('exit-left');
            }
        });

        // 2. Update Progress Bar
        const progress = (this.currentStep / this.totalSteps) * 100;
        this.progressBar.style.width = `${progress}%`;
        this.progressText.textContent = `Step ${this.currentStep} of ${this.totalSteps}`;

        // 3. Update Dots
        this.dots.forEach((dot, index) => {
            dot.classList.toggle('active', (index + 1) === this.currentStep);
        });

        // 4. Update Navigation Buttons
        this.prevBtn.style.display = this.currentStep === 1 ? 'none' : 'flex';
        this.nextBtn.innerHTML = this.currentStep === this.totalSteps ?
            'Finish <i class="fas fa-check"></i>' :
            'Next <i class="fas fa-arrow-right"></i>';
    }

    async completeSurvey() {
        // 1. Prepare formatted data for backend
        const formattedData = {
            goal: this.surveyData[1],
            interests: this.surveyData[2],
            commitment: this.surveyData[3],
            level: this.surveyData[4]
        };

        // 2. Save to localStorage (legacy support)
        localStorage.setItem('surveyPreferences', JSON.stringify(this.surveyData));

        // 3. Send to Backend API
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const response = await fetch('/api/user/onboarding', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(formattedData)
                });

                const result = await response.json();
                if (response.ok) {
                    console.log('Survey data persisted to cloud');
                } else {
                    console.error('Failed to persist survey data:', result.error);
                }
            } catch (err) {
                console.error('Network error persisting survey:', err);
            }
        }

        // 4. Final transition
        document.querySelector('.welcome-container').style.opacity = '0';

        setTimeout(() => {
            this.allSetOverlay.style.display = 'flex';
            this.allSetOverlay.style.opacity = '1';

            // Redirect after 3s
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 3000);
        }, 500);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.surveyWizard = new SurveyWizard();
});
