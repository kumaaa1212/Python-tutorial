from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://fastapiuser:fastapipass@0.0.0.0:5555/fleamarket"
# 0.0.0.0:5432はipアドレスとポート番号を指定している
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# engineとはどのデータベースにどのように接続するかを書いているもの

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SessionLocalはデータベースへのセッションを作成するためのクラス
# データベースセッションとは、データベースの操作を行うための一連の処理をまとめたもの
# autocommitがfalseなので明示的に反映される必要がある
# autoflushは一時的にクエリの結果を反映されるかの設定→コミットした段階で永続的に反映される様にしている
# bindはどのでーたべーすに接続するかを指定している

Base = declarative_base()
# 新しいデータベースモデルを定義するためのクラスを作成するためのクラス

# sqlalchemyのモデルとは、sqlテーブルをpythonのクラスとして表現したもの
