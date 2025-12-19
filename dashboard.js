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

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = 'index.html';
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

        // 5. Attach Listeners
        this.attachListeners();
    }

    updateProfileUI() {
        const name = this.userData.name || 'User';
        this.userNameBrief.textContent = name;
        this.avatarInitials.textContent = name.charAt(0).toUpperCase();
    }

    attachListeners() {
        // Dropdown Toggle
        this.userMenuTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            this.userDropdown.classList.toggle('active');
        });

        // Close dropdown on outside click
        document.addEventListener('click', () => {
            this.userDropdown.classList.remove('active');
        });

        // Logout
        const logoutActions = ['sidebarLogout', 'dropdownLogout'];
        logoutActions.forEach(id => {
            document.getElementById(id)?.addEventListener('click', () => this.handleLogout());
        });

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
        try {
            const response = await fetch('/api/user/session-status', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();
            if (data.has_previous_session) {
                setTimeout(() => {
                    this.resumeModal.style.display = 'flex';
                }, 800);
            }
        } catch (err) {
            console.error('Error checking session status:', err);
        }
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
        window.location.href = 'index.html';
    }
}

// Global Modal Toggles
function openBookmarkModal() { window.dashboard.bookmarkModal.style.display = 'flex'; }
function closeBookmarkModal() { window.dashboard.closeBookmarkModal(); }

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new DashboardManager();
});
