function showAlert(msg, type) {
    var div = document.createElement('div');
    div.className = 'alert ' + (type === 'error' ? 'alert-err' : 'alert-ok');
    div.textContent = msg;
    var box = document.getElementById('alert-container') || document.querySelector('.wrap') || document.body;
    box.prepend(div);
    setTimeout(function() { div.remove(); }, 4000);
}

function copyToClipboard(text, btn) {
    navigator.clipboard.writeText(text).then(function() {
        var orig = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(function() { btn.textContent = orig; }, 1500);
    });
}
