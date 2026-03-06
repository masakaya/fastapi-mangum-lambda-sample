"""ユーザーサービス (ビジネスロジック層)."""

from fastapi import HTTPException

from src.models.users import User
from src.repositories.users import UserRepository
from src.schemas.users import UserCreate


class UserService:
    """ユーザーに関するビジネスロジックを提供する."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def get_all(self) -> list[User]:
        """全ユーザーを取得する."""
        return self.repository.find_all()

    def get_by_id(self, user_id: int) -> User:
        """IDでユーザーを取得する. 存在しない場合は404."""
        user = self.repository.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def create(self, data: UserCreate) -> User:
        """ユーザーを作成する."""
        return self.repository.save(data)
