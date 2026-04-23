// Redirect if already logged in
if (localStorage.getItem('token')) window.location.href = 'tasks.html';

async function register() {
    const name     = document.getElementById('name').value.trim();
    const mail     = document.getElementById('email').value.trim();
    const age      = parseInt(document.getElementById('age').value);
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const msg      = document.getElementById('msg');

    if (!name || !mail || !age || !username || !password) {
        msg.textContent = 'Please fill in all fields.';
        return;
    }

    const res = await fetch('../api/auth.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'register', name, mail, age, username, password })
    });

    const data = await res.json();
    msg.textContent = data.message;

    if (data.status === 'success') {
        window.location.href = 'login.html';
    }
}