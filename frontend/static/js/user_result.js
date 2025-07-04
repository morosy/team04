/*
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/23
    Description: 過去情報の表示用JavaScript
    Note: このファイルは, ユーザーの過去情報を表示するためのJavaScript
*/

console.log("User result table loaded");


document.addEventListener("DOMContentLoaded", () => {
    console.log("user_result.js is running");

    const rows = Array.from(document.querySelectorAll(".result-row"));
    const btn = document.getElementById("showMoreBtn");
    let visibleCount = 10;

    // 初期状態で11行目以降非表示
    rows.forEach((row, index) => {
        if (index >= visibleCount) {
            row.classList.add("hidden-row");
        } else {
            row.classList.remove("hidden-row");
        }
    });

    btn.addEventListener("click", () => {
        console.log("Button clicked");
        visibleCount += 10;

        rows.forEach((row, index) => {
            if (index < visibleCount) {
                row.classList.remove("hidden-row");  // ← これが大事！！
            }
        });

        if (visibleCount >= rows.length) {
            btn.style.display = "none";
        }
    });
});
