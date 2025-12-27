/**
 * SmartEducation - Scholar's Arena Dashboard Logic (Redesign)
 */

class DashboardManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.userData = JSON.parse(localStorage.getItem('user') || '{}');

        // Check Auth
        if (!this.token) {
            window.location.href = '/';
            return;
        }

        this.init();
    }

    async init() {
        // 1. Load HUD (Level, Streak, Focus Score)
        this.loadHUD();

        // 2. Load Mission Control (Hero Card)
        this.loadMissionControl();

        // 3. Load Daily Quests
        this.loadQuests();

        // 4. Load The Arena (Leaderboard)
        this.loadArena();

        // 5. Load Stats (Hours Banked)
        this.loadStats();

        // 6. Setup Real-time updates (Simulated)
        setInterval(() => this.updateTimeRemaining(), 60000);
    }

    // --- 1. HUD HEADER ---
    async loadHUD() {
        try {
            // Fetch Gamification Data
            const res = await fetch('/api/gamification/progress', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });

            if (res.ok) {
                const data = await res.json();

                // Update Name & XP
                document.getElementById('hudName').textContent = this.userData.name || 'Scholar';
                document.getElementById('hudXP').textContent = `${data.current_xp} XP`;
                document.getElementById('hudLevel').textContent = data.current_level;

                // Update Level Ring (Stroke Dashoffset trig)
                const circle = document.getElementById('levelRing');
                const radius = circle.r.baseVal.value;
                const circumference = radius * 2 * Math.PI;
                const percent = (data.current_xp / data.next_level_xp);
                const offset = circumference - (percent * circumference);

                circle.style.strokeDashoffset = offset;

                // Update Streak (Mocked or from API if avail)
                // Assuming data.streak exists or defaulting
                const streak = data.streak || 5;
                document.getElementById('hudStreak').textContent = `${streak} Days`;

                // Update Focus Score (Mocked logic based on consistency)
                const focusScore = Math.min(100, 50 + (data.current_level * 2));
                document.getElementById('hudFocusScore').textContent = `${focusScore}/100`;
            }
        } catch (e) {
            console.error('HUD Load Error', e);
        }
    }

    // --- 2. MISSION CONTROL (HERO CARD) ---
    async loadMissionControl() {
        try {
            // Reuse the Focus API
            const response = await fetch('/api/dashboard/focus', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const task = await response.json();

            const heroTitle = document.getElementById('heroTitle');
            const heroSubtitle = document.getElementById('heroSubtitle');
            const heroTime = document.getElementById('heroTimeRemaining');
            const heroProgress = document.getElementById('heroProgress');
            const heroProgressText = document.getElementById('heroProgressText');
            const heroBtnText = document.getElementById('heroBtnText');

            if (task.type !== 'empty') {
                heroTitle.textContent = task.title;
                heroSubtitle.textContent = task.subtitle || 'Focus Session';
                heroTime.textContent = `${task.duration} min left`;

                // Simulate progress based on time of day (Mock)
                const progress = 35;
                heroProgress.style.width = `${progress}%`;
                heroProgressText.textContent = `${progress}% Complete`;
                heroBtnText.textContent = 'Resume Learning';

                // Store ID for resume
                this.currentMissionId = task.id;
                this.currentMissionType = task.type;
            } else {
                heroTitle.textContent = "All Systems Clear";
                heroSubtitle.textContent = "You have completed your immediate goals.";
                heroProgress.parentElement.style.display = 'none';
                heroProgressText.style.display = 'none';
                heroBtnText.textContent = 'Explore Library';
                this.currentMissionId = null;
            }

        } catch (e) {
            console.error('Mission Control Error', e);
        }
    }

    resumeMission() {
        if (this.currentMissionId) {
            window.location.href = `/focus?id=${this.currentMissionId}&type=${this.currentMissionType}`;
        } else {
            window.location.href = '/bookmarks'; // Library
        }
    }

    updateTimeRemaining() {
        // Visual countdown logic could go here
    }

    // --- 3. DAILY QUESTS ---
    async loadQuests() {
        const container = document.getElementById('dailyQuests');
        const quests = [
            { id: 1, text: 'Study for 45 mins', xp: 50, completed: true },
            { id: 2, text: 'Review 10 Flashcards', xp: 30, completed: false },
            { id: 3, text: 'Complete "Arrays" Quiz', xp: 100, completed: false }
        ];

        container.innerHTML = quests.map(q => `
            <div class="quest-card ${q.completed ? 'completed' : ''}" onclick="window.dashboard.toggleQuest(${q.id})">
                <div class="quest-checkbox">
                    ${q.completed ? '<i class="fas fa-check" style="font-size:0.7rem; color:white;"></i>' : ''}
                </div>
                <div style="flex:1;">
                    <div class="quest-info">${q.text}</div>
                    <div class="quest-xp">+${q.xp} XP</div>
                </div>
            </div>
        `).join('');
    }

    toggleQuest(id) {
        // In a real app, this would hit an API
        // For visual feedback:
        // const card = event.currentTarget; // Need to pass event or find element
        // Reload for now or just mock toggle
        // console.log('Toggling quest', id);
    }

    // --- 4. THE ARENA (LEADERBOARD) ---
    async loadArena() {
        // 1. Leaderboard (Phase 28: Weekly Seasons)
        const container = document.getElementById('arenaLeaderboard');

        // Fetch real data to get 'weekly_xp'
        let myWeeklyXP = 0;
        try {
            // We can fetch this from the progress endpoint again or rely on cached data
            // For now, let's assume get_progress returns weekly_xp
            const res = await fetch('/api/gamification/progress', { headers: { 'Authorization': `Bearer ${this.token}` } });
            if (res.ok) {
                const d = await res.json();
                myWeeklyXP = d.weekly_xp || 0;
            }
        } catch (e) { }

        // Mock Competitors (Simulating Weekly Reset)
        const competitors = [
            { name: 'Sarah Chen', level: 12, xp: 450, avatar: 'SC' }, // Weekly XP
            { name: 'You', level: parseInt(document.getElementById('hudLevel').textContent) || 1, xp: myWeeklyXP, avatar: 'ME', isMe: true },
            { name: 'Mike Ross', level: 11, xp: 320, avatar: 'MR' },
            { name: 'Alex T.', level: 9, xp: 150, avatar: 'AT' }
        ].sort((a, b) => b.xp - a.xp);

        container.innerHTML = competitors.map((p, i) => `
            <div class="player-row ${p.isMe ? 'is-me' : ''}">
                <div class="rank top-${i + 1}">#${i + 1}</div>
                <div class="avatar-circle" style="${p.isMe ? 'background:var(--neon-blue);' : ''}">${p.avatar}</div>
                <div class="player-info">
                    <div class="player-name">${p.name} ${p.isMe ? '(You)' : ''}</div>
                    <div class="player-xp">${p.xp} XP <span style="font-size:0.7rem; opacity:0.6;">(This Week)</span></div>
                </div>
                ${!p.isMe ? `<button class="btn-nudge" title="Nudge ${p.name}">👋</button>` : ''}
            </div>
        `).join('');

        // 2. Active Recall
        try {
            const res = await fetch('/api/recall/due', { headers: { 'Authorization': `Bearer ${this.token}` } });
            if (res.ok) {
                const cards = await res.json();
                if (cards.length > 0) {
                    document.getElementById('arenaRecall').style.display = 'flex';
                    document.getElementById('recallCount').textContent = `${cards.length} Cards Due`;
                }
            }
        } catch (e) { console.error(e); }
    }

    // --- 5. STATS (HOURS BANKED) ---
    async loadStats() {
        const container = document.getElementById('hoursChart');
        if (!container) return;

        container.innerHTML = '<div style="color:rgba(255,255,255,0.3); font-size:0.8rem;">Loading stats...</div>';

        try {
            // Phase 29: Fetch Real Aggregated Daily Stats
            const res = await fetch('/api/gamification/stats/weekly', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });

            if (res.ok) {
                const data = await res.json(); // Array of { day, date, hours }

                // If no data, show empty placeholders (Mon-Sun)
                const displayData = data.length > 0 ? data : [
                    { day: 'Mon', hours: 0 }, { day: 'Tue', hours: 0 }, { day: 'Wed', hours: 0 },
                    { day: 'Thu', hours: 0 }, { day: 'Fri', hours: 0 }, { day: 'Sat', hours: 0 }, { day: 'Sun', hours: 0 }
                ];

                // Highlight today
                const todayShort = new Date().toLocaleDateString('en-US', { weekday: 'short' });

                container.innerHTML = displayData.map((d) => `
                    <div class="bar-group">
                        <div class="bar ${d.day === todayShort ? 'active' : ''}" 
                             style="height: ${Math.min(100, (d.hours / 4) * 100)}px;"
                             title="${d.hours} hrs">
                             <!-- Max height assumes ~4 hours target for full bar -->
                        </div>
                        <div class="bar-day">${d.day}</div>
                    </div>
                `).join('');

            } else {
                throw new Error('Failed to load stats');
            }
        } catch (e) {
            console.error('Stats Load Error', e);
            container.innerHTML = '<div style="color:rgba(255,100,100,0.5); font-size:0.8rem;">Stats unavailable</div>';
        }
    }
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new DashboardManager();
});
