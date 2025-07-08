/*
Designer: Shunsuke MOROZUMI
    Date: 2025/06/17
    change: 2025/07/08 usernameの変更機能の追加
    Description: マイページのjsファイル
    Note: このファイルは, ユーザーのマイページを表示するためのjsファイル.
*/


/*
    Function: copyToClipboard
    Description: 指定された要素のテキストをクリップボードにコピー
    Parameters:
        elementId (string): コピーするテキストを含む要素のID
        label (string): コピーしたテキストのラベル（例: "ID", "名前"）
    Returns: なし
    Note: コピー成功時にメッセージを表示し、2秒後にメッセージを消去します。
    Error Handling: コピーに失敗した場合はアラートを表示します。
*/
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


/*
    Function: toggleUsernameForm
    Description: ユーザ名変更フォームの表示/非表示を切り替える
    Parameters: なし
    Returns: なし
    Note: フォームの初期状態は非表示で、ボタンをクリックすると表示されます。
*/
document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('show-username-form');
    const form = document.getElementById('username-form');

    if (!toggleButton || !form) {
        console.warn("要素が見つかりません");
        return;
    }

    toggleButton.addEventListener('click', function () {
        form.style.display = form.style.display === 'none' ? 'flex' : 'none';
    });
});