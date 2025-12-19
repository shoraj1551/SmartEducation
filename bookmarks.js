/**
 * SmartEducation - Bookmarks Logic
 */

class BookmarkManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.bookmarks = [];
        this.filteredBookmarks = [];

        // Bindings
        this.grid = document.getElementById('bookmarkGrid');
        this.emptyState = document.getElementById('emptyState');
        this.searchInput = document.getElementById('bmSearch');
        this.filterSelect = document.getElementById('bmFilter');
        this.addModal = document.getElementById('addBMModal');
        this.addForm = document.getElementById('addBMForm');

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = 'index.html';
            return;
        }

        await this.fetchBookmarks();
        this.attachListeners();
    }

    async fetchBookmarks() {
        try {
            const response = await fetch('/api/bookmarks?per_page=100', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();

            if (response.ok) {
                this.bookmarks = data.bookmarks || [];
                this.filteredBookmarks = [...this.bookmarks];
                this.render();
            }
        } catch (err) {
            console.error('Error fetching bookmarks:', err);
        }
    }

    attachListeners() {
        // Search
        this.searchInput.addEventListener('input', () => this.handleFilter());

        // Category Filter
        this.filterSelect.addEventListener('change', () => this.handleFilter());

        // Add Bookmark
        this.addForm.addEventListener('submit', (e) => this.handleAdd(e));
    }

    handleFilter() {
        const query = this.searchInput.value.toLowerCase();
        const category = this.filterSelect.value;

        this.filteredBookmarks = this.bookmarks.filter(bm => {
            const matchesSearch =
                bm.title.toLowerCase().includes(query) ||
                bm.description.toLowerCase().includes(query) ||
                (bm.tags && bm.tags.toLowerCase().includes(query));

            const matchesCategory = category === 'all' || bm.category === category;

            return matchesSearch && matchesCategory;
        });

        this.render();
    }

    async handleAdd(e) {
        e.preventDefault();
        const url = document.getElementById('newBMUrl').value;
        const title = document.getElementById('newBMTitle').value;
        const description = document.getElementById('newBMDesc').value;

        const btn = this.addForm.querySelector('button');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
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
                this.addForm.reset();
                this.closeAddModal();
                await this.fetchBookmarks();
                // Potential Achievement Trigger: First Bookmark
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

    async deleteBookmark(id) {
        if (!confirm('Are you sure you want to remove this resource?')) return;

        try {
            const response = await fetch(`/api/bookmarks/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${this.token}` }
            });

            if (response.ok) {
                this.bookmarks = this.bookmarks.filter(bm => bm.id !== id);
                this.handleFilter();
            }
        } catch (err) {
            console.error('Error deleting bookmark:', err);
        }
    }

    render() {
        if (this.filteredBookmarks.length === 0) {
            this.grid.style.display = 'none';
            this.emptyState.style.display = 'block';
            return;
        }

        this.grid.style.display = 'grid';
        this.emptyState.style.display = 'none';

        this.grid.innerHTML = this.filteredBookmarks.map(bm => `
            <div class="bookmark-card">
                <div class="card-header">
                    <span class="category-badge">${bm.category || 'General'}</span>
                    <div class="relevance-score">
                        <i class="fas fa-bolt"></i>
                        ${Math.round(bm.relevance_score * 100)}% Match
                    </div>
                </div>
                <div class="card-body">
                    <h3>${bm.title || 'Untitled Resource'}</h3>
                    <p>${bm.description || 'No description available for this curated item.'}</p>
                </div>
                <div class="card-footer">
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.2);">
                        ${this.formatDate(bm.created_at)}
                    </div>
                    <div class="card-actions">
                        <a href="${bm.url}" target="_blank" class="action-btn" title="Open Link">
                            <i class="fas fa-external-link-alt"></i>
                        </a>
                        <button class="action-btn delete-btn" onclick="window.manager.deleteBookmark('${bm.id}')" title="Delete">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString();
    }

    openAddModal() { this.addModal.style.display = 'flex'; }
    closeAddModal() { this.addModal.style.display = 'none'; }
}

// Global Modal Helpers
function openAddModal() { window.manager.openAddModal(); }
function closeAddModal() { window.manager.closeAddModal(); }

document.addEventListener('DOMContentLoaded', () => {
    window.manager = new BookmarkManager();
});
