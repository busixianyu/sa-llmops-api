import pytest

from pkg.response.http_code import HttpCode


class TestAppHandler:

    @pytest.mark.parametrize("app_id, query", [
        ("e41fb663-2aff-4b5f-9076-fe7afd467cb0", None),
        ("e41fb663-2aff-4b5f-9076-fe7afd467cb0", "你好，你是?")
    ])
    def test_completion(self, app_id, query, client):
        response = client.post(f"/app/{app_id}/debug", json={"query": query})
        assert response.status_code == 200
        if query is None:
            assert response.json.get("code") == HttpCode.VALIDATE_ERROR
        else:
            assert response.json.get("code") == HttpCode.SUCCESS
        # print(response.json.get("data"))
