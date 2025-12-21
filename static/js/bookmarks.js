/**
 * SmartEducation - Bookmarks & Library Sync Logic
 */

class BookmarkManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.bookmarks = [];
        this.filteredBookmarks = [];

        // Bindings
        this.grid = document.getElementById('bookmarkGrid');
        this.emptyState = document.getElementById('emptyLibrary'); // Fixed ID mismatch
        this.searchInput = document.getElementById('librarySearch'); // Corrected ID
        this.filterTabs = document.querySelectorAll('.filter-tab');

        // Modal Bindings
        this.uploadModal = document.getElementById('uploadModal');
        this.uploadForm = document.getElementById('uploadBookForm');
        this.syncBtn = document.getElementById('syncLibraryBtn');
        this.uploadBtn = document.getElementById('uploadBookBtn');
        this.syncOverlay = document.getElementById('syncOverlay');

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = '/';
            return;
        }

        await this.fetchBookmarks();
        this.attachListeners();

        // Initial sorting/grouping
        this.renderClusters();
    }

    async fetchBookmarks() {
        try {
            const response = await fetch('/api/bookmarks?per_page=100', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();

            if (response.ok) {
                this.bookmarks = data.bookmarks || [];
                // Sort by added_at desc default
                this.bookmarks.sort((a, b) => new Date(b.added_at) - new Date(a.added_at));
                this.filteredBookmarks = [...this.bookmarks];
                this.renderClusters();
            }
        } catch (err) {
            console.error('Error fetching library:', err);
        }
    }

    attachListeners() {
        // Search
        if (this.searchInput) {
            this.searchInput.addEventListener('input', () => this.handleFilter());
        }

        // Filter Tabs
        this.filterTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                // Remove active from all
                this.filterTabs.forEach(t => t.classList.remove('active'));
                // Add to clicked
                e.target.classList.add('active');
                this.handleFilter();
            });
        });

        // Sync Library
        if (this.syncBtn) {
            this.syncBtn.addEventListener('click', () => this.handleSync());
        }

        // Upload Book Button
        if (this.uploadBtn) {
            this.uploadBtn.addEventListener('click', () => {
                this.uploadModal.style.display = 'flex';
            });
        }

        // Upload Form Submit
        if (this.uploadForm) {
            this.uploadForm.addEventListener('submit', (e) => this.handleUpload(e));
        }
    }

    handleFilter() {
        const query = this.searchInput.value.toLowerCase();
        const activeTab = document.querySelector('.filter-tab.active');
        const category = activeTab ? activeTab.getAttribute('data-filter') : 'all';

        this.filteredBookmarks = this.bookmarks.filter(bm => {
            const matchesSearch =
                (bm.title && bm.title.toLowerCase().includes(query)) ||
                (bm.description && bm.description.toLowerCase().includes(query)) ||
                (bm.topic && bm.topic.toLowerCase().includes(query)) ||
                (bm.tags && bm.tags.toString().toLowerCase().includes(query));

            let matchesCategory = true;
            if (category !== 'all') {
                // Approximate mapping for demo
                const type = (bm.resource_type || bm.category || '').toLowerCase();
                const topic = (bm.topic || '').toLowerCase();
                matchesCategory = type.includes(category) || topic.includes(category);
            }

            return matchesSearch && matchesCategory;
        });

        this.renderClusters();
    }

    async handleSync() {
        // Show Overlay
        this.syncOverlay.style.display = 'flex';

        try {
            const response = await fetch('/api/bookmarks/sync', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();

            // Fake delay for effect if response was too fast
            await new Promise(r => setTimeout(r, 2000));

            if (response.ok) {
                // Hide Overlay
                this.syncOverlay.style.display = 'none';

                // Show Success Toast/Alert
                // Ideally use a nice toast, for now alert
                // alert(data.message);

                // Refresh Grid
                await this.fetchBookmarks();
            } else {
                this.syncOverlay.style.display = 'none';
                alert(data.error || 'Sync failed');
            }
        } catch (err) {
            this.syncOverlay.style.display = 'none';
            console.error('Sync error:', err);
            alert('Failed to connect to sync service');
        }
    }

    async handleUpload(e) {
        e.preventDefault();

        const fileInput = document.getElementById('uploadFile');
        const titleInput = document.getElementById('uploadTitle');
        const topicInput = document.getElementById('uploadTopic');
        const btn = this.uploadForm.querySelector('button');

        if (!fileInput.files[0]) return;

        const originalText = btn.innerText;
        btn.innerText = 'Uploading...';
        btn.disabled = true;

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('title', titleInput.value);
        formData.append('topic', topicInput.value);

        try {
            const response = await fetch('/api/bookmarks/upload', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${this.token}` }, // Form data doesn't need Content-Type header manually set
                body: formData
            });

            if (response.ok) {
                this.uploadForm.reset();
                this.uploadModal.style.display = 'none';
                await this.fetchBookmarks();
            } else {
                const data = await response.json();
                alert(data.error || 'Upload failed');
            }
        } catch (err) {
            console.error('Upload error:', err);
        } finally {
            btn.innerText = originalText;
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

    renderClusters() {
        if (this.filteredBookmarks.length === 0) {
            this.grid.style.display = 'none';
            if (this.emptyState) this.emptyState.style.display = 'block';
            return;
        }

        this.grid.style.display = 'block'; // Change from grid to block to support clusters
        if (this.emptyState) this.emptyState.style.display = 'none';

        // Group by Source
        const clusters = {};

        this.filteredBookmarks.forEach(bm => {
            const source = bm.source || 'Saved Resources';
            if (!clusters[source]) clusters[source] = [];
            clusters[source].push(bm);
        });

        const sortedSources = Object.keys(clusters).sort((a, b) => {
            // Priority ordering
            const priority = ['Failed', 'Manual Upload', 'Company LMS', 'Google Drive', 'Udemy', 'Coursera', 'YouTube', 'Saved Resources'];
            const idxA = priority.indexOf(a);
            const idxB = priority.indexOf(b);
            if (idxA !== -1 && idxB !== -1) return idxA - idxB;
            if (idxA !== -1) return -1;
            if (idxB !== -1) return 1;
            return a.localeCompare(b);
        });

        let html = '';

        sortedSources.forEach(source => {
            const items = clusters[source];
            if (items.length === 0) return;

            html += `
                <div class="cluster-section" style="margin-bottom: 3rem; animation: slideInUp 0.5s ease;">
                    <h2 class="cluster-title" style="font-size: 1.4rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
                        ${this.getSourceIcon(source)}
                        ${source}
                        <span style="font-size: 0.9rem; color: rgba(255,255,255,0.4); font-weight: 400;">(${items.length})</span>
                    </h2>
                    <div class="bookmark-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem;">
                        ${items.map(bm => this.createCardHTML(bm)).join('')}
                    </div>
                </div>
            `;
        });

        this.grid.innerHTML = html;
    }

    getSourceIcon(source) {
        const s = source.toLowerCase();
        if (s.includes('youtube')) return '<i class="fab fa-youtube" style="color: #ff0000;"></i>';
        if (s.includes('google') || s.includes('drive')) return '<i class="fab fa-google-drive" style="color: #22c55e;"></i>';
        if (s.includes('udemy')) return '<i class="fas fa-graduation-cap" style="color: #a435f0;"></i>';
        if (s.includes('coursera')) return '<i class="fas fa-university" style="color: #0056d2;"></i>';
        if (s.includes('cloud')) return '<i class="fas fa-cloud" style="color: #0ea5e9;"></i>';
        if (s.includes('lms')) return '<i class="fas fa-building" style="color: #f59e00;"></i>';
        if (s.includes('upload')) return '<i class="fas fa-file-upload" style="color: #ec4899;"></i>';
        return '<i class="fas fa-bookmark" style="color: #8b5cf6;"></i>';
    }

    createCardHTML(bm) {
        const icon = this.getSourceIcon(bm.source || 'bookmark');
        return `
            <div class="bookmark-card">
                <div class="card-image" style="height: 140px; font-size: 2.5rem;">
                    ${icon}
                </div>
                <div class="card-content">
                    <div class="category-badge">${bm.topic || bm.category || 'General'}</div>
                    <h3>${bm.title || 'Untitled'}</h3>
                    <p>${bm.description || 'No description available.'}</p>
                    
                    <div class="card-footer">
                        <div class="relevance-score">
                            <i class="fas fa-bolt"></i>
                            ${Math.round(bm.relevance_score * 100)}% Match
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
            </div>
        `;
    }

    // Global helper for close modal since onClick in HTML uses it
    closeUploadModal() {
        this.uploadModal.style.display = 'none';
    }
}

// Global scope helpers
function closeUploadModal() {
    if (window.manager) window.manager.closeUploadModal();
}

document.addEventListener('DOMContentLoaded', () => {
    window.manager = new BookmarkManager();
});
