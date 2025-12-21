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

        // 7. Setup Idle Detection
        this.setupIdleTimer();
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
            // If there's no H1, insert one at the top of main content
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

    formatTime(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' - ' + date.toLocaleDateString();
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

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new DashboardManager();
});
