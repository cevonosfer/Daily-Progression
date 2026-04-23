// Redirect to login if no token
const token = localStorage.getItem('token');
if (!token) window.location.href = 'login.html';

function authHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    };
}

async function loadTasks() {
    const res = await fetch('../api/router.php', {
        method: 'GET',
        headers: authHeaders()
    });

    if (res.status === 401) { logout(); return; }

    const tasks = await res.json();
    const list = document.getElementById('taskList');
    list.innerHTML = '';

    if (tasks.length === 0) {
        list.innerHTML = '<li>No tasks yet.</li>';
        return;
    }

    tasks.forEach(task => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span style="text-decoration: ${task.is_done === 'done' ? 'line-through' : 'none'}">
                ${task.name}
            </span>
            &nbsp;
            ${task.is_done !== 'done'
                ? `<button onclick="completeTask(${task.id})">Complete</button>`
                : '<i>(done)</i>'
            }
            &nbsp;
            <button onclick="deleteTask(${task.id})">Delete</button>
        `;
        list.appendChild(li);
    });
}

async function addTask() {
    const taskInput = document.getElementById('newTask');
    const task = taskInput.value.trim();
    const msg = document.getElementById('addMsg');

    if (!task) {
        msg.textContent = 'Task cannot be empty.';
        return;
    }

    const res = await fetch('../api/router.php', {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ task })
    });

    const data = await res.json();
    msg.textContent = data.message;

    if (data.status === 'success') {
        taskInput.value = '';
        loadTasks();
    }
}

async function deleteTask(id) {
    const res = await fetch('../api/router.php', {
        method: 'DELETE',
        headers: authHeaders(),
        body: JSON.stringify({ task_id: id })
    });

    const data = await res.json();
    if (data.status === 'success') loadTasks();
    else alert(data.message);
}

async function completeTask(id) {
    const res = await fetch('../api/router.php', {
        method: 'PUT',
        headers: authHeaders(),
        body: JSON.stringify({ task_id: id })
    });

    const data = await res.json();
    if (data.status === 'success') loadTasks();
    else alert(data.message);
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

loadTasks();