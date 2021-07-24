from typing import Dict, Any

import pytest

from fastapi.testclient import TestClient

from application import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


class TestPostsUsers:
    @pytest.mark.parametrize(
        'endpoint',
        [
            '/posts',
            '/users',
        ]
    )
    def test_list(
            self,
            client: TestClient,
            endpoint: str,
    ):
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.json() is not []

    @pytest.mark.parametrize(
        'endpoint, data, test_data',
        [
            (
                '/posts/new',
                {'title': 'Test title', 'body': 'Test body', 'userId': 1},
                {'title': 'Test title', 'body': 'Test body'}
            ),
            (
                '/users/new',
                {'name': 'John Test', 'username': 'John_Test', 'email': 'test@example.com', 'phone': '1234567890'},
                {'name': 'John Test', 'username': 'John_Test', 'email': 'test@example.com', 'phone': '1234567890'}
            )
        ]
    )
    def test_create(
            self,
            client: TestClient,
            endpoint: str,
            data: Dict[str, Any],
            test_data: Dict[str, Any],
    ):
        response = client.post(endpoint, json=data)
        assert response.status_code == 201
        response_data = response.json()
        assert 'id' in response_data
        for key in test_data:
            assert test_data[key] in response_data[key]


class TestPost:
    @pytest.mark.parametrize(
        'post_id',
        [
            1,
            2,
            3,
        ]
    )
    def test_single_post(
            self,
            client: TestClient,
            post_id: int,
    ):
        response = client.get(f'/posts/{post_id}')
        assert response.status_code == 200
        post = response.json()
        assert post['id'] == post_id

    @pytest.mark.parametrize(
        'post_id, edited_data',
        [
            (
                1,
                {'title': 'Edited Title', 'body': 'Edited body'}
            ),
            (
                2,
                {'title': 'Edited Title', 'body': 'Edited body'}
            ),
            (
                3,
                {'title': 'Edited Title', 'body': 'Edited body'}
            ),
        ]
    )
    def test_edit_post(
            self,
            client: TestClient,
            post_id: int,
            edited_data: Dict[str, Any]
    ):
        response = client.patch(f'/posts/{post_id}/edit', json=edited_data)
        assert response.status_code == 200
        post = response.json()
        assert 'id' in post
        for key in edited_data:
            assert edited_data[key] == post[key]


class TestUser:
    @pytest.mark.parametrize(
        'data',
        [
            {'name': 'John Test', 'username': 'John_Test', 'email': 'john@example.com', 'phone': '1234567890'}
        ]
    )
    def test_create_user(
            self,
            client: TestClient,
            data: Dict[str, Any],
    ):
        response = client.post('/users/new', json=data)
        assert response.status_code == 201
        user = response.json()
        for key in data:
            assert data[key] == user[key]
