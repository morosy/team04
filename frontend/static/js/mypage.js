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
    Function: containsFullWidth
    Description: 文字列に全角文字が含まれているかをチェック
    Parameters:
        str (string): チェックする文字列
    Returns:
        boolean: 全角文字が含まれていればtrue、そうでなければfalse
    Note: 半角英数字のみの場合はfalseを返します。
*/
function containsFullWidth(str) {
    return /[^\u0020-\u007E]/.test(str);
}


/*
    Function: toggleUsernameForm
    Description: ユーザ名変更フォームの表示/非表示を切り替える
    Parameters: なし
    Returns: なし
    Note: フォームの初期状態は非表示で、ボタンをクリックすると表示されます。
    Error Handling: 文字列の長さチェックを行い、1文字以上10文字以下でない場合は警告を表示します。
*/
document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('show-username-form');
    const form = document.getElementById('username-form');
    const input = document.getElementById('new_username');
    const warning = document.getElementById('username-warning');
    const submitButton = form ? form.querySelector('button[type="submit"]') : null;

    // フォームの表示/非表示切り替え
    if (toggleButton && form) {
        toggleButton.addEventListener('click', function () {
            form.style.display = form.style.display === 'none' ? 'flex' : 'none';
        });
    }

    // バリデーション処理
    if (input && warning && submitButton) {
        input.addEventListener('input', function () {
            const value = input.value;
            let errorMsg = "";

            if (value.length === 0) {
                errorMsg = "1文字以上入力してください";
            } else if (value.length > 10) {
                errorMsg = "10文字以内で入力してください";
                input.value = value.slice(0, 10);
            } else if (containsFullWidth(value)) {
                errorMsg = "全角文字は使用できません（半角英数字・記号のみ）";
            }

            // 警告表示
            warning.textContent = errorMsg;

            // エラーがある場合はボタンを非表示、なければ表示
            submitButton.style.display = errorMsg ? 'none' : 'inline-block';
        });

        // 初期状態でボタン非表示にしておくと安心
        submitButton.style.display = 'none';
    }
});
