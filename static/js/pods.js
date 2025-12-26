
/**
 * Accountability Pods Logic
 */
const token = localStorage.getItem('token');
if (!token) window.location.href = '/login';

async function init() {
    await loadInvites();
    await loadPod();
    await loadSharedContent();
}

async function loadInvites() {
    try {
        const res = await fetch('/api/social/invites', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            const list = await res.json();
            const container = document.getElementById('pendingList');
            const area = document.getElementById('pendingArea');

            if (list.length > 0) {
                area.style.display = 'block';
                container.innerHTML = list.map(i => `
                    <div class="pending-item">
                        <span><strong>${i.sender_name}</strong> invited you.</span>
                        <button class="btn btn-sm btn-primary" onclick="acceptInvite('${i.id}')">Accept</button>
                    </div>
                `).join('');
            } else {
                area.style.display = 'none';
            }
        }
    } catch (e) { console.error(e); }
}

async function acceptInvite(id) {
    try {
        await fetch(`/api/social/invites/${id}/accept`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        window.location.reload();
    } catch (e) { alert('Error accepting'); }
}

async function loadPod() {
    try {
        const res = await fetch('/api/social/pod', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            const list = await res.json();
            const grid = document.getElementById('podGrid');

            if (list.length === 0) {
                grid.innerHTML = `<p style="opacity:0.5; grid-column: 1/-1; text-align:center;">You are flying solo. Invite a friend below!</p>`;
                return;
            }

            grid.innerHTML = list.map(p => `
                <div class="partner-card">
                    <div class="partner-avatar">${getInitials(p.name)}</div>
                    <div class="partner-name">${p.name}</div>
                    <div style="font-size:0.8rem; opacity:0.6; margin-bottom:1rem;">Level ${p.level} Scholar</div>
                    
                    <div class="partner-stats">
                        <div class="p-stat">
                            <span class="val">${p.xp}</span>
                            <span class="label">XP</span>
                        </div>
                        <div class="p-stat">
                            <span class="val">${p.tasks_today}</span>
                            <span class="label">Tasks</span>
                        </div>
                    </div>
                    
                    <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                        <button class="btn-nudge" onclick="nudge('${p.id}')" style="flex: 1;">
                            <i class="fas fa-hand-point-right"></i> Nudge
                        </button>
                        <button class="btn-message" onclick="openMessageModal('${p.id}', '${p.name}')" style="flex: 1; background: rgba(59, 130, 246, 0.2); border: 1px solid #3b82f6; color: #3b82f6; padding: 0.5rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem; transition: all 0.2s;" onmouseover="this.style.background='rgba(59, 130, 246, 0.3)'" onmouseout="this.style.background='rgba(59, 130, 246, 0.2)'">
                            <i class="fas fa-comment"></i> Message
                        </button>
                    </div>
                </div>
            `).join('');
        }
    } catch (e) { console.error(e); }
}

async function loadSharedContent() {
    try {
        const res = await fetch('/api/pod/shared-with-me', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok) {
            const items = await res.json();
            const container = document.getElementById('sharedContent');

            if (items.length === 0) {
                container.innerHTML = '<p style="opacity:0.5; text-align:center; grid-column: 1/-1; padding: 2rem;">No content shared with you yet.</p>';
                return;
            }

            container.innerHTML = items.map((item, index) => {
                // Simulate progress (in real app, this would come from backend)
                const progress = Math.floor(Math.random() * 100);

                return `
                <div class="shared-item-card" style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); transition: all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">${item.content_title}</h4>
                            <p style="margin: 0; font-size: 0.85rem; opacity: 0.6;">
                                <i class="fas fa-user"></i> Shared by ${item.owner_name}
                            </p>
                        </div>
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.75rem; white-space: nowrap;">${item.content_type}</span>
                            <button onclick="toggleSharedItemDetails('shared-${index}')" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 0.25rem 0.5rem; border-radius: 4px; cursor: pointer; font-size: 0.75rem;">
                                <i class="fas fa-chevron-down" id="icon-shared-${index}"></i>
                            </button>
                        </div>
                    </div>
                    
                    ${item.share_progress ? `
                        <div class="progress-bar" style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden; margin-top: 1rem; position: relative;">
                            <div class="progress-bar-animated" style="height: 100%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); --progress-width: ${progress}%; width: 0%; transition: width 1s ease-out;"></div>
                            <span style="position: absolute; right: 0.5rem; top: 50%; transform: translateY(-50%); font-size: 0.7rem; font-weight: 700;">${progress}%</span>
                        </div>
                    ` : ''}
                    
                    <div id="shared-${index}" class="expandable-content" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease-out; margin-top: 1rem;">
                        <div style="padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1);">
                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1rem;">
                                <div style="background: rgba(102, 126, 234, 0.1); padding: 0.75rem; border-radius: 6px;">
                                    <div style="font-size: 0.75rem; opacity: 0.6; margin-bottom: 0.25rem;">Shared On</div>
                                    <div style="font-weight: 600;">${new Date(item.created_at).toLocaleDateString()}</div>
                                </div>
                                <div style="background: rgba(118, 75, 162, 0.1); padding: 0.75rem; border-radius: 6px;">
                                    <div style="font-size: 0.75rem; opacity: 0.6; margin-bottom: 0.25rem;">Content Type</div>
                                    <div style="font-weight: 600; text-transform: capitalize;">${item.content_type}</div>
                                </div>
                            </div>
                            <div style="display: flex; gap: 0.5rem;">
                                <button onclick="viewSharedContent('${item.content_id}')" style="flex: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; color: white; padding: 0.75rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem; transition: all 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                                    <i class="fas fa-eye"></i> View Content
                                </button>
                                <button onclick="sendThankYou('${item.user_id}')" style="flex: 1; background: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; color: #22c55e; padding: 0.75rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem; transition: all 0.2s;" onmouseover="this.style.background='rgba(34, 197, 94, 0.3)'" onmouseout="this.style.background='rgba(34, 197, 94, 0.2)'">
                                    <i class="fas fa-heart"></i> Thank
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `}).join('');

            // Animate progress bars after render
            setTimeout(() => {
                document.querySelectorAll('.progress-bar-animated').forEach(bar => {
                    bar.style.width = bar.style.getPropertyValue('--progress-width');
                });
            }, 100);
        }
    } catch (e) {
        console.error('Error loading shared content:', e);
        document.getElementById('sharedContent').innerHTML = '<p style="opacity:0.5; text-align:center; color: #ef4444;">Error loading shared content</p>';
    }
}

function toggleSharedItemDetails(id) {
    const element = document.getElementById(id);
    const icon = document.getElementById('icon-' + id);

    if (element.classList.contains('expanded')) {
        element.classList.remove('expanded');
        element.style.maxHeight = '0';
        icon.style.transform = 'rotate(0deg)';
    } else {
        // Close all other expanded items
        document.querySelectorAll('.expandable-content.expanded').forEach(el => {
            el.classList.remove('expanded');
            el.style.maxHeight = '0';
        });
        document.querySelectorAll('[id^="icon-shared-"]').forEach(ic => {
            ic.style.transform = 'rotate(0deg)';
        });

        element.classList.add('expanded');
        element.style.maxHeight = '500px';
        icon.style.transform = 'rotate(180deg)';
    }
}

function viewSharedContent(contentId) {
    // Navigate to the content (implement based on your routing)
    window.location.href = `/inbox?highlight=${contentId}`;
}

async function sendThankYou(userId) {
    try {
        await fetch('/api/pod/message', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                receiver_id: userId,
                message: '🙏 Thanks for sharing this with me!'
            })
        });
        alert('Thank you message sent!');
    } catch (e) {
        console.error('Error sending thank you:', e);
    }
}

