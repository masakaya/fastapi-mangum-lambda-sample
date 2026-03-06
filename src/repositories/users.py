"""ユーザーリポジトリ (データアクセス層).

現在はインメモリ実装 (dict) を使用しており、DBは未使用。
DB導入時にはこのクラスの内部実装を差し替えることで、
上位レイヤー (Service) への影響なく永続化を実現できる。
"""

from src.models.users import User
from src.schemas.users import UserCreate


class UserRepository:
    """ユーザーデータの永続化を担うリポジトリ.

    現在はインメモリ (dict) で管理。DB導入時にこのクラスを差し替える。
    """

    def __init__(self) -> None:
        self._store: dict[int, User] = {}
        self._next_id: int = 1

    def find_all(self) -> list[User]:
        """全ユーザーを取得する."""
        return list(self._store.values())

    def find_by_id(self, user_id: int) -> User | None:
        """IDでユーザーを取得する. 存在しない場合はNoneを返す."""
        return self._store.get(user_id)

    def save(self, data: UserCreate) -> User:
        """ユーザーを保存し、採番されたIDを含むUserを返す."""
        user = User(id=self._next_id, name=data.name, email=data.email)
        self._store[user.id] = user
        self._next_id += 1
        return user
