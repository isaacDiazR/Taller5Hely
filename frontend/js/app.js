// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State
let tasks = [];
let currentFilters = {
    status: 'all',
    priority: 'all'
};

// DOM Elements
const taskForm = document.getElementById('task-form');
const taskList = document.getElementById('task-list');
const filterStatus = document.getElementById('filter-status');
const filterPriority = document.getElementById('filter-priority');
const btnRefresh = document.getElementById('btn-refresh');
const editModal = document.getElementById('edit-modal');
const editForm = document.getElementById('edit-form');
const btnCancelEdit = document.getElementById('btn-cancel-edit');
const closeModal = document.querySelector('.close');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    loadStats();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    taskForm.addEventListener('submit', handleCreateTask);
    editForm.addEventListener('submit', handleUpdateTask);
    filterStatus.addEventListener('change', handleFilterChange);
    filterPriority.addEventListener('change', handleFilterChange);
    btnRefresh.addEventListener('click', () => {
        loadTasks();
        loadStats();
    });
    btnCancelEdit.addEventListener('click', closeEditModal);
    closeModal.addEventListener('click', closeEditModal);
    window.addEventListener('click', (e) => {
        if (e.target === editModal) {
            closeEditModal();
        }
    });
}

// API Functions
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error en la petición');
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showError(error.message);
        throw error;
    }
}

async function loadTasks() {
    try {
        showLoading();
        
        let endpoint = '/tasks';
        const params = new URLSearchParams();
        
        if (currentFilters.status !== 'all') {
            params.append('completed', currentFilters.status === 'completed');
        }
        
        if (currentFilters.priority !== 'all') {
            params.append('priority', currentFilters.priority);
        }
        
        if (params.toString()) {
            endpoint += `?${params.toString()}`;
        }
        
        const data = await fetchAPI(endpoint);
        tasks = data.tasks;
        renderTasks();
    } catch (error) {
        showError('No se pudieron cargar las tareas');
    }
}

