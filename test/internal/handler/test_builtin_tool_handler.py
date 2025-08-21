import pytest

from pkg.response import HttpCode


class TestBuiltinToolHandler:


    def test_get_categories(self, client):
        resp = client.get("builtin-tool/categories")
        assert resp.status_code == 200
        assert resp.json["code"] == HttpCode.SUCCESS
        assert len(resp.json["data"]) > 0

    def test_get_builtin_tools(self, client):
        resp = client.get("builtin-tool")
        assert resp.status_code == 200
        assert resp.json["code"] == HttpCode.SUCCESS
        assert len(resp.json["data"]) > 0

    @pytest.mark.parametrize("provider_name, tool_name", [
        ("google", "google_serper"),
    ])
    def test_get_provider_tool(self, provider_name, tool_name, client):
        resp = client.get(f"builtin-tool/{provider_name}/tool/{tool_name}")
        assert resp.status_code == 200
        assert resp.json["code"] == HttpCode.SUCCESS