async function sendInvite() {
    const email = document.getElementById('inviteEmail').value;
    if (!email) return;

    try {
        const res = await fetch('/api/social/invite', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        const d = await res.json();
        alert(d.message || d.error);
        if (res.ok) document.getElementById('inviteEmail').value = '';
    } catch (e) { alert('Error sending invite'); }
}

async function nudge(id) {
    try {
        await fetch('/api/social/nudge', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ partner_id: id })
        });
        alert('Nudge sent!');
    } catch (e) { console.error(e); }
}

// ============================================================================
// MESSAGING FUNCTIONALITY
// ============================================================================

let currentPartnerId = null;

async function openMessageModal(partnerId, partnerName) {
    currentPartnerId = partnerId;
    document.getElementById('messagePartnerName').innerHTML = `<i class="fas fa-comment"></i> Messages with ${partnerName}`;
    document.getElementById('messageModal').style.display = 'flex';
    await loadMessages(partnerId);
}

async function loadMessages(partnerId) {
    try {
        const res = await fetch(`/api/pod/messages/${partnerId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok) {
            const messages = await res.json();
            const thread = document.getElementById('messageThread');
            const userStr = localStorage.getItem('user');
            const userId = userStr ? JSON.parse(userStr).id : null;

            if (messages.length === 0) {
                thread.innerHTML = '<p style="opacity:0.5; text-align:center; padding: 2rem;">No messages yet. Start the conversation!</p>';
                return;
            }

            thread.innerHTML = messages.map(m => `
                <div style="margin-bottom: 1rem; text-align: ${m.sender_id === userId ? 'right' : 'left'};">
                    <div style="display: inline-block; max-width: 70%; padding: 0.75rem 1rem; background: ${m.sender_id === userId ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'rgba(255,255,255,0.1)'}; border-radius: 12px; word-wrap: break-word;">
                        ${m.message}
                    </div>
                    <div style="font-size: 0.75rem; opacity: 0.5; margin-top: 0.25rem;">${new Date(m.created_at).toLocaleTimeString()}</div>
                </div>
            `).join('');

            thread.scrollTop = thread.scrollHeight;
        }
    } catch (e) {
        console.error('Error loading messages:', e);
        document.getElementById('messageThread').innerHTML = '<p style="text-align: center; color: #ef4444;">Error loading messages</p>';
    }
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message || !currentPartnerId) return;

    try {
        const res = await fetch('/api/pod/message', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                receiver_id: currentPartnerId,
                message: message
            })
        });

        if (res.ok) {
            input.value = '';
            await loadMessages(currentPartnerId);
        } else {
            alert('Failed to send message');
        }
    } catch (e) {
        console.error('Error sending message:', e);
        alert('Error sending message');
    }
}

function closeMessageModal() {
    document.getElementById('messageModal').style.display = 'none';
    currentPartnerId = null;
}

function getInitials(name) {
    if (!name) return '??';
    const parts = name.split(' ');
    if (parts.length > 1) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    return name.slice(0, 2).toUpperCase();
}

init();
