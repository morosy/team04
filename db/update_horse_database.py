'''
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/10
    Description: 馬データを更新するスクリプト
        以下の順序で関数を呼び出し, 馬データを更新する
        1. delete_horse_database() - 既存の馬データを削除
        2. generate_horse_database(N) - 新しい馬データを生成, CSVファイルに書き出す
        3. insert_horse_database() - 新しい馬データをデータベースに挿入
'''


import datetime


'''
    Function Name: write_log
    Designer: Shunsuke MOROZUMI
    Date: 2025/06/10
    Description:
        ログファイルにメッセージを書き込む.
        ログファイルは追記モードで開かれ, 現在時刻とともにメッセージが書き込まれる.
        時刻は日本標準時(JST)で表示される.
    Parameters:
        message (str): ログに書き込むメッセージ
    Returns: なし
    Usage: write_log("メッセージ")
'''
def write_log(message: str):
    # JST(日本標準時)での現在時刻を取得
    jst = datetime.timezone(datetime.timedelta(hours=9), 'JST')
    now = datetime.datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S %Z")

    # ログファイルに追記モードで書き込む
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")



if __name__ == "__main__":
    from delete_horse_database import delete_horse_database
    from generate_horse_database import generate_horse_database
    from generate_horse_database import insert_horse_database

    # 生成する馬データの件数
    N = 100

    try:
        write_log("=== 馬データ更新処理 開始 ===")
        delete_horse_database()
        write_log("既存データの削除完了")

        generate_horse_database(N)
        write_log(f"{N} 件の馬データを生成し、CSVに保存")

        insert_horse_database()
        write_log("データベースへの挿入完了")

        write_log("=== 馬データ更新処理 正常終了 ===")

    except Exception as e:
        write_log(f"エラー発生: {str(e)}")