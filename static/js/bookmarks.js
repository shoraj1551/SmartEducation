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
                this.extractCategories();
            }
        } catch (err) {
            console.error('Error fetching library:', err);
        }
    }

    extractCategories() {
        if (!this.bookmarks || this.bookmarks.length === 0) return;

        // Extract unique types
        const types = new Set();
        this.bookmarks.forEach(b => {
            let type = b.resource_type || b.category;
            if (type) types.add(type.toLowerCase());
        });

        const container = document.getElementById('filterContainer');
        if (!container) return;

        // Clear container safely
        container.innerHTML = '';

        // Create helper for click handling
        const onTabClick = (e) => {
            document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            this.handleFilter();
        };

        // Create "All Items" Tab Programmatically to ensure listener works
        const allTab = document.createElement('div');
        allTab.className = 'filter-tab active';
        allTab.dataset.filter = 'all';
        allTab.textContent = 'All Items';
        allTab.onclick = onTabClick;
        container.appendChild(allTab);

        // Sort and Render dynamic tabs
        Array.from(types).sort().forEach(type => {
            const label = type.charAt(0).toUpperCase() + type.slice(1);
            const tab = document.createElement('div');
            tab.className = 'filter-tab';
            tab.dataset.filter = type;
            tab.textContent = label;
            tab.onclick = onTabClick;
            container.appendChild(tab);
        });
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
        // Open Connect Modal instead of direct sync
        document.getElementById('connectAccountsModal').style.display = 'flex';
    }

    async startSyncFlow() {
        document.getElementById('connectAccountsModal').style.display = 'none';
        this.syncOverlay.style.display = 'flex';

        try {
            const response = await fetch('/api/bookmarks/sync', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${this.token}` }
            });

            const text = await response.text();
            let data;
            try {
                data = JSON.parse(text);
            } catch (e) {
                console.error('Sync error response:', text);
                throw new Error('Server returned invalid response');
            }

            // Fake delay for effect
            setTimeout(async () => {
                this.syncOverlay.style.display = 'none';
                if (response.ok) {
                    await this.fetchBookmarks();
                    alert(data.message || 'Sync complete!');
                } else {
                    alert(data.error || 'Sync failed');
                }
            }, 2000);

        } catch (e) {
            console.error(e);
            this.syncOverlay.style.display = 'none';
            alert('Sync failed (check console)');
        }
    }

    connectAccount(provider) {
        // Mock connection logic
        const btn = event.target;
        btn.textContent = 'Connecting...';
        btn.disabled = true;

        setTimeout(() => {
            btn.textContent = 'Connected';
            btn.classList.remove('secondary-btn');
            btn.classList.add('primary-btn');

            // Update status text
            const statusEl = document.getElementById(provider === 'google-drive' ? 'driveStatus' : `${provider}Status`);
            if (statusEl) {
                statusEl.textContent = 'Active • Last synced just now';
                statusEl.style.color = '#4ade80';
            }
        }, 1200);
    }

    async handleUpload(e) {
        e.preventDefault();

        const fileInput = document.getElementById('uploadFile');
        const files = fileInput.files;
        const btn = this.uploadForm.querySelector('button');
        const titleInput = document.getElementById('uploadTitle');
        const topicInput = document.getElementById('uploadTopic');

        // Optional safe access if elements were removed/changed
        const titleVal = titleInput ? titleInput.value : '';
        const topicVal = topicInput ? topicInput.value : '';

        if (files.length === 0) return;

        if (files.length > 5) {
            alert('Maximum 5 files allowed per upload.');
            return;
        }

        const originalText = btn.innerText;
        btn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Uploading ${files.length} items...`;
        btn.disabled = true;

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('file', files[i]);
        }
        if (titleVal) formData.append('title', titleVal);
        if (topicVal) formData.append('topic', topicVal);

        try {
            const response = await fetch('/api/bookmarks/upload', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${this.token}` },
                body: formData
            });

            const text = await response.text();
            let result;
            try {
                result = JSON.parse(text);
            } catch (e) {
                console.error('Server error response:', text);
                throw new Error('Server returned invalid response');
            }

            if (response.ok) {
                this.uploadForm.reset();
                this.uploadModal.style.display = 'none';
                await this.fetchBookmarks();
                alert(result.message);
            } else {
                alert(result.error || 'Upload failed');
            }
        } catch (err) {
            console.error('Upload catch error:', err);
            alert('Upload failed (check console for details)');
        } finally {
            btn.innerHTML = originalText;
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

        // Inbox Button State
        const isInboxDisabled = bm.in_inbox ? 'disabled' : '';
        const inboxBtnText = bm.in_inbox ? '<i class="fas fa-check"></i>' : '<i class="fas fa-inbox"></i>';
        const inboxBtnClass = bm.in_inbox ? 'action-btn inbox-btn disabled' : 'action-btn inbox-btn';

        return `
            <div class="bookmark-card">
                <div class="status-badge status-${status}">
                    ${statusLabels[status]}
                </div>
                
                <div class="card-image" style="height: 140px; font-size: 2.5rem; position: relative;">
                    ${icon}
                </div>
                
                <div class="card-content">
                    <div class="category-badge">${escapeHTML(bm.topic || bm.category || 'General')}</div>
                    
                    <h3 style="margin-bottom: 0.2rem;">${escapeHTML(bm.title || 'Untitled')}</h3>
                    <div style="font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 0.8rem;">
                        by <span style="color: white;">${escapeHTML(author)}</span>
                    </div>

                    <p>${escapeHTML(bm.description || 'No description available.')}</p>
                    
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
                            <!-- Add to Inbox Button -->
                            <button class="${inboxBtnClass}"
                                    onclick="window.manager.addToInbox('${bm.id}', '${bm.title.replace(/'/g, "\\'")}')"
                                    title="Add to Learning Inbox"
                                    ${isInboxDisabled}>
                                ${inboxBtnText}
                            </button>
                            
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
                            <button class="action-btn share-btn" onclick="window.manager.openShareModal('${bm.id}', '${bm.title.replace(/'/g, "\\'")}', '${bm.resource_type}')" title="Share with Pod">
                                <i class="fas fa-share-alt"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    async addToInbox(bookmarkId, title) {
        try {
            const response = await fetch(`/api/inbox/items/${bookmarkId}/move-to-inbox`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                alert(`✅ "${title}" added to Learning Inbox!`);
            } else {
                const error = await response.json();
                alert(`❌ ${error.error || 'Failed to add to inbox'}`);
            }
        } catch (error) {
            console.error('Error adding to inbox:', error);
            alert('❌ Error adding to inbox');
        }
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

    // ============================================================================
    // SHARING LOGIC
    // ============================================================================

    async openShareModal(itemId, itemTitle, itemType) {
        this.currentShareItem = { id: itemId, title: itemTitle, type: itemType || 'bookmark' };
        this.selectedFriends = [];

        document.getElementById('shareItemTitle').textContent = `Sharing: ${itemTitle}`;
        document.getElementById('shareModal').style.display = 'flex';

        await this.loadPodFriends();
    }

    async loadPodFriends() {
        try {
            const res = await fetch('/api/social/pod', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });

            if (res.ok) {
                const friends = await res.json();
                const selector = document.getElementById('friendSelector');

                if (!Array.isArray(friends) || friends.length === 0) {
                    selector.innerHTML = '<p style="text-align: center; opacity: 0.5; padding: 2rem;">No pod friends yet. Invite friends from the Pods page!</p>';
                    return;
                }

                selector.innerHTML = friends.map(f => `
                    <label class="friend-checkbox" style="display: flex; align-items: center; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.5rem; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">
                        <input type="checkbox" value="${f.id}" onchange="window.manager.toggleFriend('${f.id}')" style="margin-right: 1rem; width: 18px; height: 18px; cursor: pointer;">
                        <div class="friend-avatar" style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-weight: 700; font-size: 1rem;">
                            ${(f.name || 'U').charAt(0)}
                        </div>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; margin-bottom: 0.2rem;">${f.name}</div>
                            <div style="font-size: 0.85rem; opacity: 0.6;">Level ${f.level || 1} Scholar</div>
                        </div>
                    </label>
                `).join('');
            } else {
                document.getElementById('friendSelector').innerHTML = '<p style="text-align: center; color: #ef4444;">Error loading friends. (404/500)</p>';
            }
        } catch (e) {
            console.error('Error loading friends:', e);
            document.getElementById('friendSelector').innerHTML = '<p style="text-align: center; color: #ef4444;">Error loading friends. Please try again.</p>';
        }
    }

    toggleFriend(friendId) {
        if (!this.selectedFriends) this.selectedFriends = [];
        if (this.selectedFriends.includes(friendId)) {
            this.selectedFriends = this.selectedFriends.filter(id => id !== friendId);
        } else {
            this.selectedFriends.push(friendId);
        }
    }

    async confirmShare() {
        if (!this.selectedFriends || this.selectedFriends.length === 0) {
            alert('Please select at least one friend to share with');
            return;
        }

        const btn = document.querySelector('#shareModal .primary-btn');
        const originalText = btn.innerText;
        btn.innerText = 'Sharing...';
        btn.disabled = true;

        try {
            const res = await fetch('/api/pod/share', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content_type: this.currentShareItem.type,
                    content_id: this.currentShareItem.id,
                    content_title: this.currentShareItem.title,
                    partner_ids: this.selectedFriends
                })
            });

            if (res.ok) {
                alert('Content shared successfully!');
                document.getElementById('shareModal').style.display = 'none';
                this.selectedFriends = [];
            } else {
                const err = await res.json();
                alert('Share failed: ' + (err.error || 'Unknown error'));
            }
        } catch (e) {
            console.error('Share error:', e);
            alert('Share failed due to network error');
        } finally {
            btn.innerText = originalText;
            btn.disabled = false;
        }
    }
    // ============================================================================
    // COMMITMENT MODAL LOGIC
    // ============================================================================

    openCommitmentModal(id, title) {
        document.getElementById('commitResourceId').value = id;
        document.getElementById('commitResourceTitle').textContent = `Commitment for: ${title}`;

        // Default Date: 7 days from now
        const date = new Date();
        date.setDate(date.getDate() + 7);
        document.getElementById('commitDate').valueAsDate = date;

        document.getElementById('commitmentModal').style.display = 'flex';
    }

    closeCommitmentModal() {
        document.getElementById('commitmentModal').style.display = 'none';
        document.getElementById('commitmentForm').reset();
    }

    async handleCommitment(e) {
        e.preventDefault();

        const resourceId = document.getElementById('commitResourceId').value;
        const targetDate = document.getElementById('commitDate').value;
        const dailyMinutes = document.getElementById('commitMinutes').value;

        const btn = e.target.querySelector('button[type="submit"]');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing...';
        btn.disabled = true;

        try {
            const response = await fetch('/api/commitment', { // Assuming this route handles creation
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    resource_id: resourceId,
                    target_date: targetDate,
                    daily_minutes: parseInt(dailyMinutes)
                })
            });

            if (response.ok) {
                alert('Commitment Signed! The Penalty Clause is now active.');
                this.closeCommitmentModal();
                // Optionally update UI to show "Signed" status
                await this.fetchBookmarks();
            } else {
                const data = await response.json();
                alert('Failed to sign commitment: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Commitment error:', error);
            alert('Network error signing commitment');
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }
}

// Global functions for HTML onclick handlers
function openCommitmentModal(id, title) {
    if (window.manager) window.manager.openCommitmentModal(id, title);
}

function closeCommitmentModal() {
    if (window.manager) window.manager.closeCommitmentModal();
}

function closeUploadModal() {
    if (window.manager) window.manager.closeUploadModal();
}

function closeOtpModal() {
    if (window.manager) window.manager.closeOtpModal();
}

document.addEventListener('DOMContentLoaded', () => {
    window.manager = new BookmarkManager();

    // Bind Commitment Form
    const commitForm = document.getElementById('commitmentForm');
    if (commitForm) {
        commitForm.addEventListener('submit', (e) => window.manager.handleCommitment(e));
    }
});
