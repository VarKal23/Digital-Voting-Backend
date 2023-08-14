import pytest
from app import schemas


def test_get_all_candidates(authorized_client, test_candidates):
    res = authorized_client.get("/candidates/")

    def validate(candidate):
        return schemas.candidateOut(**candidate)
    candidates_map = map(validate, res.json())
    candidates_list = list(candidates_map)

    assert len(res.json()) == len(test_candidates)
    assert res.status_code == 200


def test_unauthorized_user_get_all_candidates(client, test_candidates):
    res = client.get("/candidates/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_candidate(client, test_candidates):
    res = client.get(f"/candidates/{test_candidates[0].id}")
    assert res.status_code == 401


def test_get_one_candidate_not_exist(authorized_client, test_candidates):
    res = authorized_client.get(f"/candidates/88888")
    assert res.status_code == 404


def test_get_one_canddate(authorized_client, test_candidates):
    res = authorized_client.get(f"/candidates/{test_candidates[0].id}")
    candidate = schemas.candidateOut(**res.json())
    assert candidate.candidate.id == test_candidates[0].id
    assert candidate.candidate.content == test_candidates[0].content
    assert candidate.candidate.title == test_candidates[0].title


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_candidate(authorized_client, test_user, test_candidates, title, content, published):
    res = authorized_client.candidate(
        "/candidates/", json={"title": title, "content": content, "published": published})

    created_candidate = schemas.candidate(**res.json())
    assert res.status_code == 201
    assert created_candidate.title == title
    assert created_candidate.content == content
    assert created_candidate.published == published
    assert created_candidate.owner_id == test_user['id']


def test_create_candidate_default_published_true(authorized_client, test_user, test_candidates):
    res = authorized_client.candidate(
        "/candidates/", json={"title": "arbitrary title", "content": "aasdfjasdf"})

    created_candidate = schemas.candidate(**res.json())
    assert res.status_code == 201
    assert created_candidate.title == "arbitrary title"
    assert created_candidate.content == "aasdfjasdf"
    assert created_candidate.published == True
    assert created_candidate.owner_id == test_user['id']


def test_unauthorized_user_create_candidate(client, test_user, test_candidates):
    res = client.candidate(
        "/candidates/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    assert res.status_code == 401


def test_unauthorized_user_delete_candidate(client, test_user, test_candidates):
    res = client.delete(
        f"/candidates/{test_candidates[0].id}")
    assert res.status_code == 401


def test_delete_candidate_success(authorized_client, test_user, test_candidates):
    res = authorized_client.delete(
        f"/candidates/{test_candidates[0].id}")

    assert res.status_code == 204


def test_delete_candidate_non_exist(authorized_client, test_user, test_candidates):
    res = authorized_client.delete(
        f"/candidates/8000000")

    assert res.status_code == 404


def test_delete_other_user_candidate(authorized_client, test_user, test_candidates):
    res = authorized_client.delete(
        f"/candidates/{test_candidates[3].id}")
    assert res.status_code == 403


def test_update_candidate(authorized_client, test_user, test_candidates):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_candidates[0].id

    }
    res = authorized_client.put(f"/candidates/{test_candidates[0].id}", json=data)
    updated_candidate = schemas.candidate(**res.json())
    assert res.status_code == 200
    assert updated_candidate.title == data['title']
    assert updated_candidate.content == data['content']


def test_update_other_user_candidate(authorized_client, test_user, test_user2, test_candidates):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_candidates[3].id

    }
    res = authorized_client.put(f"/candidates/{test_candidates[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_candidate(client, test_user, test_candidates):
    res = client.put(
        f"/candidates/{test_candidates[0].id}")
    assert res.status_code == 401


def test_update_candidate_non_exist(authorized_client, test_user, test_candidates):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_candidates[3].id

    }
    res = authorized_client.put(
        f"/candidates/8000000", json=data)

    assert res.status_code == 404
