from fastapi.testclient import TestClient


def test_root_redirect(client: TestClient):
    # Arrange: client fixture provided by conftest
    # Act (don't follow redirects so status code is exposed)
    response = client.get("/", follow_redirects=False)
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client: TestClient):
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_already(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already in the default participants
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400


def test_signup_not_found(client: TestClient):
    # Arrange
    # Act
    response = client.post("/activities/NoSuchActivity/signup", params={"email": "a@b.com"})
    # Assert
    assert response.status_code == 404


def test_remove_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/remove", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"


def test_remove_not_signed(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "nobody@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/remove", params={"email": email})
    # Assert
    assert response.status_code == 400


def test_remove_not_found(client: TestClient):
    # Arrange
    # Act
    response = client.post("/activities/NoSuchActivity/remove", params={"email": "a@b.com"})
    # Assert
    assert response.status_code == 404
