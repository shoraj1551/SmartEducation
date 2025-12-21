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

        // OTP Modal Bindings
        this.otpModal = document.getElementById('otpModal');
        this.otpForm = document.getElementById('otpForm');
        this.otpInput = document.getElementById('otpInput');
        this.otpResourceId = document.getElementById('otpResourceId');
        this.otpSentMsg = document.getElementById('otpSentMsg');

        // Restore Missing Bindings
        this.syncBtn = document.getElementById('syncLibraryBtn');
        this.uploadBtn = document.getElementById('uploadBookBtn');
        this.uploadModal = document.getElementById('uploadModal');
        this.uploadForm = document.getElementById('uploadBookForm');
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

    // ... (fetchBookmarks remains same)

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
        // ... (Previous listeners)
        // Search
        if (this.searchInput) {
            this.searchInput.addEventListener('input', () => this.handleFilter());
        }

        // Filter Tabs
        this.filterTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.filterTabs.forEach(t => t.classList.remove('active'));
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

        // OTP Form Submit (Secure Deletion)
        if (this.otpForm) {
            this.otpForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.verifyOtpAndDelete();
            });
        }
    }

    // ... (handleFilter, handleSync, handleUpload remain same)

    handleFilter() {
        const query = this.searchInput.value.toLowerCase();
        const activeTab = document.querySelector('.filter-tab.active');
        const category = activeTab ? activeTab.getAttribute('data-filter') : 'all';

        this.filteredBookmarks = this.bookmarks.filter(bm => {
            const matchesSearch =
                (bm.title && bm.title.toLowerCase().includes(query)) ||
                (bm.description && bm.description.toLowerCase().includes(query)) ||
                (bm.topic && bm.topic.toLowerCase().includes(query)) ||
                (bm.tags && bm.tags.toString().toLowerCase().includes(query)) ||
                (bm.author && bm.author.toLowerCase().includes(query)) ||
                (bm.platform && bm.platform.toLowerCase().includes(query));

            let matchesCategory = true;
            if (category !== 'all') {
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
                this.syncOverlay.style.display = 'none';
                await this.fetchBookmarks();
                // Show generic success
                alert(data.message || 'Sync Complete');
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
                headers: { 'Authorization': `Bearer ${this.token}` },
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
        // Step 1: Request OTP
        this.otpResourceId.value = id;
        this.otpModal.style.display = 'flex';
        this.otpSentMsg.style.display = 'none';
        this.otpInput.value = '';
        this.otpInput.focus();

        try {
            const response = await fetch(`/api/bookmarks/${id}/delete-otp`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${this.token}` }
            });

            if (response.ok) {
                this.otpSentMsg.style.display = 'block';
            } else {
                const data = await response.json();
                alert(data.error || 'Failed to send OTP');
                this.closeOtpModal();
            }
        } catch (err) {
            console.error('OTP Request Error:', err);
            alert('Network error requesting OTP');
            this.closeOtpModal();
        }
    }

    async verifyOtpAndDelete() {
        const id = this.otpResourceId.value;
        const otp = this.otpInput.value;

        if (otp.length !== 6) {
            alert('Please enter a valid 6-digit OTP code');
            return;
        }

        const btn = this.otpForm.querySelector('button[type="submit"]');
        const originalText = btn.innerText;
        btn.innerText = 'Verifying...';
        btn.disabled = true;

        try {
            const response = await fetch(`/api/bookmarks/${id}/confirm`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ otp: otp })
            });

            if (response.ok) {
                this.closeOtpModal();
                this.bookmarks = this.bookmarks.filter(bm => bm.id !== id);
                this.handleFilter();
            } else {
                const data = await response.json();
                alert(data.error || 'Invalid OTP');
            }
        } catch (err) {
            console.error('Delete verification error:', err);
        } finally {
            btn.innerText = originalText;
            btn.disabled = false;
        }
    }

    closeOtpModal() {
        this.otpModal.style.display = 'none';
        this.otpForm.reset();
    }

    // ... (renderClusters logic)
    renderClusters() {
        if (this.filteredBookmarks.length === 0) {
            this.grid.style.display = 'none';
            if (this.emptyState) this.emptyState.style.display = 'block';
            return;
        }

        this.grid.style.display = 'block';
        if (this.emptyState) this.emptyState.style.display = 'none';

        // Group by Source
        const clusters = {};

        this.filteredBookmarks.forEach(bm => {
            const source = bm.source || 'Saved Resources';
            if (!clusters[source]) clusters[source] = [];
            clusters[source].push(bm);
        });

        const sortedSources = Object.keys(clusters).sort((a, b) => {
            const priority = ['Failed', 'Manual Upload', 'Company LMS', 'Google Drive', 'Udemy', 'Coursera', 'YouTube Premium', 'Saved Resources'];
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
        if (s.includes('oreilly') || s.includes("o'reilly")) return '<i class="fas fa-book" style="color: #ef4444;"></i>';
        return '<i class="fas fa-bookmark" style="color: #8b5cf6;"></i>';
    }

    createCardHTML(bm) {
        const icon = this.getSourceIcon(bm.source || 'bookmark');

        // Status & Progress logic
        const status = bm.status || 'not_started';
        const progress = bm.progress || 0;
        const author = bm.author || 'Unknown Author';

        const statusLabels = {
            'not_started': 'Not Started',
            'in_progress': 'In Progress',
            'completed': 'Completed'
        };

        // Construct Metadata string (e.g., 2h 30m • 4.5 Stars)
        let metaString = '';
        if (bm.meta_data) {
            const parts = [];
            if (bm.meta_data.duration) parts.push(`<i class="far fa-clock"></i> ${bm.meta_data.duration}`);
            if (bm.meta_data.pages) parts.push(`<i class="far fa-file-alt"></i> ${bm.meta_data.pages} pgs`);
            if (bm.meta_data.rating) parts.push(`<i class="fas fa-star" style="color: gold;"></i> ${bm.meta_data.rating}`);
            metaString = parts.join(' &nbsp;&bull;&nbsp; ');
        }

        return `
            <div class="bookmark-card">
                <div class="status-badge status-${status}">
                    ${statusLabels[status]}
                </div>
                
                <div class="card-image" style="height: 140px; font-size: 2.5rem; position: relative;">
                    ${icon}
                </div>
                
                <div class="card-content">
                    <div class="category-badge">${bm.topic || bm.category || 'General'}</div>
                    
                    <h3 style="margin-bottom: 0.2rem;">${bm.title || 'Untitled'}</h3>
                    <div style="font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 0.8rem;">
                        by <span style="color: white;">${author}</span>
                    </div>

                    <p>${bm.description || 'No description available.'}</p>
                    
                    ${metaString ? `<div style="font-size: 0.8rem; color: rgba(255,255,255,0.4); margin-bottom: 1rem;">${metaString}</div>` : ''}

                    <!-- Progress Bar -->
                    ${status === 'in_progress' || status === 'completed' ? `
                        <div style="margin-bottom: 1rem;">
                            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-bottom: 0.3rem;">
                                <span>Progress</span>
                                <span>${progress}%</span>
                            </div>
                            <div class="progress-bar-container">
                                <div class="progress-bar-fill" style="width: ${progress}%"></div>
                            </div>
                        </div>
                    ` : ''}

                    <div class="card-footer">
                        <div class="relevance-score">
                            <i class="fas fa-bolt"></i>
                            ${Math.round(bm.relevance_score * 100)}% Match
                        </div>
                        <div class="card-actions">
                            <!-- Commit Button for Features 1 & 3 -->
                            <button class="action-btn commit-btn" onclick="openCommitmentModal('${bm.id}', '${bm.title.replace(/'/g, "\\'")}')" title="Make a Hard Commitment">
                                <i class="fas fa-handshake"></i>
                            </button>
                            
                            <a href="${bm.url}" target="_blank" class="action-btn" title="Open Link">
                                <i class="fas fa-external-link-alt"></i>
                            </a>
                            <button class="action-btn delete-btn" onclick="window.manager.deleteBookmark('${bm.id}')" title="Delete Securely">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    closeUploadModal() {
        this.uploadModal.style.display = 'none';
        // Reset form? Optional.
    }

    closeOtpModal() {
        this.otpModal.style.display = 'none';
        this.otpForm.reset();
        this.otpSentMsg.style.display = 'none';
    }
}

function closeUploadModal() {
    if (window.manager) window.manager.closeUploadModal();
}

function closeOtpModal() {
    if (window.manager) window.manager.closeOtpModal();
}

document.addEventListener('DOMContentLoaded', () => {
    window.manager = new BookmarkManager();
});
