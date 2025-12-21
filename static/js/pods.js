
/**
 * Accountability Pods Logic
 */
const token = localStorage.getItem('token');
if (!token) window.location.href = '/login';

async function init() {
    await loadInvites();
    await loadPod();
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
                    
                    <button class="btn-nudge" onclick="nudge('${p.id}')">
                        <i class="fas fa-hand-point-right"></i> Nudge
                    </button>
                </div>
            `).join('');
        }
    } catch (e) { console.error(e); }
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

function getInitials(name) {
    if (!name) return '??';
    const parts = name.split(' ');
    if (parts.length > 1) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    return name.slice(0, 2).toUpperCase();
}

init();
