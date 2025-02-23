import duckdb
import os

class Artist_Queue:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT:seed", {}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def __init__(self):
        self.con = duckdb.connect()  # インメモリDBを作成
        query = "SELECT tag_string_artist FROM read_parquet('/Comfy_Share/storage/db/artist_name.parquet')"
        self.cursor_file = "/Comfy_Share/storage/db/last_processed_index.txt"  # カーソル情報のファイルパス
        self.counter = self.query_row_by_row(query)

    def run(self, seed=None):
        try:
            row = next(self.counter)
            return (row[0],)
        except StopIteration:
            self.con.close()  # ジェネレータが終了した後に接続を閉じる
            return ("No more rows",)


    def query_row_by_row(self, query):
        result = self.con.execute(query)

        # 最後に処理した行番号を取得（存在しなければ0）
        last_index = self.get_last_processed_index()

        index = 0  # 行番号を保持
        while True:
            row = result.fetchone()  # 1行ずつ取得
            if row is None:
                break

            if index > last_index:
                # 行を返す前にインデックスを保存
                self.save_last_processed_index(index)

                yield row  # 行を返す

            index += 1


    def get_last_processed_index(self):
        """最後に処理した行番号を取得。ファイルがない場合は0を返す。"""
        if os.path.exists(self.cursor_file):
            with open(self.cursor_file, "r") as f:
                return int(f.read().strip())
        else:
            # ファイルが存在しない場合、新規作成して0を記録
            self.save_last_processed_index(-1)
            return -1

    def save_last_processed_index(self, index):
        """処理した行番号をファイルに保存"""
        with open(self.cursor_file, "w") as f:
            f.write(str(index))

# NODEクラスマッピング
NODE_CLASS_MAPPINGS = {
  "Artist_Queue": Artist_Queue,
}
