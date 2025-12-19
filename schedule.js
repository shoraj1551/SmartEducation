/**
 * SmartEducation - Schedule Logic
 */

class ScheduleManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.userData = JSON.parse(localStorage.getItem('user') || '{}');
        this.currentDate = new Date();
        this.tasks = [];

        // UI Bindings
        this.calendarGrid = document.getElementById('calendarGrid');
        this.currentMonthText = document.getElementById('currentMonth');
        this.taskList = document.getElementById('taskList');
        this.emptyTasks = document.getElementById('emptyTasks');
        this.prefTimeLabel = document.getElementById('prefTimeLabel');
        this.addModal = document.getElementById('addTaskModal');
        this.scheduleForm = document.getElementById('scheduleForm');

        this.init();
    }

    async init() {
        if (!this.token) {
            window.location.href = 'index.html';
            return;
        }

        this.prefTimeLabel.textContent = this.userData.preferred_learning_time || 'Morning';

        await this.fetchTasks();
        this.renderCalendar();
        this.renderDailyTasks();
        this.attachListeners();
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
            <div class="task-item ${task.is_completed ? 'completed' : ''}">
                <div class="task-check" onclick="window.scheduleManager.toggleTask('${task.id}', ${!task.is_completed})">
                    ${task.is_completed ? '<i class="fas fa-check" style="font-size: 0.6rem; color: white;"></i>' : ''}
                </div>
                <div class="task-info">
                    <h4>${task.title}</h4>
                    <p>${task.description || 'Focus session'}</p>
                    <span class="time-badge">${this.formatTime(task.start_time)}</span>
                </div>
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
            }
        } catch (err) {
            console.error('Error updating task:', err);
        }
    }

    attachListeners() {
        document.getElementById('prevMonth').onclick = () => {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this.renderCalendar();
        };
        document.getElementById('nextMonth').onclick = () => {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this.renderCalendar();
        };

        this.scheduleForm.onsubmit = (e) => this.handleAddTask(e);
    }

    async handleAddTask(e) {
        e.preventDefault();
        const title = document.getElementById('taskTitle').value;
        const start_time = document.getElementById('taskStart').value;
        const end_time = document.getElementById('taskEnd').value;
        const repeat_pattern = document.getElementById('taskRepeat').value;

        try {
            const response = await fetch('/api/user/schedules', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ title, start_time, end_time, repeat_pattern })
            });

            if (response.ok) {
                await this.fetchTasks();
                this.renderCalendar();
                this.renderDailyTasks();
                this.closeAddModal();
                this.scheduleForm.reset();
            }
        } catch (err) {
            console.error('Error adding task:', err);
        }
    }

    formatTime(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    openAddModal() { this.addModal.style.display = 'flex'; }
    closeAddModal() { this.addModal.style.display = 'none'; }
}

function openAddTaskModal() { window.scheduleManager.openAddModal(); }
function closeAddTaskModal() { window.scheduleManager.closeAddModal(); }

document.addEventListener('DOMContentLoaded', () => {
    window.scheduleManager = new ScheduleManager();
});
