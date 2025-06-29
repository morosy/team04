// frontend/static/js/registration.js
document.addEventListener('DOMContentLoaded', function() {
    const userIdField = document.getElementById('user_id');
    const usernameField = document.getElementById('username');
    const passwordField = document.getElementById('password');
    const registerButton = document.getElementById('registerButton');
    const messageDiv = document.getElementById('message');

    // ユーザーIDを生成するAPIを呼び出す関数
    async function generateUserId() {
        try {
            messageDiv.className = 'message';
            messageDiv.textContent = 'ユーザーIDを生成中...';
            // バックエンドの /api/generate-user-id/ を呼び出す
            const response = await fetch('/api/generate-user-id/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}) // 空のJSONを送信
            });
            const data = await response.json();

            if (data.registration_success) {
                userIdField.value = data.user_ID;
                messageDiv.className = 'message success';
                messageDiv.textContent = 'ユーザーIDが生成されました。';
            } else {
                userIdField.value = 'エラー';
                messageDiv.className = 'message error';
                messageDiv.textContent = `ID生成失敗: ${data.errorMessage}`;
                registerButton.disabled = true; // エラー時は登録ボタンを無効化
            }
        } catch (error) {
            userIdField.value = '通信エラー';
            messageDiv.className = 'message error';
            messageDiv.textContent = `ID生成通信エラー: ${error.message}`;
            registerButton.disabled = true; // エラー時は登録ボタンを無効化
        }
    }

    // ページロード時にユーザーIDを生成
    generateUserId();

    // 登録ボタンクリック時の処理
    registerButton.addEventListener('click', async function() {
        const userId = userIdField.value;
        const username = usernameField.value;
        const password = passwordField.value;

        // 簡単なクライアント側バリデーション
        if (!userId || userId === 'エラー' || userId === '通信エラー') {
            messageDiv.className = 'message error';
            messageDiv.textContent = '有効なユーザーIDがありません。';
            return;
        }
        if (!username || username.length < 1 || username.length > 10 || !/^[a-zA-Z0-9]+$/.test(username)) {
            messageDiv.className = 'message error';
            messageDiv.textContent = 'ユーザー名は半角英数字1～10文字で入力してください。';
            return;
        }
        if (!password || password.length < 8 || password.length > 16 || !/^[a-zA-Z0-9]+$/.test(password)) {
            messageDiv.className = 'message error';
            messageDiv.textContent = 'パスワードは半角英数字8～16文字で入力してください。';
            return;
        }

        messageDiv.className = 'message';
        messageDiv.textContent = '登録処理中...';

        try {
            // バックエンドの /api/name-registration/register/ を呼び出す
            const response = await fetch('/api/name-registration/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_name: username,
                    password: password,
                    user_ID: parseInt(userId) // 数値に変換して送信
                })
            });
            const data = await response.json();

            if (data.success) {
                messageDiv.className = 'message success';
                messageDiv.textContent = '登録が完了しました！ログイン画面へ遷移します。';
                // 実際にはここでログイン画面へリダイレクトします
                // 例: setTimeout(() => window.location.href = '/login/', 2000);
            } else {
                messageDiv.className = 'message error';
                messageDiv.textContent = `登録失敗: ${data.errorMessage}`;
            }
        } catch (error) {
            messageDiv.className = 'message error';
            messageDiv.textContent = `通信エラー: ${error.message}`;
        }
    });
});