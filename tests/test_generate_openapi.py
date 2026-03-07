"""generate_openapi.py の単体テスト."""

from src.main import app
from scripts.generate_openapi import add_apigateway_extensions

DUMMY_ARN = "arn:aws:lambda:ap-northeast-1:123456789012:function:my-func"


class TestAddApigatewayExtensions:
    def test_all_paths_have_integration(self) -> None:
        """全パス・メソッドに x-amazon-apigateway-integration が付与される."""
        schema = app.openapi()
        result = add_apigateway_extensions(schema, DUMMY_ARN)

        for path, methods in result["paths"].items():
            for method, operation in methods.items():
                if method in ("get", "post", "put", "delete", "patch"):
                    assert "x-amazon-apigateway-integration" in operation, (
                        f"{method.upper()} {path} に integration がない"
                    )

    def test_integration_type_is_aws_proxy(self) -> None:
        """integration type が aws_proxy であること."""
        schema = app.openapi()
        result = add_apigateway_extensions(schema, DUMMY_ARN)

        integration = result["paths"]["/"]["get"]["x-amazon-apigateway-integration"]
        assert integration["type"] == "aws_proxy"
        assert integration["httpMethod"] == "POST"

    def test_integration_uri_contains_lambda_arn(self) -> None:
        """integration URI に Lambda ARN が含まれること."""
        schema = app.openapi()
        result = add_apigateway_extensions(schema, DUMMY_ARN)

        integration = result["paths"]["/"]["get"]["x-amazon-apigateway-integration"]
        assert DUMMY_ARN in integration["uri"]

    def test_original_schema_is_not_modified(self) -> None:
        """元のスキーマが変更されないこと."""
        schema = app.openapi()
        original_keys = set(schema["paths"]["/"]["get"].keys())

        add_apigateway_extensions(schema, DUMMY_ARN)

        assert set(schema["paths"]["/"]["get"].keys()) == original_keys

    def test_region_extracted_from_arn(self) -> None:
        """ARN からリージョンが正しく抽出されること."""
        schema = app.openapi()
        result = add_apigateway_extensions(schema, DUMMY_ARN)

        integration = result["paths"]["/"]["get"]["x-amazon-apigateway-integration"]
        assert "ap-northeast-1" in integration["uri"]
