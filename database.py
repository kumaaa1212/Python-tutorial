from sqlalchemy import create_engine
from config import get_settings
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLALCHEMY_DATABASE_URL = "postgresql://fastapiuser:fastapipass@0.0.0.0:5555/fleamarket"
SQLALCHEMY_DATABASE_URL = get_settings().sqlalchemy_database_url

# 0.0.0.0:5432はipアドレスとポート番号を指定している
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# engineとはどのデータベースにどのように接続するかを書いているもの

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SessionLocalはデータベースへのセッションを作成するためのクラス
# データベースセッションとは、データベースの操作を行うための一連の処理をまとめたもの
# autocommitがfalseなので明示的に反映される必要がある
# autoflushは一時的にクエリの結果を反映されるかの設定→コミットした段階で永続的に反映される様にしている
# bindはどのでーたべーすに接続するかを指定している

# 新しいデータベースモデルを定義するためのクラスを作成するためのベースのクラスを作成
# このベースクラスを継承して新しいデータベースモデルを作成することで、データベースモデルを定義することができる
Base = declarative_base()

# sqlalchemyのモデルとは、sqlテーブルをpythonのクラスとして表現したもの


# データベースへのセッションを取得する関数
def get_db():
    # データベースへのセッションを初期化
    db = SessionLocal()
    try:
        # yieldを使うと、レスポンスを返した後に処理を続けることができる
        yield db
    finally:
        db.close()
