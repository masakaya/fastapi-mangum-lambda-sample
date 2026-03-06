"""ユーザーコントローラー (プレゼンテーション層).

HTTPリクエスト/レスポンスの処理のみを担当し、
ビジネスロジックは Service 層に委譲する。
"""

from fastapi import APIRouter, Depends

from src.repositories.users import UserRepository
from src.schemas.users import UserCreate, UserResponse
from src.services.users import UserService

router = APIRouter(prefix="/users", tags=["users"])

_user_repository = UserRepository()


def get_user_service() -> UserService:
    """UserService のインスタンスを返す."""
    return UserService(repository=_user_repository)


@router.get("", response_model=list[UserResponse])
def get_users(service: UserService = Depends(get_user_service)) -> list[UserResponse]:
    """全ユーザーを取得する."""
    return [UserResponse(id=u.id, name=u.name, email=u.email) for u in service.get_all()]


@router.post("", response_model=UserResponse, status_code=201)
def create_user(
    body: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """ユーザーを作成する."""
    user = service.create(body)
    return UserResponse(id=user.id, name=user.name, email=user.email)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """指定IDのユーザーを取得する."""
    user = service.get_by_id(user_id)
    return UserResponse(id=user.id, name=user.name, email=user.email)
