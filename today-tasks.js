/**
 * SmartEducation - Today's Tasks Widget
 * Displays daily tasks and manages task completion
 */

class TodayTasksManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.tasks = [];
        this.activeTimer = null;
        this.currentTaskId = null;
        this.timerStartTime = null;

        this.init();
    }

    async init() {
        if (!this.token) {
            return;
        }

        await this.loadTodayTasks();
        this.setupEventListeners();
        this.startAutoRefresh();
    }

    async loadTodayTasks() {
        try {
            const response = await fetch('/api/tasks/today', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.tasks = data.tasks;
                this.renderTasks();
            }
        } catch (error) {
            console.error('Error loading today\'s tasks:', error);
        }
    }

    renderTasks() {
        const container = document.getElementById('todayTasksContainer');
        if (!container) return;

        if (this.tasks.length === 0) {
            container.innerHTML = `
                <div class="empty-tasks">
                    <i class="fas fa-check-circle" style="font-size: 3rem; color: rgba(124, 58, 237, 0.3); margin-bottom: 1rem;"></i>
                    <h3>No tasks for today</h3>
                    <p>You're all caught up! Generate a learning plan to get started.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.tasks.map(task => this.createTaskCard(task)).join('');
        this.attachTaskListeners();
    }

    createTaskCard(task) {
        const isActive = this.currentTaskId === task.id;
        const difficultyColors = {
            easy: '#10b981',
            medium: '#f59e0b',
            hard: '#ef4444'
        };

        return `
            <div class="task-card ${isActive ? 'active' : ''}" data-task-id="${task.id}">
                <div class="task-header">
                    <div class="task-meta">
                        <span class="task-difficulty" style="background: ${difficultyColors[task.difficulty_level]}20; color: ${difficultyColors[task.difficulty_level]}">
                            ${task.difficulty_level}
                        </span>
                        <span class="task-duration">
                            <i class="fas fa-clock"></i> ${task.estimated_duration_minutes} min
                        </span>
                    </div>
                    ${task.is_overdue ? '<span class="overdue-badge"><i class="fas fa-exclamation-triangle"></i> Overdue</span>' : ''}
                </div>
                
                <h3 class="task-title">${task.title}</h3>
                <p class="task-description">${task.description || 'No description'}</p>
                
                <div class="task-progress-info">
                    <span><i class="fas fa-book"></i> ${task.task_type}</span>
                    ${task.content_reference?.progress_percentage ?
                `<span><i class="fas fa-chart-line"></i> ${Math.round(task.content_reference.progress_percentage)}% through course</span>`
                : ''}
                </div>

                <div class="task-actions">
                    ${!isActive ? `
                        <button class="task-btn primary" onclick="todayTasksManager.startTask('${task.id}')">
                            <i class="fas fa-play"></i> Start Task
                        </button>
                    ` : `
                        <div class="timer-display" id="timer-${task.id}">
                            <i class="fas fa-stopwatch"></i>
                            <span class="timer-text">00:00</span>
                        </div>
                        <button class="task-btn success" onclick="todayTasksManager.completeTask('${task.id}')">
                            <i class="fas fa-check"></i> Complete
                        </button>
                        <button class="task-btn" onclick="todayTasksManager.stopTask()">
                            <i class="fas fa-stop"></i> Stop
                        </button>
                    `}
                </div>
            </div>
        `;
    }

    attachTaskListeners() {
        // Event listeners are handled via onclick in HTML for simplicity
    }

    startTask(taskId) {
        if (this.activeTimer) {
            if (!confirm('You have another task in progress. Stop it and start this one?')) {
                return;
            }
            this.stopTask();
        }

        this.currentTaskId = taskId;
        this.timerStartTime = Date.now();

        // Start timer
        this.activeTimer = setInterval(() => {
            this.updateTimer();
        }, 1000);

        this.renderTasks();
    }

    updateTimer() {
        if (!this.timerStartTime) return;

        const elapsed = Math.floor((Date.now() - this.timerStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;

        const timerElement = document.querySelector(`#timer-${this.currentTaskId} .timer-text`);
        if (timerElement) {
            timerElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        }
    }

    stopTask() {
        if (this.activeTimer) {
            clearInterval(this.activeTimer);
            this.activeTimer = null;
        }
        this.currentTaskId = null;
        this.timerStartTime = null;
        this.renderTasks();
    }

    async completeTask(taskId) {
        const actualDuration = this.timerStartTime ?
            Math.floor((Date.now() - this.timerStartTime) / 60000) : null;

        try {
            const response = await fetch(`/api/tasks/${taskId}/complete`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({
                    actual_duration_minutes: actualDuration
                })
            });

            if (response.ok) {
                this.stopTask();
                await this.loadTodayTasks();
                this.showCompletionCelebration();
            } else {
                alert('Failed to complete task');
            }
        } catch (error) {
            console.error('Error completing task:', error);
            alert('Failed to complete task');
        }
    }

    showCompletionCelebration() {
        // Simple celebration animation
        const celebration = document.createElement('div');
        celebration.className = 'task-celebration';
        celebration.innerHTML = `
            <div class="celebration-content">
                <i class="fas fa-check-circle" style="font-size: 4rem; color: #10b981;"></i>
                <h2>Task Completed! 🎉</h2>
                <p>Great job! Keep up the momentum.</p>
            </div>
        `;
        document.body.appendChild(celebration);

        setTimeout(() => {
            celebration.classList.add('show');
        }, 100);

        setTimeout(() => {
            celebration.classList.remove('show');
            setTimeout(() => celebration.remove(), 300);
        }, 2000);
    }

    setupEventListeners() {
        // Additional event listeners can be added here
    }

    startAutoRefresh() {
        // Refresh tasks every 5 minutes
        setInterval(() => {
            if (!this.activeTimer) {
                this.loadTodayTasks();
            }
        }, 300000);
    }
}

// Initialize on dashboard
let todayTasksManager;
if (document.getElementById('todayTasksContainer')) {
    document.addEventListener('DOMContentLoaded', () => {
        todayTasksManager = new TodayTasksManager();
    });
}
