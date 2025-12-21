
/**
 * SmartEducation Flashcard Logic
 * Handles SRS Review queues and interactions.
 */

class FlashcardManager {
    constructor() {
        this.queue = [];
        this.currentCard = null;
        this.token = localStorage.getItem('token');

        if (!this.token) {
            window.location.href = '/login';
            return;
        }

        this.init();
    }

    async init() {
        await this.fetchQueue();
    }

    async fetchQueue() {
        try {
            const res = await fetch('/api/recall/due', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            if (res.ok) {
                this.queue = await res.json();
                this.updateQueueCount();
                this.loadNextCard();
            } else {
                document.getElementById('cardStage').innerHTML = `<p class="error">Failed to load cards.</p>`;
            }
        } catch (e) {
            console.error(e);
        }
    }

    updateQueueCount() {
        const el = document.getElementById('queueCount');
        if (el) el.innerText = `${this.queue.length} cards due`;
    }

    loadNextCard() {
        if (this.queue.length === 0) {
            this.renderEmptyState();
            return;
        }

        this.currentCard = this.queue[0]; // Peek
        this.renderCard(this.currentCard);
    }

    renderCard(card) {
        const stage = document.getElementById('cardStage');
        const controls = document.getElementById('controlsArea');

        // Render Front
        stage.innerHTML = `
            <div class="flashcard">
                <div class="card-front">
                    <div class="card-label">Question</div>
                    <div class="card-text">${this.formatText(card.front)}</div>
                </div>
                <div class="card-back" id="cardBack">
                    <!-- HIDDEN -->
                </div>
            </div>
        `;

        // Render Reveal Button
        controls.innerHTML = `
            <button class="btn-reveal" onclick="cardManager.reveal()">
                Show Answer <i class="fas fa-eye"></i>
            </button>
        `;
    }

    reveal() {
        const back = document.getElementById('cardBack');
        if (!back) return;

        // Show Back
        back.style.display = 'block';
        back.innerHTML = `
            <div class="card-label">Answer</div>
            <div class="card-text back-text">${this.formatText(this.currentCard.back)}</div>
        `;

        // Change Controls to Rating
        const controls = document.getElementById('controlsArea');
        controls.innerHTML = `
            <div class="rating-grid">
                <button class="btn-rate rate-again" onclick="cardManager.submitReview(1)">
                    <small>Again</small><br>< 1m
                </button>
                <button class="btn-rate rate-hard" onclick="cardManager.submitReview(2)">
                    <small>Hard</small><br>2d
                </button>
                <button class="btn-rate rate-good" onclick="cardManager.submitReview(4)">
                    <small>Good</small><br>4d
                </button>
                <button class="btn-rate rate-easy" onclick="cardManager.submitReview(5)">
                    <small>Easy</small><br>7d
                </button>
            </div>
        `;
    }

    async submitReview(quality) {
        if (!this.currentCard) return;

        // Optimistic UI update
        this.queue.shift(); // Remove current
        this.updateQueueCount();

        const cardId = this.currentCard.id;

        // Load next immediately
        this.loadNextCard();

        // Send API request in background
        try {
            await fetch('/api/recall/review', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    card_id: cardId,
                    quality: quality
                })
            });
            // Could handle error here if needed, but for SRS flow, speed is key.
        } catch (e) {
            console.error(e);
        }
    }

    renderEmptyState() {
        const stage = document.getElementById('cardStage');
        stage.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon"><i class="fas fa-check-circle"></i></div>
                <h2>All Caught Up!</h2>
                <p>You have reviewed all your cards for today.</p>
                <a href="/dashboard" class="btn btn-primary" style="margin-top:1rem;">Back to Dashboard</a>
            </div>
        `;
        document.getElementById('controlsArea').innerHTML = ''; // Clear controls
    }

    // Formatting Helper to handle newlines
    formatText(text) {
        if (!text) return '';
        return text.replace(/\n/g, '<br>');
    }
}

// Init
const cardManager = new FlashcardManager();
