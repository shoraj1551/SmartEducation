/**
 * SmartEducation - Dashboard Logic
 */

class DashboardManager {
    constructor() {
        this.userData = JSON.parse(localStorage.getItem('user') || '{}');
        this.token = localStorage.getItem('token');

        // Element Bindings
        this.userMenuTrigger = document.getElementById('userMenuTrigger');
        this.userDropdown = document.getElementById('userDropdown');
        this.userNameBrief = document.getElementById('userNameBrief');
        this.avatarInitials = document.getElementById('avatarInitials');
        this.activityFeed = document.getElementById('activityFeed');

        // Bookmark Bindings
        this.bookmarkModal = document.getElementById('bookmarkModal');
        this.addBookmarkForm = document.getElementById('addBookmarkForm');
        this.bookmarkList = document.getElementById('bookmarkList');
        this.bookmarkPagination = document.getElementById('bookmarkPagination');

        // Modal Bindings
        this.resumeModal = document.getElementById('resumeModal');
        this.startFreshBtn = document.getElementById('startFreshBtn');
        this.resumeSessionBtn = document.getElementById('resumeSessionBtn');

        // Session State
        this.idleTimeout = null;
        this.IDLE_LIMIT = 60 * 60 * 1000; // 60 minutes
        this.lastAction = Date.now();

        this.init();

        // Expose helpers for HTML onclicks
        window.toggleNotifications = this.toggleNotifications.bind(this);
        window.markNotifRead = this.markNotifRead.bind(this);
    }

    async init() {
        if (!this.token) {
            window.location.href = '/';
            return;
        }

        // 1. Set User Profile Info
        this.updateProfileUI();

        // 2. Check for Session Resumption
        await this.checkSessionStatus();

        // 3. Fetch Recent Activities
        await this.fetchActivities();

        // 4. Fetch Bookmarks
        await this.fetchBookmarks();

        // 5. Fetch Full Profile for AI Personalization
        await this.fetchFullProfile();

        // 6. Attach Listeners
        this.attachListeners();

        // 7. Load Focus Task (Feature 2 & 4)
        this.loadFocusTask();

        // 8. Load Reality Metrics (Feature 6)
        this.loadRealityMetrics();

        // 9. Load Wellness Status (Feature 8)
        this.loadWellnessStatus();

        // 10. Load Gamification (Feature 9)
        this.loadGamification();

        // 11. Setup Idle Detection
        this.setupIdleTimer();

        // 12. Load Notifications (Feature 11)
        this.loadNotifications();
    }

