/**
 * SmartEducation - Inbox Management Logic
 * Handles learning inbox UI and interactions
 */

class InboxManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.currentFilter = 'active';
        this.selectedItems = new Set();
        this.allItems = [];

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = '/';
            return;
        }

        await this.loadItems();
        await this.updateCapacityIndicator();
        this.attachListeners();
    }

    attachListeners() {
        // Filter tabs
        document.querySelectorAll('.filter-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
                e.target.classList.add('active');
                this.currentFilter = e.target.dataset.filter;
                this.renderItems();
            });
        });

        // Add item button
        document.getElementById('addItemBtn').addEventListener('click', () => this.openAddModal());

        // Add item form
        document.getElementById('addItemForm').addEventListener('submit', (e) => this.handleAddItem(e));

        // Search
        document.getElementById('searchInput').addEventListener('input', (e) => this.handleSearch(e.target.value));

        // Modal close on outside click
        document.getElementById('addItemModal').addEventListener('click', (e) => {
            if (e.target.id === 'addItemModal') {
                this.closeAddModal();
            }
        });
    }

    async loadItems() {
        try {
            const response = await fetch('/api/inbox/items', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.allItems = data.items;
                this.renderItems();
            } else {
                console.error('Failed to load items');
            }
        } catch (error) {
            console.error('Error loading items:', error);
        }
    }

    renderItems() {
        const grid = document.getElementById('inboxGrid');
        const emptyState = document.getElementById('emptyState');

        // Filter items
        let filteredItems = this.allItems;
        if (this.currentFilter !== 'all') {
            filteredItems = this.allItems.filter(item => item.status === this.currentFilter);
        }

        if (filteredItems.length === 0) {
            grid.style.display = 'none';
            emptyState.style.display = 'block';
            return;
        }

        grid.style.display = 'grid';
        emptyState.style.display = 'none';

        grid.innerHTML = filteredItems.map(item => this.createItemCard(item)).join('');

        // Attach item-specific listeners
        this.attachItemListeners();
    }

    createItemCard(item) {
        const statusColors = {
            active: 'rgba(124, 58, 237, 0.2)',
            paused: 'rgba(251, 191, 36, 0.2)',
            completed: 'rgba(34, 197, 94, 0.2)',
            dropped: 'rgba(239, 68, 68, 0.2)'
        };

        return `
            <div class="inbox-item" data-item-id="${item.id}" style="position: relative;">
                <div class="item-header">
                    <div>
                        <span class="item-type-badge" style="background: ${statusColors[item.status]}">
                            ${item.source_type}
                        </span>
                    </div>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                        <button class="share-btn" onclick="event.stopPropagation(); inboxManager.openShareModal('${item.id}', '${item.title.replace(/'/g, "\\'")}', '${item.source_type}')" 
                            style="background: rgba(124, 58, 237, 0.1); border: 1px solid var(--primary); color: var(--primary); padding: 0.4rem 0.8rem; border-radius: 6px; cursor: pointer; font-size: 0.8rem; display: flex; align-items: center; gap: 0.3rem;">
                            <i class="fas fa-user-friends"></i> Share
                        </button>
                        <input type="checkbox" class="item-checkbox" data-item-id="${item.id}" 
                               style="width: 18px; height: 18px; cursor: pointer;">
                    </div>
                </div>
                <h3 class="item-title">${item.title}</h3>
                <p class="item-platform">
                    <i class="fas fa-${this.getSourceIcon(item.source_type)}"></i> 
                    ${item.platform || 'No platform'}
                </p>
                
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" style="width: ${item.progress_percentage}%"></div>
                </div>
                <p class="progress-text">
                    ${Math.round(item.progress_percentage)}% complete
                    ${item.total_duration > 0 ? ` • ${item.completed_duration}/${item.total_duration} min` : ''}
                </p>

                <div class="item-actions">
                    ${this.getActionButtons(item)}
                </div>
            </div>
        `;
    }

    getSourceIcon(sourceType) {
        const icons = {
            course: 'graduation-cap',
            video: 'play-circle',
            playlist: 'list',
            pdf: 'file-pdf',
            article: 'newspaper',
            bookmark: 'bookmark'
        };
        return icons[sourceType] || 'file';
    }

    getActionButtons(item) {
        if (item.status === 'active') {
            return `
                <button class="action-btn" onclick="inboxManager.updateStatus('${item.id}', 'paused')">
                    <i class="fas fa-pause"></i> Pause
                </button>
                <button class="action-btn primary" onclick="inboxManager.updateStatus('${item.id}', 'completed')">
                    <i class="fas fa-check"></i> Complete
                </button>
            `;
        } else if (item.status === 'paused') {
            return `
                <button class="action-btn primary" onclick="inboxManager.updateStatus('${item.id}', 'active')">
                    <i class="fas fa-play"></i> Resume
                </button>
                <button class="action-btn" onclick="inboxManager.updateStatus('${item.id}', 'dropped')">
                    <i class="fas fa-times"></i> Drop
                </button>
            `;
        } else if (item.status === 'completed') {
            return `
                <button class="action-btn" onclick="inboxManager.deleteItem('${item.id}')">
                    <i class="fas fa-trash"></i> Delete
                </button>
            `;
        } else {
            return `
                <button class="action-btn" onclick="inboxManager.deleteItem('${item.id}')">
                    <i class="fas fa-trash"></i> Delete
                </button>
            `;
        }
    }

    attachItemListeners() {
        // Checkbox listeners
        document.querySelectorAll('.item-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const itemId = e.target.dataset.itemId;
                if (e.target.checked) {
                    this.selectedItems.add(itemId);
                } else {
                    this.selectedItems.delete(itemId);
                }
                this.updateBulkActionsBar();
            });
        });
    }

    updateBulkActionsBar() {
        const bar = document.getElementById('bulkActionsBar');
        const count = document.getElementById('selectedCount');

        if (this.selectedItems.size > 0) {
            bar.classList.add('visible');
            count.textContent = `${this.selectedItems.size} selected`;
        } else {
            bar.classList.remove('visible');
        }
    }

    async openAddModal() {
        // Check capacity first
        try {
            const response = await fetch('/api/inbox/check-capacity', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            const result = await response.json();

            if (!result.can_add) {
                alert(result.message + '\n\nSuggestions:\n' + result.suggestions.join('\n'));
                return;
            }

            if (result.warning) {
                if (!confirm(result.warning + '\n\nDo you want to continue?')) {
                    return;
                }
            }

            document.getElementById('addItemModal').style.display = 'flex';
        } catch (error) {
            console.error('Error checking capacity:', error);
            document.getElementById('addItemModal').style.display = 'flex';
        }
    }

    closeAddModal() {
        document.getElementById('addItemModal').style.display = 'none';
        document.getElementById('addItemForm').reset();
    }

    async handleAddItem(e) {
        e.preventDefault();

        const itemData = {
            title: document.getElementById('itemTitle').value,
            source_type: document.getElementById('itemSourceType').value,
            source_url: document.getElementById('itemSourceUrl').value,
            platform: document.getElementById('itemPlatform').value,
            description: document.getElementById('itemDescription').value,
            total_duration: parseInt(document.getElementById('itemDuration').value) || 0
        };

        try {
            const response = await fetch('/api/inbox/items', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify(itemData)
            });

            const result = await response.json();

            if (response.ok) {
                this.closeAddModal();
                await this.loadItems();
                await this.updateCapacityIndicator();
                alert('Learning item added successfully!');
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error adding item:', error);
            alert('Failed to add item. Please try again.');
        }
    }

    async updateStatus(itemId, newStatus) {
        try {
            const response = await fetch(`/api/inbox/items/${itemId}/status`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ status: newStatus })
            });

            const result = await response.json();

            if (response.ok) {
                await this.loadItems();
                await this.updateCapacityIndicator();
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error updating status:', error);
            alert('Failed to update status.');
        }
    }

    async deleteItem(itemId) {
        if (!confirm('Are you sure you want to delete this item?')) {
            return;
        }

        try {
            const response = await fetch(`/api/inbox/items/${itemId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                await this.loadItems();
                await this.updateCapacityIndicator();
            } else {
                alert('Failed to delete item.');
            }
        } catch (error) {
            console.error('Error deleting item:', error);
        }
    }

    async updateCapacityIndicator() {
        try {
            const response = await fetch('/api/inbox/stats', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            const data = await response.json();
            const stats = data.stats;

            // Update capacity slots
            const slots = document.querySelectorAll('.capacity-slots .slot');
            slots.forEach((slot, index) => {
                if (index < stats.active_items) {
                    slot.classList.add('filled');
                } else {
                    slot.classList.remove('filled');
                }
            });

            // Update capacity text
            document.getElementById('capacityText').textContent =
                `${stats.active_items}/${stats.max_active_items}`;

        } catch (error) {
            console.error('Error updating capacity:', error);
        }
    }

    handleSearch(query) {
        const grid = document.getElementById('inboxGrid');
        const items = grid.querySelectorAll('.inbox-item');

        items.forEach(item => {
            const title = item.querySelector('.item-title').textContent.toLowerCase();
            if (title.includes(query.toLowerCase())) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }

    // Bulk actions
    async bulkPause() {
        await this.bulkUpdateStatus('paused');
    }

    async bulkComplete() {
        await this.bulkUpdateStatus('completed');
    }

    async bulkDrop() {
        await this.bulkUpdateStatus('dropped');
    }

    async bulkUpdateStatus(status) {
        if (this.selectedItems.size === 0) return;

        try {
            const response = await fetch('/api/inbox/items/bulk-update', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({
                    item_ids: Array.from(this.selectedItems),
                    status: status
                })
            });

            if (response.ok) {
                this.clearSelection();
                await this.loadItems();
                await this.updateCapacityIndicator();
            }
        } catch (error) {
            console.error('Error in bulk update:', error);
        }
    }

    clearSelection() {
        this.selectedItems.clear();
        document.querySelectorAll('.item-checkbox').forEach(cb => cb.checked = false);
        this.updateBulkActionsBar();
    }

    // ============================================================================
    // POD SHARING FUNCTIONALITY
    // ============================================================================

    async openShareModal(itemId, itemTitle, itemType) {
        this.currentShareItem = { id: itemId, title: itemTitle, type: itemType };
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

                if (friends.length === 0) {
                    selector.innerHTML = '<p style="text-align: center; opacity: 0.5; padding: 2rem;">No pod friends yet. Invite friends from the Pods page!</p>';
                    return;
                }

                selector.innerHTML = friends.map(f => `
                    <label class="friend-checkbox" style="display: flex; align-items: center; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.5rem; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">
                        <input type="checkbox" value="${f.id}" onchange="inboxManager.toggleFriend('${f.id}')" style="margin-right: 1rem; width: 18px; height: 18px; cursor: pointer;">
                        <div class="friend-avatar" style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-weight: 700; font-size: 1rem;">
                            ${this.getInitials(f.name)}
                        </div>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; margin-bottom: 0.2rem;">${f.name}</div>
                            <div style="font-size: 0.85rem; opacity: 0.6;">Level ${f.level} Scholar</div>
                        </div>
                    </label>
                `).join('');
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
                this.closeShareModal();
            } else {
                const error = await res.json();
                alert('Failed to share content: ' + (error.error || 'Unknown error'));
            }
        } catch (e) {
            console.error('Error sharing:', e);
            alert('Error sharing content. Please try again.');
        }
    }

    closeShareModal() {
        document.getElementById('shareModal').style.display = 'none';
        this.selectedFriends = [];
        this.currentShareItem = null;
    }

    getInitials(name) {
        if (!name) return '??';
        const parts = name.split(' ');
        if (parts.length > 1) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
        return name.slice(0, 2).toUpperCase();
    }
}

// Initialize
let inboxManager;
document.addEventListener('DOMContentLoaded', () => {
    inboxManager = new InboxManager();
});
