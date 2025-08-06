import pytest

from pkg.http_code import HttpCode


class TestAppHandler:

    @pytest.mark.parametrize("query", ["你好", None])
    def test_completion(self,query, client):
        response = client.post("/app/completion", json={"query":query})
        assert response.status_code == 200
        if query is None:
            assert response.json.get("code") == HttpCode.VALIDATE_ERROR
        else:
            assert response.json.get("code") == HttpCode.SUCCESS
        print(response.json.get("data"))

