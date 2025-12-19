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
            window.location.href = 'index.html';
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
            <div class="inbox-item" data-item-id="${item.id}">
                <div class="item-header">
                    <div>
                        <span class="item-type-badge" style="background: ${statusColors[item.status]}">
                            ${item.source_type}
                        </span>
                    </div>
                    <input type="checkbox" class="item-checkbox" data-item-id="${item.id}" 
                           style="width: 18px; height: 18px; cursor: pointer;">
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
}

// Initialize
let inboxManager;
document.addEventListener('DOMContentLoaded', () => {
    inboxManager = new InboxManager();
});
