var API = '/api';

function checkAuth() {
    return fetch(API + '/auth/check', { credentials: 'include' })
        .then(function (r) { return r.json(); })
        .then(function (d) { return d.authenticated ? d.user : null; })
        .catch(function () { return null; });
}

function updateNav() {
    checkAuth().then(function (user) {
        var el = document.getElementById('auth-links');
        if (!el) return;
        if (user) {
            el.innerHTML =
                '<div class="user-chip">' +
                '<div class="avatar">' + user.username.charAt(0).toUpperCase() + '</div>' +
                '<span>' + user.username + '</span>' +
                '<a href="/dashboard" class="btn btn-outline">Dashboard</a>' +
                '<button onclick="logout()" class="btn btn-outline">Log out</button>' +
                '</div>';
        } else {
            el.innerHTML =
                '<a href="/login">Log in</a>' +
                '<a href="/signup" class="btn btn-primary">Sign up</a>';
        }
    });
}

function logout() {
    fetch(API + '/auth/logout', { method: 'POST', credentials: 'include' })
        .then(function () { window.location.href = '/'; });
}

function showAlert(msg, type) {
    var div = document.createElement('div');
    div.className = 'alert ' + (type === 'error' ? 'alert-err' : 'alert-ok');
    div.textContent = msg;
    var target = document.getElementById('alert-container') || document.querySelector('.wrap') || document.body;
    target.prepend(div);
    setTimeout(function () { div.remove(); }, 4000);
}

function copyToClipboard(text, btn) {
    navigator.clipboard.writeText(text).then(function () {
        var orig = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = orig; }, 1500);
    });
}

document.addEventListener('DOMContentLoaded', updateNav);
