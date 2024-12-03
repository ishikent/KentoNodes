from pathlib import Path
import os

def get_root_path():
    # 環境変数 STORAGE_DIR を取得
    storage_dir = os.environ.get("STORAGE_DIR")

    # STORAGE_DIR が未設定の場合のチェック
    if storage_dir is None:
        raise ValueError("Environment variable 'STORAGE_DIR' is not set.")

    # Path オブジェクトを作成
    root_path = Path(storage_dir)

    # 指定されたパスが存在するか確認
    if root_path.exists():
        return root_path
    else:
        raise FileNotFoundError(f"The path '{root_path}' does not exist.")
