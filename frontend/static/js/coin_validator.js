/*
    Designer: Shunsuke MOROZUMI
    Date: 2025/07/13
    Description: 入力されたコイン枚数が所持コインを超えないように制御するJS.
    Note: このファイルは race1, race2, race3 で共通使用可能.
*/

document.addEventListener("DOMContentLoaded", function() {
    const coinInput = document.getElementById("coin_input");
    const submitButton = document.querySelector(".start-button");

    if (!coinInput || !submitButton) return;

    const currentCoin = Number(document.querySelector(".coin-info")?.textContent?.match(/\d+/)?.[0]);

    const errorElem = document.createElement("p");
    errorElem.style.color = "red";
    errorElem.style.fontWeight = "bold";
    errorElem.style.marginTop = "8px";
    errorElem.id = "coin-error";
    coinInput.parentElement.appendChild(errorElem);

    coinInput.addEventListener("input", function () {
        const value = Number(coinInput.value);

        if (value > currentCoin) {
            errorElem.textContent = `※ 所持コイン ${currentCoin}枚 を超えています`;
            submitButton.disabled = true;
            submitButton.classList.add("disabled-button");
        } else if (value <= 0) {
            errorElem.textContent = "※ 1枚以上入力してください";
            submitButton.disabled = true;
            submitButton.classList.add("disabled-button");
        } else {
            errorElem.textContent = "";
            submitButton.disabled = false;
            submitButton.classList.remove("disabled-button");
        }
    });
});
