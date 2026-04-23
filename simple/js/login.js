// Redirect if already logged in
if (localStorage.getItem('token')) window.location.href = 'tasks.html';

async function login() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const msg = document.getElementById('msg');

    if (!username || !password) {
        msg.textContent = 'Please fill in all fields.';
        return;
    }

    const res = await fetch('../api/auth.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'login', username, password })
    });

    const data = await res.json();
    msg.textContent = data.message;

    if (data.status === 'success') {
        localStorage.setItem('token', data.data.token);
        window.location.href = 'tasks.html';
    }
}