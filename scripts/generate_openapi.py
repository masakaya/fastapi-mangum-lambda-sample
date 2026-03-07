"""FastAPI の OpenAPI スキーマに API Gateway 拡張を付与して出力する.

使い方:
    LAMBDA_ARN=arn:aws:lambda:... uv run python scripts/generate_openapi.py > openapi.json
"""

import json
import os
import sys
from copy import deepcopy
from pathlib import Path

# プロジェクトルートを PYTHONPATH に追加
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.main import app  # noqa: E402


def add_apigateway_extensions(schema: dict, lambda_arn: str) -> dict:
    """各パス・メソッドに x-amazon-apigateway-integration を付与する."""
    schema = deepcopy(schema)

    integration = {
        "type": "aws_proxy",
        "httpMethod": "POST",
        "uri": f"arn:aws:apigateway:{_get_region(lambda_arn)}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations",
        "passthroughBehavior": "when_no_match",
    }

    for _path, methods in schema.get("paths", {}).items():
        for method, _operation in list(methods.items()):
            if method in ("get", "post", "put", "delete", "patch", "options", "head"):
                methods[method]["x-amazon-apigateway-integration"] = integration

    return schema


def _get_region(lambda_arn: str) -> str:
    """Lambda ARN からリージョンを抽出する."""
    # arn:aws:lambda:<region>:<account>:function:<name>
    parts = lambda_arn.split(":")
    if len(parts) >= 4:
        return parts[3]
    return os.environ.get("AWS_REGION", "ap-northeast-1")


def main() -> None:
    lambda_arn = os.environ.get("LAMBDA_ARN")
    if not lambda_arn:
        print("Error: LAMBDA_ARN environment variable is required", file=sys.stderr)
        sys.exit(1)

    schema = app.openapi()
    schema = add_apigateway_extensions(schema, lambda_arn)

    json.dump(schema, sys.stdout, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
