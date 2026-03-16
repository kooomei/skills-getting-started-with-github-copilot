from src.app import activities

def test_get_activities(client):
    # Arrange - No special setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_success(client):
    # Arrange
    email = "new@student.edu"
    activity = "Soccer Team"

    # Act
    response = client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert email in activities[activity]["participants"]

def test_unregister_success(client):
    # Arrange
    email = "unreg@student.edu"
    activity = "Soccer Team"
    client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email={email}")  # Sign up first

    # Act
    response = client.post(f"/activities/{activity.replace(' ', '%20')}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert email not in activities[activity]["participants"]