"""ユーザー関連のリクエスト/レスポンススキーマ."""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """ユーザー作成リクエスト."""

    name: str
    email: str


class UserResponse(BaseModel):
    """ユーザーレスポンス."""

    id: int
    name: str
    email: str
