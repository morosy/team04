/*
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/23
    Description: 過去情報の表示用JavaScript
    Note: このファイルは, ユーザーの過去情報を表示するためのJavaScript
*/

console.log("User result table loaded");

document.addEventListener("DOMContentLoaded", () => {
    const showMoreBtn = document.getElementById("showMoreBtn");
    if (showMoreBtn) {
        showMoreBtn.addEventListener("click", () => {
            const hiddenRows = document.querySelectorAll(".hidden-row");
            hiddenRows.forEach(row => {
                row.style.display = "";
            });
            showMoreBtn.style.display = "none";
        });
    }
});

