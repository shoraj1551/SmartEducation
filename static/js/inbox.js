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
        await this.loadTodaysSchedule();
        this.attachListeners();
        await this.updateCapacityIndicator();
    }

    attachListeners() {
        // Filter tabs
        const filterTabs = document.querySelectorAll('.filter-tab');
        filterTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                // Remove active class from all tabs
                filterTabs.forEach(t => t.classList.remove('active'));
                // Add active class to clicked tab
                e.target.classList.add('active');

                // Update filter
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
                <button class="action-btn" onclick="inboxManager.moveToLibrary('${item.id}', '${item.title.replace(/'/g, "\\'")}')"
                    style="background: rgba(255,193,7,0.1); border-color: rgba(255,193,7,0.3); color: #fbbf24;">
                    <i class="fas fa-arrow-left"></i> Move to Library
                </button>
            `;
        } else if (item.status === 'paused') {
            return `
                <button class="action-btn primary" onclick="inboxManager.updateStatus('${item.id}', 'active')">
                    <i class="fas fa-play"></i> Resume
                </button>
                <button class="action-btn" onclick="inboxManager.moveToLibrary('${item.id}', '${item.title.replace(/'/g, "\\'")}')"
                    style="background: rgba(255,193,7,0.1); border-color: rgba(255,193,7,0.3); color: #fbbf24;">
                    <i class="fas fa-arrow-left"></i> Move to Library
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

    // ============================================================================
    // STATUS UPDATE & COMPLETION HANDLING
    // ============================================================================

    async updateStatus(itemId, newStatus) {
            try {
                // Find the item to get its title
                const item = this.allItems.find(i => i.id === itemId);
                const itemTitle = item ? item.title : 'this item';

                const response = await fetch(`/api/inbox/items/${itemId}/status`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ status: newStatus })
                });

                if (response.ok) {
                    await this.loadItems();
                    await this.updateCapacityIndicator();

                    // Show completion notification with action buttons
                    if (newStatus === 'completed') {
                        this.showCompletionNotification(itemId, itemTitle);
                    } else {
                        this.showNotification(`✅ Status updated to ${newStatus}`, 'success');
                    }
                } else {
                    const error = await response.json();
                    this.showNotification(`❌ Failed to update status: ${error.error || 'Unknown error'}`, 'error');
                }
            } catch (error) {
                console.error('Error updating status:', error);
                this.showNotification('❌ Error updating status. Please try again.', 'error');
            }
        }

        showCompletionNotification(itemId, itemTitle) {
            // Create notification container if it doesn't exist
            let container = document.getElementById('notificationContainer');
            if (!container) {
                container = document.createElement('div');
                container.id = 'notificationContainer';
                container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 10000; max-width: 450px;';
                document.body.appendChild(container);
            }

            const notification = document.createElement('div');
            notification.className = 'notification success';
            notification.style.cssText = `
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.95) 0%, rgba(16, 185, 129, 0.95) 100%);
            color: white;
            padding: 1.25rem 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            box-shadow: 0 8px 24px rgba(34, 197, 94, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            animation: slideInRight 0.3s ease-out;
        `;

            notification.innerHTML = `
            <div style="display: flex; align-items: start; gap: 1rem;">
                <div style="font-size: 1.5rem;">🎉</div>
                <div style="flex: 1;">
                    <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">Completed!</div>
                    <div style="font-size: 0.9rem; opacity: 0.95; margin-bottom: 1rem;">${itemTitle}</div>
                    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        <button onclick="inboxManager.createFlashcardFor('${itemId}', '${itemTitle.replace(/'/g, "\\'")}')" 
                            style="flex: 1; min-width: 140px; background: rgba(255,255,255,0.25); border: 1px solid rgba(255,255,255,0.4); color: white; padding: 0.6rem 1rem; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.85rem; transition: all 0.2s;"
                            onmouseover="this.style.background='rgba(255,255,255,0.35)'"
                            onmouseout="this.style.background='rgba(255,255,255,0.25)'">
                            📝 Create Flashcard
                        </button>
                        <button onclick="inboxManager.generateAITest('${itemId}', '${itemTitle.replace(/'/g, "\\'")}')" 
                            style="flex: 1; min-width: 140px; background: rgba(124, 58, 237, 0.3); border: 1px solid rgba(124, 58, 237, 0.6); color: white; padding: 0.6rem 1rem; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.85rem; transition: all 0.2s;"
                            onmouseover="this.style.background='rgba(124, 58, 237, 0.4)'"
                            onmouseout="this.style.background='rgba(124, 58, 237, 0.3)'">
                            🤖 Generate AI Test
                        </button>
                    </div>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" 
                    style="background: none; border: none; color: white; font-size: 1.25rem; cursor: pointer; opacity: 0.7; padding: 0; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;"
                    onmouseover="this.style.opacity='1'"
                    onmouseout="this.style.opacity='0.7'">
                    ×
                </button>
            </div>
        `;

            container.appendChild(notification);

            // Auto-remove after 15 seconds
            setTimeout(() => {
                notification.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => notification.remove(), 300);
            }, 15000);
        }

        showNotification(message, type = 'info') {
            let container = document.getElementById('notificationContainer');
            if (!container) {
                container = document.createElement('div');
                container.id = 'notificationContainer';
                container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 10000; max-width: 400px;';
                document.body.appendChild(container);
            }

            const colors = {
                success: 'linear-gradient(135deg, rgba(34, 197, 94, 0.95) 0%, rgba(16, 185, 129, 0.95) 100%)',
                error: 'linear-gradient(135deg, rgba(239, 68, 68, 0.95) 0%, rgba(220, 38, 38, 0.95) 100%)',
                info: 'linear-gradient(135deg, rgba(59, 130, 246, 0.95) 0%, rgba(37, 99, 235, 0.95) 100%)'
            };

            const notification = document.createElement('div');
            notification.style.cssText = `
            background: ${colors[type] || colors.info};
            color: white;
            padding: 1rem 1.25rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            animation: slideInRight 0.3s ease-out;
        `;
            notification.textContent = message;

            container.appendChild(notification);

            setTimeout(() => {
                notification.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => notification.remove(), 300);
            }, 5000);
        }

    // ============================================================================
    // FLASHCARD CREATION
    // ============================================================================

    async createFlashcardFor(itemId, itemTitle) {
            const summary = prompt(`📝 What did you learn from "${itemTitle}"?\n\nSummarize the key takeaways in 2-3 sentences:`);

            if (!summary || summary.trim().length === 0) {
                return;
            }

            try {
                const response = await fetch('/api/recall/create', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        learning_item_id: itemId,
                        front: `What did you learn from: ${itemTitle}?`,
                        back: summary.trim()
                    })
                });

                if (response.ok) {
                    this.showNotification('✅ Flashcard created! Review it in Active Recall.', 'success');
                } else {
                    const error = await response.json();
                    this.showNotification(`❌ Failed to create flashcard: ${error.error || 'Unknown error'}`, 'error');
                }
            } catch (error) {
                console.error('Error creating flashcard:', error);
                this.showNotification('❌ Error creating flashcard. Please try again.', 'error');
            }
        }

    // ============================================================================
    // MOVE TO LIBRARY
    // ============================================================================

    async moveToLibrary(itemId, itemTitle) {
            if (!confirm(`Move "${itemTitle}" back to library?\n\nYou can add it to your inbox again later from the Library.`)) {
                return;
            }

            try {
                const response = await fetch(`/api/inbox/items/${itemId}/move-to-library`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    }
                });

                if (response.ok) {
                    this.showNotification(`✅ "${itemTitle}" moved to library`, 'success');
                    await this.loadItems();
                    await this.updateCapacityIndicator();
                } else {
                    const error = await response.json();
                    this.showNotification(`❌ ${error.error}`, 'error');
                }
            } catch (error) {
                console.error('Error moving to library:', error);
                this.showNotification('❌ Error moving to library', 'error');
            }
        }

    // ============================================================================
    // AI TEST GENERATION
    // ============================================================================

    async generateAITest(itemId, itemTitle) {
            // Show AI test generation modal
            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.style.display = 'flex';
            modal.innerHTML = `
            <div class="modal-card" style="max-width: 600px; background: linear-gradient(135deg, rgba(30, 41, 59, 0.98) 0%, rgba(15, 23, 42, 0.98) 100%); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.15); border-radius: 16px; padding: 2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <h3 style="margin: 0; font-size: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        🤖 AI Test Generation
                    </h3>
                    <button onclick="this.closest('.modal').remove()" 
                        style="background: rgba(255,255,255,0.05); border: none; color: rgba(255,255,255,0.6); font-size: 1.25rem; cursor: pointer; padding: 0.5rem; border-radius: 8px; width: 36px; height: 36px;">
                        ×
                    </button>
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <p style="opacity: 0.8; margin-bottom: 1rem;">Generate AI-powered test questions for:</p>
                    <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid #667eea;">
                        <strong>${itemTitle}</strong>
                    </div>
                </div>

                <div style="background: rgba(255, 193, 7, 0.1); border: 1px solid rgba(255, 193, 7, 0.3); border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem;">
                    <div style="display: flex; align-items: start; gap: 0.75rem;">
                        <div style="font-size: 1.25rem;">⚠️</div>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; margin-bottom: 0.25rem; color: #fbbf24;">Coming Soon!</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">
                                AI-powered test generation is currently under development. This feature will automatically create multiple-choice and short-answer questions based on your learning content.
                            </div>
                        </div>
                    </div>
                </div>

                <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                    <div style="font-weight: 600; margin-bottom: 0.75rem;">📋 Planned Features:</div>
                    <ul style="margin: 0; padding-left: 1.5rem; opacity: 0.8;">
                        <li>Generate 5-10 questions automatically</li>
                        <li>Multiple choice, true/false, and short answer formats</li>
                        <li>Difficulty levels (Easy, Medium, Hard)</li>
                        <li>Instant feedback and explanations</li>
                        <li>Track test scores and progress</li>
                    </ul>
                </div>

                <div style="display: flex; gap: 0.75rem; justify-content: flex-end;">
                    <button onclick="this.closest('.modal').remove()" 
                        class="primary-btn"
                        style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; font-weight: 600;">
                        Got it!
                    </button>
                </div>
            </div>
        `;
            document.body.appendChild(modal);

            // TODO: Implement actual AI test generation
            // This would call an AI service (OpenAI, etc.) to generate questions
            // based on the video/course title and description
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

        // ============================================================================
        // JOIN LIVE CLASS
        // ============================================================================

        async handleJoinClass(event) {
            event.preventDefault();

            const meetingUrl = document.getElementById('classUrl').value.trim();
            const classTitle = document.getElementById('classTitle').value.trim();

            if (!meetingUrl) {
                alert('Please enter a meeting URL');
                return;
            }

            try {
                const response = await fetch('/api/live-class/join', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        meeting_url: meetingUrl,
                        title: classTitle || 'Live Class',
                        platform: 'custom'
                    })
                });

                if (response.ok) {
                    // Open meeting in new tab
                    window.open(meetingUrl, '_blank');

                    // Show success message
                    this.showNotification('✅ Joining class... Opening in new tab', 'success');

                    // Close modal and reset form
                    closeJoinClassModal();
                } else {
                    const error = await response.json();
                    this.showNotification(`❌ ${error.error}`, 'error');
                }
            } catch (error) {
                console.error('Error joining class:', error);
                this.showNotification('❌ Error joining class', 'error');
            }
        }

        // ============================================================================
        // TODAY'S SCHEDULE
        // ============================================================================

        async loadTodaysSchedule() {
            const scheduleContainer = document.getElementById('scheduleItems');

            if (!scheduleContainer) {
                console.error('Schedule container not found');
                return;
            }

            try {
                // Get current time and 6 hours from now
                const now = new Date();
                const sixHoursLater = new Date(now.getTime() + (6 * 60 * 60 * 1000));

                // Fetch schedule from calendar API
                const response = await fetch(`/api/schedule/events?start=${now.toISOString()}&end=${sixHoursLater.toISOString()}`, {
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    const events = data.events || [];

                    if (events.length === 0) {
                        scheduleContainer.innerHTML = '<div style="text-align: center; opacity: 0.5; padding: 1rem;">No events in the next 6 hours</div>';
                        return;
                    }

                    scheduleContainer.innerHTML = events.map(event => {
                        const startTime = new Date(event.start_time);
                        const timeStr = startTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

                        return `
                            <div style="display: flex; align-items: center; gap: 1rem; padding: 0.75rem; background: rgba(255,255,255,0.05); border-radius: 8px;">
                                <div style="font-weight: 700; color: #667eea; min-width: 60px;">${timeStr}</div>
                                <div style="flex: 1;">
                                    <div style="font-weight: 600;">${event.title}</div>
                                    ${event.description ? `<div style="font-size: 0.85rem; opacity: 0.7;">${event.description}</div>` : ''}
                                </div>
                                ${event.meeting_url ? `
                                    <button onclick="window.open('${event.meeting_url}', '_blank')" class="action-btn" style="padding: 0.5rem 1rem;">
                                        <i class="fas fa-video"></i> Join
                                    </button>
                                ` : ''}
                            </div>
                        `;
                    }).join('');
                } else {
                    scheduleContainer.innerHTML = '<div style="text-align: center; opacity: 0.5; padding: 1rem;">Unable to load schedule</div>';
                }
            } catch (error) {
                console.error('Error loading schedule:', error);
                scheduleContainer.innerHTML = '<div style="text-align: center; opacity: 0.5; padding: 1rem;">Error loading schedule</div>';
            }
        }

        // ============================================================================
        // JOIN LIVE CLASS
        // ============================================================================

        async handleJoinClass(event) {
            event.preventDefault();

            const meetingUrl = document.getElementById('classUrl').value.trim();
            const classTitle = document.getElementById('classTitle').value.trim();

            if (!meetingUrl) {
                alert('Please enter a meeting URL');
                return;
            }

            try {
                const response = await fetch('/api/live-class/join', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        meeting_url: meetingUrl,
                        title: classTitle || 'Live Class',
                        platform: 'custom'
                    })
                });

                if (response.ok) {
                    // Open meeting in new tab
                    window.open(meetingUrl, '_blank');

                    // Show success message
                    this.showNotification('✅ Joining class... Opening in new tab', 'success');

                    // Close modal and reset form
                    closeJoinClassModal();
                } else {
                    const error = await response.json();
                    this.showNotification(`❌ ${error.error}`, 'error');
                }
            } catch (error) {
                console.error('Error joining class:', error);
                this.showNotification('❌ Error joining class', 'error');
            }
        }

        // ============================================================================
        // TODAY'S SCHEDULE
        // ============================================================================

        async loadTodaysSchedule() {
            const scheduleContainer = document.getElementById('scheduleItems');

            if (!scheduleContainer) {
                console.error('Schedule container not found');
                return;
            }

            try {
                // Get current time and 6 hours from now
                const now = new Date();
                const sixHoursLater = new Date(now.getTime() + (6 * 60 * 60 * 1000));

                // Fetch schedule from calendar API
                const response = await fetch(`/api/schedule/events?start=${now.toISOString()}&end=${sixHoursLater.toISOString()}`, {
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    const events = data.events || [];

                    if (events.length === 0) {
                        scheduleContainer.innerHTML = '<div style="text-align: center; opacity: 0.5; padding: 1rem;">No events in the next 6 hours</div>';
                        return;
                    }

                    scheduleContainer.innerHTML = events.map(event => {
                        const startTime = new Date(event.start_time);
                        const timeStr = startTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

                        return `
                            <div style="display: flex; align-items: center; gap: 1rem; padding: 0.75rem; background: rgba(255,255,255,0.05); border-radius: 8px;">
                                <div style="font-weight: 700; color: #667eea; min-width: 60px;">${timeStr}</div>
                                <div style="flex: 1;">
                                    <div style="font-weight: 600;">${event.title}</div>
                                    ${event.description ? `<div style="font-size: 0.85rem; opacity: 0.7;">${event.description}</div>` : ''}
                                </div>
                                ${event.meeting_url ? `
                                    <button onclick="window.open('${event.meeting_url}', '_blank')" class="action-btn" style="padding: 0.5rem 1rem;">
                                        <i class="fas fa-video"></i> Join
                                    </button>
                                ` : ''}
                            </div>
                        `;
                    }).join('');
                } else {
                    scheduleContainer.innerHTML = '<div style="text-align: center; opacity: 0.5; padding: 1rem;">Unable to load schedule</div>';
                }
            } catch (error) {
                console.error('Error loading schedule:', error);
                scheduleContainer.innerHTML = '<div style="text-align: center; opacity: 0.5; padding: 1rem;">Error loading schedule</div>';
            }
        }
    }

// Global functions for modals
function openJoinClassModal() {
    document.getElementById('joinClassModal').style.display = 'flex';
}

function closeJoinClassModal() {
    document.getElementById('joinClassModal').style.display = 'none';
    document.getElementById('joinClassForm').reset();
}

// Initialize
let inboxManager;
document.addEventListener('DOMContentLoaded', () => {
    inboxManager = new InboxManager();
});