async function loadStats() {
    try {
        const data = await fetchAPI('/stats');
        updateStats(data);
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function createTask(taskData) {
    return await fetchAPI('/tasks', {
        method: 'POST',
        body: JSON.stringify(taskData)
    });
}

async function updateTask(taskId, taskData) {
    return await fetchAPI(`/tasks/${taskId}`, {
        method: 'PUT',
        body: JSON.stringify(taskData)
    });
}

async function deleteTask(taskId) {
    return await fetchAPI(`/tasks/${taskId}`, {
        method: 'DELETE'
    });
}

async function toggleTaskComplete(taskId, completed) {
    return await updateTask(taskId, { completed });
}

// Event Handlers
async function handleCreateTask(e) {
    e.preventDefault();
    
    const formData = new FormData(taskForm);
    const taskData = {
        title: formData.get('title').trim(),
        description: formData.get('description').trim(),
        priority: formData.get('priority')
    };
    
    if (!taskData.title) {
        showError('El título es requerido');
        return;
    }
    
    try {
        await createTask(taskData);
        taskForm.reset();
        await loadTasks();
        await loadStats();
        showSuccess('✅ Tarea creada exitosamente');
    } catch (error) {
        showError('Error al crear la tarea');
    }
}

async function handleUpdateTask(e) {
    e.preventDefault();
    
    const taskId = parseInt(document.getElementById('edit-task-id').value);
    const taskData = {
        title: document.getElementById('edit-task-title').value.trim(),
        description: document.getElementById('edit-task-description').value.trim(),
        priority: document.getElementById('edit-task-priority').value,
        completed: document.getElementById('edit-task-completed').checked
    };
    
    try {
        await updateTask(taskId, taskData);
        closeEditModal();
        await loadTasks();
        await loadStats();
        showSuccess('✅ Tarea actualizada exitosamente');
    } catch (error) {
        showError('Error al actualizar la tarea');
    }
}

async function handleDeleteTask(taskId) {
    if (!confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
        return;
    }
    
    try {
        await deleteTask(taskId);
        await loadTasks();
        await loadStats();
        showSuccess('🗑️ Tarea eliminada');
    } catch (error) {
        showError('Error al eliminar la tarea');
    }
}

async function handleToggleComplete(taskId, currentStatus) {
    try {
        await toggleTaskComplete(taskId, !currentStatus);
        await loadTasks();
        await loadStats();
        showSuccess(!currentStatus ? '✅ Tarea completada' : '↩️ Tarea marcada como pendiente');
    } catch (error) {
        showError('Error al actualizar el estado');
    }
}

function handleFilterChange() {
    currentFilters.status = filterStatus.value;
    currentFilters.priority = filterPriority.value;
    loadTasks();
}

// UI Functions
function renderTasks() {
    if (!tasks || tasks.length === 0) {
        taskList.innerHTML = '<p class="empty-state">📋 No hay tareas para mostrar</p>';
        return;
    }
    
    taskList.innerHTML = tasks.map(task => createTaskHTML(task)).join('');
}

function createTaskHTML(task) {
    const priorityEmoji = {
        high: '🔴',
        medium: '🟡',
        low: '🟢'
    };
    
    const priorityText = {
        high: 'Alta',
        medium: 'Media',
        low: 'Baja'
    };
    
    const completedClass = task.completed ? 'completed' : '';
    const completeButtonText = task.completed ? '↩️ Pendiente' : '✅ Completar';
    
    return `
        <div class="task-item ${completedClass}" data-task-id="${task.id}">
            <div class="task-content">
                <div class="task-header">
                    <h3 class="task-title">${escapeHTML(task.title)}</h3>
                    <span class="task-priority priority-${task.priority}">
                        ${priorityEmoji[task.priority]} ${priorityText[task.priority]}
                    </span>
                </div>
                
                ${task.description ? `
                    <p class="task-description">${escapeHTML(task.description)}</p>
                ` : ''}
                
                <div class="task-meta">
                    <span>📅 Creada: ${formatDate(task.created_at)}</span>
                    ${task.updated_at !== task.created_at ? `
                        <span>🔄 Actualizada: ${formatDate(task.updated_at)}</span>
                    ` : ''}
                    ${task.completed ? '<span>✅ Completada</span>' : '<span>⏳ Pendiente</span>'}
                </div>
            </div>
            
            <div class="task-actions">
                <button class="btn btn-complete" onclick="handleToggleComplete(${task.id}, ${task.completed})">
                    ${completeButtonText}
                </button>
                <button class="btn btn-edit" onclick="openEditModal(${task.id})">
                    ✏️ Editar
                </button>
                <button class="btn btn-danger" onclick="handleDeleteTask(${task.id})">
                    🗑️ Eliminar
                </button>
            </div>
        </div>
    `;
}

function openEditModal(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;
    
    document.getElementById('edit-task-id').value = task.id;
    document.getElementById('edit-task-title').value = task.title;
    document.getElementById('edit-task-description').value = task.description || '';
    document.getElementById('edit-task-priority').value = task.priority;
    document.getElementById('edit-task-completed').checked = task.completed;
    
    editModal.classList.add('active');
}

function closeEditModal() {
    editModal.classList.remove('active');
    editForm.reset();
}

function updateStats(stats) {
    document.getElementById('total-tasks').textContent = stats.total || 0;
    document.getElementById('completed-tasks').textContent = stats.completed || 0;
    document.getElementById('pending-tasks').textContent = stats.pending || 0;
}

function showLoading() {
    taskList.innerHTML = '<p class="loading">⏳ Cargando tareas...</p>';
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = `❌ ${message}`;
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #f44336;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideDown 0.3s;
    `;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.style.animation = 'fadeOut 0.3s';
        setTimeout(() => errorDiv.remove(), 300);
    }, 3000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.textContent = message;
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideDown 0.3s;
    `;
    
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.style.animation = 'fadeOut 0.3s';
        setTimeout(() => successDiv.remove(), 300);
    }, 3000);
}

// Utility Functions
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function formatDate(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Add fadeOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(style);
