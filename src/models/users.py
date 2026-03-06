"""ユーザードメインモデル.

現在DBは未使用。インメモリのデータ構造として定義している。
将来的にSQLAlchemy等のORMモデルに置き換え予定。
"""

from dataclasses import dataclass


@dataclass
class User:
    """ユーザーエンティティ."""

    id: int
    name: str
    email: str
