# FastAPI + Mangum Lambda Sample

[![Tests](https://github.com/masakaya/fastapi-mangum-lambda-sample/actions/workflows/test.yml/badge.svg)](https://github.com/masakaya/fastapi-mangum-lambda-sample/actions/workflows/test.yml)
[![Ruff](https://github.com/masakaya/fastapi-mangum-lambda-sample/actions/workflows/ruff.yml/badge.svg)](https://github.com/masakaya/fastapi-mangum-lambda-sample/actions/workflows/ruff.yml)
[![mypy](https://github.com/masakaya/fastapi-mangum-lambda-sample/actions/workflows/mypy.yml/badge.svg)](https://github.com/masakaya/fastapi-mangum-lambda-sample/actions/workflows/mypy.yml)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

FastAPI + Mangum によるAWS Lambda対応のAPIサンプル。レイヤードアーキテクチャを採用。

## アーキテクチャ

```
Controller (プレゼンテーション層)
    ↓ FastAPI Depends
Service (ビジネスロジック層)
    ↓ コンストラクタインジェクション
Repository (データアクセス層)
    ↓
In-Memory Store (※DB導入時に差し替え)
```

## プロジェクト構成

```
src/
├── main.py              # FastAPIアプリ & Lambda handler
├── controllers/         # ルーティング・リクエスト/レスポンス処理
│   └── users.py
├── services/            # ビジネスロジック
│   └── users.py
├── repositories/        # データアクセス（現在はインメモリ）
│   └── users.py
├── schemas/             # Pydantic リクエスト/レスポンススキーマ
│   └── users.py
└── models/              # ドメインモデル
    └── users.py
tests/
├── test_main.py
└── test_users.py
```

## セットアップ

```bash
# 依存関係インストール
uv sync --all-groups

# Git hooks インストール
poe setup-hooks
```

## 開発

```bash
# ローカルサーバー起動
poe dev

# Docker で起動
docker compose up

# 全チェック実行（lint + format + typecheck + test）
poe check
```

## API エンドポイント

| Method | Path | 説明 |
|--------|------|------|
| GET | `/` | ルート |
| GET | `/health` | ヘルスチェック |
| GET | `/users` | 全ユーザー取得 |
| POST | `/users` | ユーザー作成 |
| GET | `/users/{user_id}` | ユーザー取得 |

## DI 構成

FastAPI の `Depends` を使用。各コントローラー内でDIプロバイダを定義。

```python
# src/controllers/users.py
_user_repository = UserRepository()

def get_user_service() -> UserService:
    return UserService(repository=_user_repository)

@router.get("")
def get_users(service: UserService = Depends(get_user_service)):
    ...
```

## コミットルール

[Conventional Commits](https://www.conventionalcommits.org/) を採用。gitlint で自動検証。

```bash
git commit -m "feat: add user login"
git commit -m "fix: resolve memory leak"
```

## デプロイ

AWS Lambda へのデプロイ時は Mangum が ASGI アダプターとして機能する。

```python
# src/main.py
handler = Mangum(app, lifespan="off")
```
