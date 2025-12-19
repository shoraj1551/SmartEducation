/**
 * SmartEducation - Achievements Logic
 */

class AchievementManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.userData = JSON.parse(localStorage.getItem('user') || '{}');

        // UI Bindings
        this.badgeGrid = document.getElementById('badgeGrid');
        this.xpProgress = document.getElementById('xpProgress');
        this.currentXPText = document.getElementById('currentXP');
        this.nextLevelXPText = document.getElementById('nextLevelXP');
        this.levelBadge = document.getElementById('levelBadge');
        this.welcomeText = document.getElementById('welcomeText');

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = 'index.html';
            return;
        }

        this.renderUserProfile();
        await this.fetchAchievements();
    }

    renderUserProfile() {
        const xp = this.userData.xp_total || 0;
        const level = this.userData.level || 1;
        const name = this.userData.name ? this.userData.name.split(' ')[0] : 'Explorer';

        this.welcomeText.textContent = `Great progress, ${name}!`;
        this.levelBadge.textContent = `LEVEL ${level} ${this.getLevelTitle(level)}`;

        // XP Calculation
        const nextLevelXP = level * 1000;
        const progress = (xp / nextLevelXP) * 100;

        this.xpProgress.style.width = `${progress}%`;
        this.currentXPText.textContent = `${xp} XP`;
        this.nextLevelXPText.textContent = `${nextLevelXP} XP for Level ${level + 1}`;
    }

    getLevelTitle(level) {
        if (level < 5) return 'APPRENTICE';
        if (level < 10) return 'SCHOLAR';
        if (level < 20) return 'MASTER';
        return 'LEGEND';
    }

    async fetchAchievements() {
        // Mock achievements for now
        const allAchievements = [
            { code: 'first_bookmark', title: 'Knowledge Seeker', description: 'Saved your first educational resource.', icon: 'fa-bookmark', xp: 50 },
            { code: 'profile_complete', title: 'Verified Identity', description: 'Completed your 100% verified profile.', icon: 'fa-id-card', xp: 100 },
            { code: 'early_bird', title: 'Early Bird', description: 'Studied before 7 AM for 3 days.', icon: 'fa-sun', xp: 150 },
            { code: 'consistent', title: 'Momentum', description: 'Maintained a 5-day learning streak.', icon: 'fa-fire', xp: 200 },
            { code: 'polymath', title: 'Polymath', description: 'Saved resources in 3 different categories.', icon: 'fa-brain', xp: 250 },
            { code: 'night_owl', title: 'Night Owl', description: 'Active during peak midnight hours.', icon: 'fa-moon', xp: 150 }
        ];

        // Fetch user earned achievements
        try {
            const response = await fetch('/api/user/achievements', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const earnedResponse = await response.json();
            const earnedCodes = earnedResponse.map(a => a.achievement_code);

            this.renderBadges(allAchievements, earnedCodes);
        } catch (err) {
            console.warn('Backend achievements fetch failed, showing available badges only');
            this.renderBadges(allAchievements, []);
        }
    }

    renderBadges(all, earned) {
        this.badgeGrid.innerHTML = all.map(badge => {
            const isUnlocked = earned.includes(badge.code);
            return `
                <div class="badge-card ${isUnlocked ? 'unlocked' : ''}">
                    <div class="lock-overlay">
                        <i class="fas ${isUnlocked ? 'fa-check-circle' : 'fa-lock'}"></i>
                    </div>
                    <div class="badge-icon">
                        <i class="fas ${badge.icon}"></i>
                    </div>
                    <h3>${badge.title}</h3>
                    <p>${badge.description}</p>
                    <div style="margin-top: 1rem; font-weight: 700; color: var(--primary); font-size: 0.8rem;">
                        +${badge.xp} XP
                    </div>
                </div>
            `;
        }).join('');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new AchievementManager();
});