    async loadFocusTask() {
        try {
            const container = document.getElementById('focusTaskContainer');
            if (!container) return; // Only if element exists

            container.innerHTML = '<div class="loading-spinner"><i class="fas fa-circle-notch fa-spin"></i> Finding your focus...</div>';

            const response = await fetch('/api/dashboard/focus', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const task = await response.json();

            if (!response.ok) throw new Error(task.error);

            if (task.type === 'empty') {
                container.innerHTML = `
                    <div class="focus-empty-state">
                        <i class="fas fa-check-circle" style="font-size: 2rem; color: #10b981; margin-bottom: 10px;"></i>
                        <h3>All Caught Up!</h3>
                        <p>Relax or explore the library.</p>
                        <a href="/bookmarks" class="btn btn-primary">Browse Library</a>
                    </div>
                `;
            } else {
                container.innerHTML = `
                    <div class="focus-card ${task.reason === 'Catch Up (High Priority)' ? 'urgent' : ''}">
                        <div class="focus-header">
                            <span class="focus-badge"><i class="fas fa-bullseye"></i> ${task.reason}</span>
                            <span class="focus-duration"><i class="far fa-clock"></i> ${task.duration}m</span>
                        </div>
                        <h2 class="focus-title">${task.title}</h2>
                        <p class="focus-subtitle">${task.subtitle}</p>
                        
                        <div class="focus-actions">
                            <button class="btn btn-primary btn-lg" onclick="window.location.href='/focus?id=${task.id}&type=${task.type}'">
                                <i class="fas fa-play"></i> Start Focusing
                            </button>
                            ${task.type === 'daily_task' ? `<button class="btn btn-secondary" onclick="skipTask('${task.id}')">Skip</button>` : ''}
                        </div>
                    </div>
                `;
            }
        } catch (err) {
            console.error('Focus load error:', err);
            const container = document.getElementById('focusTaskContainer');
            if (container) container.innerHTML = '<div class="error-state">Could not load focus task.</div>';
        }
    }

    async loadRealityMetrics() {
        try {
            const container = document.getElementById('realityContainer');
            if (!container) return;

            const response = await fetch('/api/reality/metrics', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });

            if (!response.ok) return;

            const data = await response.json();

            // Only show if there's significant data (e.g. at least some history or active commitments)
            // Or always show to establish the habit. Let's always show if enabled.
            container.style.display = 'block';

            let html = '';

            // 1. Days Wasted Card
            if (data.days_wasted > 0) {
                html += `
                    <div class="reality-card danger">
                        <div class="reality-icon"><i class="fas fa-exclamation-triangle"></i></div>
                        <div class="reality-info">
                            <h3>The Harsh Truth</h3>
                            <p>You have wasted <strong>${data.days_wasted} days</strong> in the last 30 days.</p>
                            <div class="velocity-stat">
                                <span>Actual Velocity: ${data.actual_velocity} min/day</span>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                html += `
                    <div class="reality-card success">
                        <div class="reality-icon"><i class="fas fa-check-double"></i></div>
                        <div class="reality-info">
                            <h3>Total Discipline</h3>
                            <p>Zero days wasted recently. You are a machine.</p>
                            <div class="velocity-stat">
                                <span>Velocity: ${data.actual_velocity} min/day</span>
                            </div>
                        </div>
                    </div>
                `;
            }

            // 2. Projections (If any are delayed)
            if (data.projections && data.projections.length > 0) {
                const delayed = data.projections.filter(p => p.gap_days > 0);
                if (delayed.length > 0) {
                    html += `<div class="reality-gap-list">`;
                    delayed.forEach(p => {
                        html += `
                            <div class="gap-item">
                                <span class="gap-title">${p.title}</span>
                                <span class="gap-warning">+${p.gap_days} DAYS LATE</span>
                            </div>
                        `;
                    });
                    html += `</div>`;
                }
            }

            container.innerHTML = html;

        } catch (err) {
            console.error('Reality load error:', err);
        }
    }

    async loadWellnessStatus() {
        try {
            // 1. Check Burnout
            const burnoutRes = await fetch('/api/wellness/burnout', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            if (burnoutRes.ok) {
                const bData = await burnoutRes.json();
                const bContainer = document.getElementById('burnoutContainer');
                if (bData.level === 'high' || bData.level === 'moderate') {
                    bContainer.style.display = 'block';
                    bContainer.innerHTML = `
                        <div class="burnout-alert ${bData.level}">
                            <i class="fas fa-biohazard"></i>
                            <div class="alert-content">
                                <strong>${bData.message}</strong>
                                <span>High intensity streak: ${bData.details.high_intensity_streak} days. Rest is productive.</span>
                            </div>
                        </div>
                     `;
                }
            }

            // 2. Check Weekly Review
            // Only fetch if it's Sunday or Monday? For now, always fetch to see if we have data.
            const reviewRes = await fetch('/api/wellness/review', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            if (reviewRes.ok) {
                const rData = await reviewRes.json();
                // If we have substantial data (e.g. > 1 task or hour), offer review
                if (rData.tasks_completed > 0 || rData.total_hours > 0) {
                    this.renderReviewTrigger(rData);
                }
            }
        } catch (err) {
            console.error('Wellness check failed', err);
        }
    }

    renderReviewTrigger(data) {
        // We'll append a "Review Card" to the Reality Container for high visibility
        const container = document.getElementById('realityContainer');
        if (container) {
            container.style.display = 'block'; // Ensure visible
            // Create a wrapper if needed or just append
            const div = document.createElement('div');
            div.className = 'reality-card review-card';
            div.innerHTML = `
                <div class="reality-icon" style="background: rgba(139, 92, 246, 0.2); color: #a78bfa;">
                    <i class="fas fa-chart-pie"></i>
                </div>
                <div class="reality-info">
                    <h3>Weekly Report Ready</h3>
                    <p>${data.total_hours} hours logged. Most productive on ${data.most_productive_day}.</p>
                </div>
                <button class="btn btn-sm btn-primary" onclick="openReviewModal()">View</button>
            `;
            container.appendChild(div);

            // Store data for modal
            window.weeklyReviewData = data;
        }
    }

    async loadGamification() {
        try {
            const res = await fetch('/api/gamification/progress', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            if (res.ok) {
                const data = await res.json();
                const container = document.getElementById('gamificationContainer');

                if (container) {
                    container.style.display = 'flex';
                    container.innerHTML = `
                        <div class="level-pill" title="${data.current_level_xp}/${data.next_level_xp_target} XP to next level">
                            <span class="lvl-num">LVL ${data.level}</span>
                            <span class="lvl-title">${data.title}</span>
                            <div class="xp-bar-mini">
                                <div class="xp-fill" style="width: ${data.percent}%"></div>
                            </div>
                        </div>
                     `;
                }
            }
        } catch (e) {
            console.error(e);
        }
    }

    toggleNotifications() {
        const d = document.getElementById('notifDropdown');
        if (d) d.style.display = d.style.display === 'none' ? 'block' : 'none';
    }

    async markNotifRead(id, link) {
        // Optimistic remove
        try {
            await fetch(`/api/notifications/${id}/read`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });
            // Reload to update badge
            window.location.reload();
            if (link && link !== 'null') window.location.href = link;
        } catch (e) { console.error(e); }
    }

    // --- NOTIFICATIONS ---
    async loadNotifications() {
        try {
            const res = await fetch('/api/notifications', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            if (res.ok) {
                const list = await res.json();
                this.renderNotifications(list);
            }
        } catch (e) { console.error(e); }
    }

    renderNotifications(list) {
        const badge = document.getElementById('notifBadge');
        const container = document.getElementById('notifList');

        if (list.length > 0) {
            badge.style.display = 'block';
            badge.innerText = list.length;

            container.innerHTML = list.map(n => `
                <div class="notif-item ${!n.is_read ? 'unread' : ''}" onclick="markNotifRead('${n.id}', '${n.action_link || ''}')">
                    <span class="notif-title">${n.title}</span>
                    <span class="notif-body">${n.message}</span>
                </div>
            `).join('');
        } else {
            badge.style.display = 'none';
            container.innerHTML = '<div class="empty-notif">No new notifications</div>';
        }
    }

    async fetchFullProfile() {
        try {
            const response = await fetch('/api/user/profile', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const user = await response.json();
            if (response.ok) {
                this.userData = user;
                localStorage.setItem('user', JSON.stringify(user));
                this.updatePersonalizedGreeting();
                this.renderRecommendations();
                this.updateCommitmentTracker();
                this.updateStats();
            }
        } catch (err) {
            console.error('Error fetching full profile:', err);
        }
    }

    updatePersonalizedGreeting() {
        const name = this.userData.name.split(' ')[0];
        const goal = this.userData.learning_goal || 'learning';
        const greetingEl = document.querySelector('.main-content h1');

        // Map goals to friendly phrases
        const goalPhrases = {
            'school': 'crushing your school boards',
            'competitive': 'conquering your competitive exams',
            'college': 'excelling in your university studies',
            'upskill': 'mastering new professional skills',
            'switch': 'on your path to a new career',
            'academic': 'striving for general excellence',
            'hobby': 'exploring your passions'
        };

        const phrase = goalPhrases[goal] || 'glad to have you back';

        if (greetingEl) {
            greetingEl.innerHTML = `Welcome back, ${name}! <span style="font-size: 1rem; color: rgba(255,255,255,0.4); display: block; margin-top: 0.5rem; font-weight: 400;">You're ${phrase}.</span>`;
        } else {
            // If there's no H1, insert one at
            const topNav = document.querySelector('.top-nav');
            const h1 = document.createElement('h1');
            h1.style.marginBottom = '2rem';
            h1.innerHTML = `Welcome back, ${name}! <span style="font-size: 1rem; color: rgba(255,255,255,0.4); display: block; margin-top: 0.5rem; font-weight: 400;">You're ${phrase}.</span>`;
            topNav.parentNode.insertBefore(h1, topNav.nextSibling);
        }
    }

    updateProfileUI() {
        const name = this.userData.name || 'User';
        this.userNameBrief.textContent = name;
        this.avatarInitials.textContent = name.charAt(0).toUpperCase();
    }

    renderRecommendations() {
        const area = document.getElementById('recommendationArea');
        const grid = document.getElementById('recommendationGrid');
        const pathLabel = document.getElementById('interestPathLabel');

        const interests = this.userData.interests || [];
        const primaryInterest = interests.length > 0 ? interests[0] : 'Learning';

        if (pathLabel) pathLabel.textContent = primaryInterest;
        if (area) area.style.display = 'block';

        // Mock recommendations based on interests
        const mocks = {
            'government': [
                { title: 'SSC CGL Complete Guide', type: 'Course', icon: '🏛️', url: '#' },
                { title: 'Banking Awareness 2024', type: 'Article', icon: '🏦', url: '#' },
                { title: 'UPSC Current Affairs Daily', type: 'Video', icon: '📰', url: '#' }
            ],
            'entrance': [
                { title: 'JEE Advanced Maths Mastery', type: 'Course', icon: '📐', url: '#' },
                { title: 'NEET Biology Rapid Revision', type: 'Article', icon: '🩺', url: '#' },
                { title: 'GATE CS Theory of Computation', type: 'Video', icon: '🖥️', url: '#' }
            ],
            'school_subjects': [
                { title: 'Class 12 Physics: Optics', type: 'Course', icon: '🔭', url: '#' },
                { title: 'Calculus for Beginners', type: 'Article', icon: '🔢', url: '#' },
                { title: 'Tenth Grade History Simplified', type: 'Video', icon: '📜', url: '#' }
            ],
            'tech': [
                { title: 'Full-Stack Roadmap 2024', type: 'Course', icon: '💻', url: '#' },
                { title: 'System Design Fundamentals', type: 'Article', icon: '🏗️', url: '#' },
                { title: 'Advanced React Patterns', type: 'Video', icon: '⚛️', url: '#' }
            ],
            'design': [
                { title: 'UI/UX Design Masterclass', type: 'Course', icon: '🎨', url: '#' },
                { title: 'Typography in Modern Apps', type: 'Article', icon: '✍️', url: '#' },
                { title: 'Figma to Code Workflow', type: 'Video', icon: '🛠️', url: '#' }
            ],
            'business': [
                { title: 'Product Management 101', type: 'Course', icon: '📈', url: '#' },
                { title: 'Agile Methodology Guide', type: 'Article', icon: '🤝', url: '#' },
                { title: 'Market Analysis Techniques', type: 'Video', icon: '📊', url: '#' }
            ]
        };

        const recs = mocks[primaryInterest.toLowerCase()] || mocks['tech'];

        if (grid) {
            grid.innerHTML = recs.map(rec => `
                <div class="stat-card" style="cursor: pointer; transition: transform 0.3s ease;" onclick="window.open('${rec.url}', '_blank')">
                    <div class="stat-icon purple" style="background: rgba(124, 58, 237, 0.1); font-size: 1.2rem;">${rec.icon}</div>
                    <div class="stat-info">
                        <h4 style="font-size: 0.7rem;">${rec.type}</h4>
                        <p style="font-size: 0.95rem; line-height: 1.2;">${rec.title}</p>
                    </div>
                </div>
            `).join('');
        }
    }

    updateCommitmentTracker() {
        const level = this.userData.commitment_level || 'moderate';
        const bar = document.getElementById('commitmentBar');
        const label = document.getElementById('commitmentLabel');

        const goals = { 'light': 2, 'moderate': 5, 'intensive': 10 };
        const goalHours = goals[level] || 5;

        // Mocking hours spent for now (will connect to session data later)
        const spent = 1.2;
        const percentage = Math.min((spent / goalHours) * 100, 100);

        if (bar) bar.style.width = `${percentage}%`;
        if (label) {
            const levelUpper = level.charAt(0).toUpperCase() + level.slice(1);
            label.textContent = `${levelUpper} (${spent}/${goalHours}h)`;
        }
    }

    updateStats() {
        const hoursEl = document.getElementById('hoursSpent');
        if (hoursEl) hoursEl.textContent = '1.2'; // Mock

        const rateEl = document.getElementById('completionRate');
        if (rateEl) rateEl.textContent = '15%'; // Mock
    }

    attachListeners() {
        // Dropdown Toggle and Logout are handled by common.js to prevent conflicts

        // Modal Actions
        this.startFreshBtn.addEventListener('click', () => this.closeModal());
        this.resumeSessionBtn.addEventListener('click', () => {
            this.closeModal();
            this.logActivity('course_resume', 'User resumed their last course session');
        });

        // Bookmark Form
        if (this.addBookmarkForm) {
            this.addBookmarkForm.addEventListener('submit', (e) => this.handleAddBookmark(e));
        }

        // Idle Reset Listeners
        ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(evt => {
            document.addEventListener(evt, () => this.resetIdleTimer());
        });
    }

    async handleAddBookmark(e) {
        e.preventDefault();
        const url = document.getElementById('bmUrl').value;
        const title = document.getElementById('bmTitle').value;
        const description = document.getElementById('bmDesc').value;

        const btn = this.addBookmarkForm.querySelector('button');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Identifying...';
        btn.disabled = true;

        try {
            const response = await fetch('/api/bookmarks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ url, title, description })
            });

            if (response.ok) {
                this.addBookmarkForm.reset();
                this.closeBookmarkModal();
                await this.fetchBookmarks();
                this.logActivity('add_bookmark', `Added resource: ${title || url}`);
            } else {
                const data = await response.json();
                alert(data.error || 'Failed to add bookmark');
            }
        } catch (err) {
            console.error('Error adding bookmark:', err);
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }

    async fetchBookmarks(page = 1) {
        try {
            const response = await fetch(`/api/bookmarks?page=${page}&per_page=20`, {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();
            this.renderBookmarks(data.bookmarks);
            this.renderPagination(data.total, data.page, data.per_page);
        } catch (err) {
            console.error('Error fetching bookmarks:', err);
            this.bookmarkList.innerHTML = '<p style="color: rgba(255,255,255,0.3);">Failed to load bookmarks.</p>';
        }
    }

    renderBookmarks(bookmarks) {
        if (!bookmarks || bookmarks.length === 0) {
            this.bookmarkList.innerHTML = `
                <div class="activity-item" style="text-align: center; justify-content: center; padding: 4rem 2rem;">
                    <div style="opacity: 0.3;">
                        <i class="fas fa-bookmark" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                        <p>No bookmarks yet. Start building your library!</p>
                    </div>
                </div>`;
            return;
        }

        this.bookmarkList.innerHTML = bookmarks.map(bm => `
            <div class="activity-item">
                <div style="width: 50px; height: 50px; background: rgba(255,255,255,0.05); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">
                    ${this.getCategoryIcon(bm.category)}
                </div>
                <div class="activity-content" style="flex: 1;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <h5 style="margin-bottom: 0.25rem;">${bm.title}</h5>
                        <span style="font-size: 0.75rem; background: rgba(124, 58, 237, 0.2); color: var(--primary); padding: 2px 8px; border-radius: 20px;">
                            Score: ${Math.round(bm.relevance_score * 100)}%
                        </span>
                    </div>
                    <p style="margin-bottom: 0.5rem; font-size: 0.85rem;">${bm.description || 'No description'}</p>
                    <div style="display: flex; gap: 1rem; align-items: center;">
                        <a href="${bm.url}" target="_blank" class="text-btn" style="font-size: 0.8rem; text-decoration: none;">
                            <i class="fas fa-external-link-alt"></i> Visit Resource
                        </a>
                        <span class="activity-time" style="margin: 0;">${bm.category.toUpperCase()}</span>
                    </div>
                </div>
            </div>
        `).join('');
    }

    renderPagination(total, currentPage, perPage) {
        const pages = Math.ceil(total / perPage);
        if (pages <= 1) {
            this.bookmarkPagination.innerHTML = '';
            return;
        }

        let html = '';
        for (let i = 1; i <= pages; i++) {
            html += `<button class="nav-btn ${i === currentPage ? 'primary-btn' : 'secondary-btn'}" 
                             style="padding: 0.4rem 0.8rem; font-size: 0.8rem; min-width: 35px;" 
                             onclick="window.dashboard.fetchBookmarks(${i})">${i}</button>`;
        }
        this.bookmarkPagination.innerHTML = html;
    }

    getCategoryIcon(cat) {
        switch (cat) {
            case 'video': return '📽️';
            case 'course': return '🎓';
            case 'article/docs': return '📄';
            default: return '🔗';
        }
    }

    async logActivity(type, description = '', metadata = null) {
        try {
            const response = await fetch('/api/user/log-activity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ type, description, metadata })
            });
            if (response.ok) {
                await this.fetchActivities();
            }
        } catch (err) {
            console.error('Error logging activity:', err);
        }
    }

    async checkSessionStatus() {
        // FEEDBACK FIX: Only check once per browser session
        if (sessionStorage.getItem('checked_resumption')) return;

        try {
            const response = await fetch('/api/user/session-status', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();
            if (data.has_previous_session) {
                setTimeout(() => {
                    this.resumeModal.style.display = 'flex';
                    sessionStorage.setItem('checked_resumption', 'true');
                }, 800);
            }
        } catch (err) {
            console.error('Error checking session status:', err);
        }
    }

    setupIdleTimer() {
        if (this.idleTimeout) clearTimeout(this.idleTimeout);
        this.idleTimeout = setTimeout(() => {
            // Re-trigger session prompt after 60 mins of inactivity
            sessionStorage.removeItem('checked_resumption');
            this.checkSessionStatus();
        }, this.IDLE_LIMIT);
    }

    resetIdleTimer() {
        this.lastAction = Date.now();
        this.setupIdleTimer();
    }

    async fetchActivities() {
        try {
            const response = await fetch('/api/user/activities?limit=5', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const activities = await response.json();
            this.renderActivities(activities);
        } catch (err) {
            console.error('Error fetching activities:', err);
            this.activityFeed.innerHTML = '<p style="color: rgba(255,255,255,0.3);">Failed to load activity feed.</p>';
        }
    }

    renderActivities(activities) {
        if (!activities || activities.length === 0) {
            this.activityFeed.innerHTML = '<p style="color: rgba(255,255,255,0.3);">No recent activities found.</p>';
            return;
        }

        this.activityFeed.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="activity-marker">
                    <div class="activity-dot"></div>
                    <div class="activity-line"></div>
                </div>
                <div class="activity-content">
                    <h5>${this.formatActivityTitle(activity.activity_type)}</h5>
                    <p>${activity.description || 'Activity recorded'}</p>
                    <div class="activity-time">${this.formatTime(activity.created_at)}</div>
                </div>
            </div>
        `).join('');
    }

    formatActivityTitle(type) {
        return type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    }

    closeModal() {
        this.resumeModal.style.opacity = '0';
        setTimeout(() => {
            this.resumeModal.style.display = 'none';
            this.resumeModal.style.opacity = '1';
        }, 300);
    }

    closeBookmarkModal() {
        this.bookmarkModal.style.display = 'none';
    }

    handleLogout() {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        window.location.href = '/';
    }
}

// Global Modal Toggles
function openBookmarkModal() { window.dashboard.bookmarkModal.style.display = 'flex'; }
function closeBookmarkModal() { window.dashboard.closeBookmarkModal(); }

// --- SEARCH ENGINE (Feature 15) ---
function getGreeting() {
    const hr = new Date().getHours();
    if (hr < 12) return 'Good morning';
    if (hr < 18) return 'Good afternoon';
    return 'Good evening';
}

document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        toggleSearch();
    }
    if (e.key === 'Escape') {
        const m = document.getElementById('searchModal');
        if (m) {
            m.style.display = 'none';
            document.getElementById('searchInput').value = '';
        }
    }
});

function toggleSearch() {
    const modal = document.getElementById('searchModal');
    const input = document.getElementById('searchInput');
    if (!modal) return;

    if (modal.style.display === 'none') {
        modal.style.display = 'flex';
        input.focus();
    } else {
        modal.style.display = 'none';
        input.value = '';
    }
}

let searchDebounce;
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchDebounce);
        const query = e.target.value.trim();

        if (!query) {
            document.getElementById('searchResults').innerHTML = '<div class="search-placeholder">Type to search...</div>';
            return;
        }

        searchDebounce = setTimeout(() => performSearch(query), 300);
    });
}

async function performSearch(query) {
    try {
        const token = localStorage.getItem('token');
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            const data = await res.json();
            renderSearchResults(data);
        }
    } catch (e) { console.error(e); }
}

function renderSearchResults(data) {
    const container = document.getElementById('searchResults');
    let html = '';

    if (data.tasks.length === 0 && data.library.length === 0 && data.flashcards.length === 0) {
        container.innerHTML = '<div class="search-placeholder">No results found.</div>';
        return;
    }

    // Helper to render sections
    const renderSection = (title, items) => {
        if (items.length === 0) return '';
        return `<div class="search-group-title">${title}</div>` + items.map(i => renderResultItem(i)).join('');
    };

    html += renderSection('Tasks', data.tasks);
    html += renderSection('Library', data.library);
    html += renderSection('Flashcards', data.flashcards);

    container.innerHTML = html;
}

function renderResultItem(item) {
    return `
        <div class="result-item" onclick="window.location.href='${item.link}'">
            <div class="result-icon"><i class="fas ${item.icon}"></i></div>
            <div class="result-content">
                <span class="result-title">${item.title}</span>
                <span class="result-sub">${item.subtitle}</span>
            </div>
            <i class="fas fa-arrow-right" style="opacity:0.3; font-size:0.8rem;"></i>
        </div>
    `;
}

// Close search if clicking outside box
const searchModal = document.getElementById('searchModal');
if (searchModal) {
    searchModal.addEventListener('click', (e) => {
        if (e.target.id === 'searchModal') toggleSearch();
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new DashboardManager();
});
