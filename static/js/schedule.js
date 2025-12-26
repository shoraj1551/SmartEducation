/**
 * SmartEducation - Schedule Logic
 */

class ScheduleManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.userData = JSON.parse(localStorage.getItem('user') || '{}');
        this.currentDate = new Date();
        this.tasks = [];
        this.viewMode = 'month'; // 'month' or 'day'

        // UI Bindings
        this.calendarGrid = document.getElementById('calendarGrid');
        this.currentMonthText = document.getElementById('currentMonth');
        this.taskList = document.getElementById('taskList');
        this.emptyTasks = document.getElementById('emptyTasks');
        this.prefTimeLabel = document.getElementById('prefTimeLabel');
        this.addModal = document.getElementById('addTaskModal');
        this.scheduleForm = document.getElementById('scheduleForm');
        this.monthView = document.getElementById('monthView');
        this.dayView = document.getElementById('dayView');
        this.dayTimeline = document.getElementById('dayTimeline');
        this.dayViewDate = document.getElementById('dayViewDate');

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = '/';
            return;
        }

        this.prefTimeLabel.textContent = this.userData.preferred_learning_time || 'Morning';

        await this.fetchTasks();
        this.renderCalendar();
        this.renderDailyTasks();
        this.attachListeners();

        // Request notification permission
        this.requestNotificationPermission();

        // Start checking for upcoming tasks (every minute)
        this.startNotificationChecker();
    }

    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    console.log('Notification permission granted');
                }
            });
        }
    }

    startNotificationChecker() {
        // Check every minute for upcoming tasks
        setInterval(() => {
            this.checkUpcomingTasks();
        }, 60000); // 60 seconds

        // Also check immediately
        this.checkUpcomingTasks();
    }

    checkUpcomingTasks() {
        if (Notification.permission !== 'granted') return;

        const now = new Date();
        const in15Minutes = new Date(now.getTime() + 15 * 60 * 1000);

        this.tasks.forEach(task => {
            if (task.is_completed) return;

            const taskTime = new Date(task.start_time);
            const timeDiff = taskTime - now;

            // Notify 15 minutes before (within 1-minute window to avoid duplicates)
            if (timeDiff > 14 * 60 * 1000 && timeDiff <= 15 * 60 * 1000) {
                this.sendNotification(task);
            }
        });
    }

    sendNotification(task) {
        const taskTime = new Date(task.start_time);
        const timeStr = taskTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        new Notification('Upcoming Task Reminder', {
            body: `${task.title} starts at ${timeStr}`,
            icon: '/static/img/logo.png',
            badge: '/static/img/logo.png',
            tag: task.id, // Prevents duplicate notifications
            requireInteraction: false
        });
    }

    async fetchTasks() {
        try {
            const response = await fetch('/api/user/schedules', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            if (response.ok) {
                this.tasks = await response.json();
            }
        } catch (err) {
            console.error('Error fetching schedules:', err);
        }
    }

    renderCalendar() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();

        this.currentMonthText.textContent = new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' }).format(this.currentDate);

        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        this.calendarGrid.innerHTML = '';

        // Adjust for Monday start (mon=0, sun=6)
        let startingPos = (firstDay === 0) ? 6 : firstDay - 1;

        // Blanks
        for (let i = 0; i < startingPos; i++) {
            const blank = document.createElement('div');
            blank.className = 'calendar-day';
            blank.style.opacity = '0';
            this.calendarGrid.appendChild(blank);
        }

        const today = new Date();
        const prefTime = this.userData.preferred_learning_time || 'morning';

        // Actual Days
        for (let day = 1; day <= daysInMonth; day++) {
            const dayEl = document.createElement('div');
            dayEl.className = 'calendar-day';
            if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                dayEl.classList.add('today');
            }

            dayEl.innerHTML = `<span class="day-number">${day}</span>`;

            // Smart Slot Indicator (Mock logic: every weekday has a peak slot)
            const dateObj = new Date(year, month, day);
            const dayOfWeek = dateObj.getDay();
            if (dayOfWeek >= 1 && dayOfWeek <= 5) {
                const indicator = document.createElement('div');
                indicator.className = 'peak-slot-indicator';
                indicator.title = `Peak Flow State: ${prefTime}`;
                dayEl.appendChild(indicator);
            }

            dayEl.onclick = () => {
                this.currentDate = new Date(year, month, day);
                this.renderDailyTasks();
            };

            this.calendarGrid.appendChild(dayEl);
        }
    }

    renderDailyTasks() {
        const selectedStr = this.currentDate.toDateString();
        const dailyTasks = this.tasks.filter(t => new Date(t.start_time).toDateString() === selectedStr);

        if (dailyTasks.length === 0) {
            this.taskList.style.display = 'none';
            this.emptyTasks.style.display = 'block';
            return;
        }

        this.taskList.style.display = 'flex';
        this.emptyTasks.style.display = 'none';

        this.taskList.innerHTML = dailyTasks.map(task => `
            <div class="task-item ${task.is_completed ? 'completed' : ''}" style="position: relative;">
                <div class="task-check" onclick="window.scheduleManager.toggleTask('${task.id}', ${!task.is_completed})">
                    ${task.is_completed ? '<i class="fas fa-check" style="font-size: 0.6rem; color: white;"></i>' : ''}
                </div>
                <div class="task-info">
                    <h4>${task.title}</h4>
                    <p>${task.description || 'Focus session'}</p>
                    <span class="time-badge">${this.formatTime(task.start_time)}</span>
                </div>
                <button class="delete-task-btn" onclick="window.scheduleManager.deleteTask('${task.id}')" style="position: absolute; right: 1rem; top: 50%; transform: translateY(-50%); background: rgba(239, 68, 68, 0.1); border: none; color: #ef4444; padding: 0.5rem; border-radius: 6px; cursor: pointer; opacity: 0.7; transition: opacity 0.2s;">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');
    }

    async toggleTask(id, status) {
        try {
            const response = await fetch(`/api/user/schedules/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ is_completed: status })
            });
            if (response.ok) {
                const updated = await response.json();
                this.tasks = this.tasks.map(t => t.id === id ? updated : t);
                this.renderDailyTasks();
                if (this.viewMode === 'day') this.renderDayView();
            }
        } catch (err) {
            console.error('Error updating task:', err);
        }
    }

    async deleteTask(id) {
        if (!confirm('Are you sure you want to delete this task?')) return;

        try {
            const response = await fetch(`/api/user/schedules/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            if (response.ok) {
                this.tasks = this.tasks.filter(t => t.id !== id);
                this.renderCalendar();
                this.renderDailyTasks();
                if (this.viewMode === 'day') this.renderDayView();
            } else {
                alert('Failed to delete task');
            }
        } catch (err) {
            console.error('Error deleting task:', err);
            alert('Failed to delete task. Please try again.');
        }
    }

    attachListeners() {
        document.getElementById('prevMonth').onclick = () => {
            if (this.viewMode === 'month') {
                this.currentDate.setMonth(this.currentDate.getMonth() - 1);
                this.renderCalendar();
            } else {
                this.currentDate.setDate(this.currentDate.getDate() - 1);
                this.renderDayView();
            }
        };
        document.getElementById('nextMonth').onclick = () => {
            if (this.viewMode === 'month') {
                this.currentDate.setMonth(this.currentDate.getMonth() + 1);
                this.renderCalendar();
            } else {
                this.currentDate.setDate(this.currentDate.getDate() + 1);
                this.renderDayView();
            }
        };

        // View toggle
        document.getElementById('monthViewBtn').onclick = () => this.switchView('month');
        document.getElementById('dayViewBtn').onclick = () => this.switchView('day');

        this.scheduleForm.onsubmit = (e) => this.handleAddTask(e);
    }

    async handleAddTask(e) {
        e.preventDefault();

        // Get form values using CORRECT field IDs from HTML
        const title = document.getElementById('taskTitle').value;
        const time = document.getElementById('taskTime').value;
        const frequency = document.getElementById('taskFreq').value;
        const priority = document.getElementById('taskPriority').value;
        const importance = document.getElementById('taskImportance').value;

        // Create ISO datetime from selected date + time
        const year = this.currentDate.getFullYear();
        const month = String(this.currentDate.getMonth() + 1).padStart(2, '0');
        const day = String(this.currentDate.getDate()).padStart(2, '0');
        const start_time = `${year}-${month}-${day}T${time}:00`;

        // Calculate end time (1 hour later by default)
        const startDate = new Date(start_time);
        const endDate = new Date(startDate.getTime() + 60 * 60 * 1000);
        const end_time = endDate.toISOString();

        const repeat_pattern = frequency;

        try {
            const response = await fetch('/api/user/schedules', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({
                    title,
                    start_time,
                    end_time,
                    repeat_pattern,
                    priority,
                    importance
                })
            });

            if (response.ok) {
                // Show success feedback
                const submitBtn = document.getElementById('submitTaskBtn');
                submitBtn.innerHTML = '<i class="fas fa-check"></i> Task Created!';
                submitBtn.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';

                // Wait a moment before closing
                setTimeout(() => {
                    this.fetchTasks();
                    this.renderCalendar();
                    this.renderDailyTasks();
                    if (this.viewMode === 'day') this.renderDayView();
                    this.closeAddModal();
                    this.scheduleForm.reset();

                    // Reset button
                    submitBtn.innerHTML = 'Create Task';
                    submitBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                }, 800);
            } else {
                const error = await response.json();
                alert(`Failed to add task: ${error.error || 'Unknown error'}`);
            }
        } catch (err) {
            console.error('Error adding task:', err);
            alert('Failed to add task. Please try again.');
        }
    }

    formatTime(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    switchView(mode) {
        this.viewMode = mode;
        const monthBtn = document.getElementById('monthViewBtn');
        const dayBtn = document.getElementById('dayViewBtn');

        if (mode === 'month') {
            this.monthView.style.display = 'block';
            this.dayView.style.display = 'none';
            monthBtn.style.background = 'var(--primary)';
            monthBtn.style.color = 'white';
            dayBtn.style.background = 'transparent';
            dayBtn.style.color = 'rgba(255,255,255,0.5)';
            this.renderCalendar();
        } else {
            this.monthView.style.display = 'none';
            this.dayView.style.display = 'block';
            dayBtn.style.background = 'var(--primary)';
            dayBtn.style.color = 'white';
            monthBtn.style.background = 'transparent';
            monthBtn.style.color = 'rgba(255,255,255,0.5)';
            this.renderDayView();
        }
    }

    renderDayView() {
        // Update header
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        this.dayViewDate.textContent = this.currentDate.toLocaleDateString('en-US', options);

        // Get tasks for selected day
        const selectedStr = this.currentDate.toDateString();
        const dailyTasks = this.tasks.filter(t => new Date(t.start_time).toDateString() === selectedStr);

        // Create half-hour timeline (12 AM - 11:30 PM = 48 slots)
        let html = '';
        for (let hour = 0; hour <= 23; hour++) {
            for (let minute = 0; minute < 60; minute += 30) {
                const hourStr = hour === 0 ? '12' :
                    hour < 12 ? `${hour}` :
                        hour === 12 ? '12' :
                            `${hour - 12}`;
                const minuteStr = minute === 0 ? '00' : '30';
                const ampm = hour < 12 ? 'AM' : 'PM';
                const timeLabel = `${hourStr}:${minuteStr} ${ampm}`;

                // Find tasks that start in this 30-minute window
                const tasksInSlot = dailyTasks.filter(t => {
                    const taskDate = new Date(t.start_time);
                    const taskHour = taskDate.getHours();
                    const taskMinute = taskDate.getMinutes();
                    return taskHour === hour && taskMinute >= minute && taskMinute < minute + 30;
                });

                html += `
                    <div class="hour-slot" style="display: flex; border-bottom: 1px solid rgba(255,255,255,0.05); padding: 0.75rem 0; min-height: 50px;">
                        <div class="hour-label" style="width: 100px; color: rgba(255,255,255,0.4); font-size: 0.85rem; font-weight: ${minute === 0 ? '600' : '400'};">${timeLabel}</div>
                        <div class="hour-tasks" style="flex: 1;">
                            ${tasksInSlot.map(task => `
                                <div class="hour-task ${task.is_completed ? 'completed' : ''}" style="background: rgba(124, 58, 237, 0.1); border-left: 3px solid var(--primary); padding: 0.75rem; border-radius: 6px; margin-bottom: 0.5rem;">
                                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                                        <div class="task-check" onclick="window.scheduleManager.toggleTask('${task.id}', ${!task.is_completed})" style="width: 20px; height: 20px; border: 2px solid rgba(255,255,255,0.3); border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                                            ${task.is_completed ? '<i class="fas fa-check" style="font-size: 0.6rem; color: white;"></i>' : ''}
                                        </div>
                                        <div style="flex: 1;">
                                            <h4 style="margin: 0 0 0.25rem 0; font-size: 0.95rem;">${task.title}</h4>
                                            <p style="margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.5);">${task.description || 'Focus session'}</p>
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                            ${tasksInSlot.length === 0 ? '<div style="color: rgba(255,255,255,0.15); font-size: 0.8rem;"></div>' : ''}
                        </div>
                    </div>
                `;
            }
        }

        this.dayTimeline.innerHTML = html;
    }

    openAddModal() { this.addModal.style.display = 'flex'; }
    closeAddModal() { this.addModal.style.display = 'none'; }
}

function openAddTaskModal() { window.scheduleManager.openAddModal(); }
function closeAddTaskModal() { window.scheduleManager.closeAddModal(); }

document.addEventListener('DOMContentLoaded', () => {
    window.scheduleManager = new ScheduleManager();
});
