function copyToClipboard(elementId, label) {
    const text = document.getElementById(elementId).textContent;
    navigator.clipboard.writeText(text).then(() => {
        const msgId = label === 'ID' ? 'copy-msg-id' : 'copy-msg-name';
        const msgElem = document.getElementById(msgId);
        msgElem.textContent = `${label}をコピーしました`;
        setTimeout(() => {
            msgElem.textContent = '';
        }, 2000);
    }).catch(() => {
        alert("コピーに失敗しました");
    });
}
