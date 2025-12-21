
/**
 * SmartEducation - Premium Survey Wizard Logic (IMPROVEMENT-001)
 * Updated for new personalized survey questions
 */

class SurveyWizard {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 6;
        this.surveyData = {
            user_role: '',
            learning_goals: [],
            learning_type: '',
            deadline_type: '',
            daily_time_commitment: '',
            learning_blockers: []
        };

        // Element Bindings
        this.steps = document.querySelectorAll('.survey-step');
        this.progressBar = document.getElementById('progress-bar');
        this.progressText = document.getElementById('progress-text');
        this.dots = document.querySelectorAll('.dot');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.skipBtn = document.getElementById('skip-btn');
        this.skipContainer = document.getElementById('skip-container');

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
        this.skipBtn.addEventListener('click', () => this.skipCurrentStep());
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

            // Map step to data field
            switch (stepIndex) {
                case 1:
                    this.surveyData.user_role = value;
                    break;
                case 3:
                    this.surveyData.learning_type = value;
                    break;
                case 4:
                    this.surveyData.deadline_type = value;
                    break;
                case 5:
                    this.surveyData.daily_time_commitment = value;
                    break;
            }

            // Auto advance for single select
            setTimeout(() => this.goToNextStep(), 400);
        } else {
            // Toggle selection for multi (Steps 2 and 6)
            card.classList.toggle('selected');

            // Collect all selected values
            const selectedCards = stepEl.querySelectorAll('.option-card.selected');
            const selectedValues = Array.from(selectedCards).map(c => c.dataset.value);

            if (stepIndex === 2) {
                this.surveyData.learning_goals = selectedValues;
            } else if (stepIndex === 6) {
                this.surveyData.learning_blockers = selectedValues;
            }
        }
    }

    goToNextStep() {
        // Validate current step before proceeding
        if (!this.validateCurrentStep()) {
            alert('Please make a selection before proceeding.');
            return;
        }

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

    skipCurrentStep() {
        // Only Step 6 (bonus question) can be skipped
        if (this.currentStep === 6) {
            this.surveyData.learning_blockers = [];
            this.completeSurvey();
        }
    }

    validateCurrentStep() {
        const currentStepEl = this.steps[this.currentStep - 1];
        const type = currentStepEl.dataset.type;

        if (type === 'single') {
            const selected = currentStepEl.querySelector('.option-card.selected');
            return selected !== null;
        } else {
            // Multi-select: at least one selection required (except Step 6 which is optional)
            if (this.currentStep === 6) {
                return true; // Step 6 is optional
            }
            const selectedCards = currentStepEl.querySelectorAll('.option-card.selected');
            return selectedCards.length > 0;
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

        // 5. Show/Hide Skip Button (only on Step 6)
        this.skipContainer.style.display = this.currentStep === 6 ? 'flex' : 'none';
    }

    getMotivationalQuote() {
        // Personalized quotes based on user role (BUG-006)
        const quotes = {
            school: [
                { text: "Education is the most powerful weapon which you can use to change the world.", author: "Nelson Mandela" },
                { text: "The beautiful thing about learning is that no one can take it away from you.", author: "B.B. King" },
                { text: "Your education is a dress rehearsal for a life that is yours to lead.", author: "Nora Ephron" }
            ],
            college: [
                { text: "The future belongs to those who believe in the beauty of their dreams.", author: "Eleanor Roosevelt" },
                { text: "Success is not final, failure is not fatal: it is the courage to continue that counts.", author: "Winston Churchill" },
                { text: "Your time is limited, don't waste it living someone else's life.", author: "Steve Jobs" }
            ],
            professional: [
                { text: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
                { text: "Success is walking from failure to failure with no loss of enthusiasm.", author: "Winston Churchill" },
                { text: "Don't watch the clock; do what it does. Keep going.", author: "Sam Levenson" }
            ],
            freelancer: [
                { text: "The secret of getting ahead is getting started.", author: "Mark Twain" },
                { text: "Opportunities don't happen. You create them.", author: "Chris Grosser" },
                { text: "Success usually comes to those who are too busy to be looking for it.", author: "Henry David Thoreau" }
            ],
            career_switcher: [
                { text: "It's never too late to be what you might have been.", author: "George Eliot" },
                { text: "The only impossible journey is the one you never begin.", author: "Tony Robbins" },
                { text: "Change is the end result of all true learning.", author: "Leo Buscaglia" }
            ],
            other: [
                { text: "The journey of a thousand miles begins with a single step.", author: "Lao Tzu" },
                { text: "Learning never exhausts the mind.", author: "Leonardo da Vinci" },
                { text: "Live as if you were to die tomorrow. Learn as if you were to live forever.", author: "Mahatma Gandhi" }
            ]
        };

        const userRole = this.surveyData.user_role || 'other';
        const roleQuotes = quotes[userRole] || quotes.other;
        const randomQuote = roleQuotes[Math.floor(Math.random() * roleQuotes.length)];

        return randomQuote;
    }

    showMotivationalQuote() {
        const quote = this.getMotivationalQuote();
        const quoteText = document.getElementById('motivational-text');
        const quoteAuthor = document.getElementById('quote-author');

        if (quoteText && quoteAuthor) {
            quoteText.textContent = `"${quote.text}"`;
            quoteAuthor.textContent = `- ${quote.author}`;
        }
    }

    async completeSurvey() {
        console.log('Survey completed with data:', this.surveyData);

        // Save to localStorage
        localStorage.setItem('surveyPreferences', JSON.stringify(this.surveyData));

        // Send to Backend API
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const response = await fetch('/api/user/onboarding', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(this.surveyData)
                });

                const result = await response.json();
                if (response.ok) {
                    console.log('Survey data persisted to database');
                } else {
                    console.error('Failed to persist survey data:', result.error);
                }
            } catch (err) {
                console.error('Network error persisting survey:', err);
            }
        }

        // Final transition
        document.querySelector('.welcome-container').style.opacity = '0';

        setTimeout(() => {
            // Show personalized motivational quote (BUG-006)
            this.showMotivationalQuote();

            this.allSetOverlay.style.display = 'flex';
            this.allSetOverlay.style.opacity = '1';

            // Clear token and redirect to login after 3s (BUG-005, BUG-006 fix)
            setTimeout(() => {
                // Clear any existing tokens to force fresh login
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                // Redirect to login page with auto-open parameter
                window.location.href = '/?login=true';
            }, 4000);  // Extended to 4s to enjoy the motivational message
        }, 500);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.surveyWizard = new SurveyWizard();
});
