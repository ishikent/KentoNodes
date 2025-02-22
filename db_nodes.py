import duckdb


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
        query = "SELECT tag_string_artist FROM read_parquet('/mnt/ssd2/home/Data/Comfy_Data/storage/db/artist_name.parquet')"
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
        while True:
            row = result.fetchone()  # 1行ずつ取得
            if row is None:
                break
            yield row  # 行を返す


NODE_CLASS_MAPPINGS = {
  "Artist_Queue":Artist_Queue,
}