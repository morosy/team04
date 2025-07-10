/*
    Designer: Shunsuke MOROZUMI
    Date: 2025/07/09
    Description: JavaScript for the race3 page.
    Note: このファイルは, 三連単レースのJavaScriptを定義
*/

// グローバル変数
// 現在表示されているパネルのインデックス
let currentPanel = 0;


/*
    Function Name: showPanel
    Designer: Shunsuke MOROZUMI
    Date: 2025/07/09
    Description:
        指定されたインデックスのパネルを表示し、他のパネルを非表示にする関数.
    Parameters:
        index (number): 表示するパネルのインデックス.
    Returns:
        None
    Usage:
        showPanel(0); // 0番目のパネルを表示
*/
function showPanel(index) {
    const panels = document.querySelectorAll('.horse-panel');
    panels.forEach((panel, i) => {
        panel.style.display = (i === index) ? 'block' : 'none';
    });

    // n着予想のnを更新
    const placeLabel = document.getElementById('place-label');
    if (placeLabel) {
        placeLabel.textContent = `${index + 1}着予想`;
    }

    currentPanel = index;
}

// 次のパネルを表示する関数
function nextPanel() {
    showPanel((currentPanel + 1) % 3);
}

// 前のパネルを表示する関数
function prevPanel() {
    showPanel((currentPanel + 2) % 3);
}

// イベントリスナーの設定
document.addEventListener('DOMContentLoaded', () => {
    showPanel(0);
});
