document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // フォームの通常の送信を停止

    const errorMessageDiv = document.getElementById('error-message');
    const successMessageDiv = document.getElementById('success-message');

    errorMessageDiv.textContent = ''; // エラーメッセージをクリア
    successMessageDiv.style.display = 'none'; // 成功メッセージを非表示に

    // FormDataオブジェクトを使ってフォームデータを簡単に取得
    const formData = new FormData(event.target);

     try {
         const response = await fetch(event.target.action, { // フォームのaction属性からURLを取得
             method: 'POST',
             body: formData, // FormDataを直接bodyに指定
             headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken') // CSRFトークンをヘッダーに含める
            }
        });

        const data = await response.json(); // DjangoのJsonResponseをパース

        if (response.ok && data.success) {
            successMessageDiv.style.display = 'block';
            setTimeout(() => {
                window.location.href = data.redirect_url || '/'; // ログイン後のホーム画面へのリダイレクト
            }, 2000);
        } else {
            errorMessageDiv.textContent = data.message || 'ログインに失敗しました。'; 
        }
    } catch (error) {
        console.error('Error during login request:', error);
        errorMessageDiv.textContent = 'ネットワークエラーが発生しました。';
    }
});