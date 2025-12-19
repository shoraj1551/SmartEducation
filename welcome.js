
// Welcome Wizard Logic

class SurveyWizard {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 5; // 4 questions + 1 finish
        this.formData = {};

        // Elements
        this.steps = document.querySelectorAll('.wizard-step');
        this.dots = document.querySelectorAll('.progress-dot');
        this.overlay = document.getElementById('successOverlay');
        this.mainContainer = document.getElementById('mainContainer');
        this.overlayUserName = document.getElementById('overlayUserName');

        this.init();
    }

    init() {
        // Get user name
        const userData = JSON.parse(localStorage.getItem('user') || '{}');
        const userName = userData.name || 'Friend';
        this.overlayUserName.textContent = userName;

        // Start Entrance Animation
        this.playEntranceAnimation();

        // Attach Event Listeners
        this.attachListeners();
    }

    playEntranceAnimation() {
        // Show overlay immediately
        this.overlay.classList.add('active');

        // After 2.5 seconds, transition to wizard
        setTimeout(() => {
            this.overlay.style.opacity = '0';
            this.overlay.style.pointerEvents = 'none';

            // Fade within main container
            this.mainContainer.style.opacity = '1';

            // Activate Step 1
            this.showStep(1);
        }, 2500);
    }

    attachListeners() {
        // Radio Options (Auto-advance)
        document.querySelectorAll('.radio-option').forEach(option => {
            option.addEventListener('click', (e) => {
                // Remove selected from siblings
                const group = option.closest('.radio-group');
                group.querySelectorAll('.radio-option').forEach(opt => opt.classList.remove('selected'));

                // Select clicked
                option.classList.add('selected');

                // Save data
                const question = group.dataset.question;
                const value = option.dataset.value;
                this.formData[question] = value;

                // Auto advance with delay
                setTimeout(() => {
                    this.nextStep();
                }, 400); // 400ms delay for visual feedback
            });
        });

        // Finish Button
        document.getElementById('finishBtn').addEventListener('click', () => {
            this.finish();
        });
    }

    showStep(stepNum) {
        // Reset classes
        this.steps.forEach(step => {
            step.classList.remove('active', 'exit-left', 'exit-right');
            if (parseInt(step.dataset.step) === stepNum) {
                step.classList.add('active');
            }
        });

        this.updateDots(stepNum);
        this.currentStep = stepNum;
    }

    nextStep() {
        if (this.currentStep >= this.totalSteps) return;

        const currentEl = document.querySelector(`.wizard-step[data-step="${this.currentStep}"]`);
        const nextEl = document.querySelector(`.wizard-step[data-step="${this.currentStep + 1}"]`);

        if (currentEl && nextEl) {
            // Animate Out Current
            currentEl.classList.remove('active');
            currentEl.classList.add('exit-left');

            // Animate In Next
            nextEl.classList.add('active');
            // Remove exit-left/right if it had it from before (back navigation?)
            // For now, we only go forward.

            this.currentStep++;
            this.updateDots(this.currentStep);
        }
    }

    skipStep() {
        // Just move next without saving (or save 'skipped')
        this.nextStep();
    }

    updateDots(stepNum) {
        // Hide dots on final step?
        if (stepNum === 5) {
            document.querySelector('.wizard-progress').style.display = 'none';
            return;
        }

        this.dots.forEach(dot => {
            const dotStep = parseInt(dot.dataset.step);
            dot.classList.toggle('active', dotStep === stepNum);
            // Optional: highlight previous dots as completed
            if (dotStep < stepNum) dot.style.opacity = '0.5';
        });
    }

    finish() {
        // Save to localStorage
        localStorage.setItem('learningPreferences', JSON.stringify(this.formData));

        // Redirect to Dashboard (Assuming dashboard.html exists)
        // Or index.html if user needs to login again?
        // script.js login saves token then redirects to dashboard.
        // If we just registered, we have token in localStorage?
        // script.js register flow saves token.

        window.location.href = 'dashboard.html';
    }
}

// Initialize
const wizard = new SurveyWizard();
