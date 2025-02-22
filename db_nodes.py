import duckdb


class Artist_Queue:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "query": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def __init__(self, query):
        self.counter = self.query_row_by_row(query)
        self.con = duckdb.connect(database=":memory:")  # インメモリDBを作成
        self.con.execute("ATTACH 'artist_name.db' AS artists")  # 既存のDBをアタッチ

    def run(self, text, seed=None):
        try:
            row = next(self.counter)
            return (row,)
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
