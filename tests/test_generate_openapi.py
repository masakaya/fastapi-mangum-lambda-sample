"""generate_openapi.py の単体テスト."""

from src.main import app
from scripts.generate_openapi import add_apigateway_extensions, downgrade_openapi_31_to_30

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


class TestDowngradeOpenapi31To30:
    def test_version_is_downgraded(self) -> None:
        """OpenAPI バージョンが 3.0.x に変換されること."""
        schema = app.openapi()
        result = downgrade_openapi_31_to_30(schema)
        assert result["openapi"].startswith("3.0.")

    def test_nullable_anyof_converted(self) -> None:
        """anyOf + null が nullable に変換されること."""
        schema = {
            "openapi": "3.1.0",
            "info": {"title": "test", "version": "0.1.0"},
            "paths": {},
            "components": {
                "schemas": {
                    "Test": {
                        "properties": {
                            "field": {
                                "anyOf": [{"type": "string"}, {"type": "null"}]
                            }
                        }
                    }
                }
            },
        }
        result = downgrade_openapi_31_to_30(schema)
        field = result["components"]["schemas"]["Test"]["properties"]["field"]
        assert "anyOf" not in field
        assert field["type"] == "string"
        assert field["nullable"] is True

    def test_original_schema_not_modified(self) -> None:
        """元のスキーマが変更されないこと."""
        schema = app.openapi()
        original_version = schema["openapi"]
        downgrade_openapi_31_to_30(schema)
        assert schema["openapi"] == original_version
