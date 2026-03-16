from src.app import activities

def test_signup_duplicate(client):
    # Arrange
    email = "dup@student.edu"
    activity = "Soccer Team"
    client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email={email}")  # First signup

    # Act
    response = client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "already signed up" in result["detail"]

def test_signup_activity_full(client):
    # Arrange
    activity = "Chess Club"
    max_p = activities[activity]["max_participants"]
    current = len(activities[activity]["participants"])
    for i in range(max_p - current):
        client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email=fill{i}@student.edu")

    # Act
    response = client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email=full@student.edu")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "full" in result["detail"]

def test_unregister_not_registered(client):
    # Arrange
    email = "notreg@student.edu"
    activity = "Soccer Team"

    # Act
    response = client.post(f"/activities/{activity.replace(' ', '%20')}/unregister?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "not registered" in result["detail"]

def test_capacity_boundary(client):
    # Arrange - Test exactly at max capacity
    activity = "Basketball Club"  # max 15, starts empty
    for i in range(14):  # Leave one spot
        client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email=user{i}@student.edu")

    # Act - Should succeed
    response = client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email=last@student.edu")

    # Assert
    assert response.status_code == 200
    assert len(activities[activity]["participants"]) == 15

    # Now full
    response2 = client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email=extra@student.edu")
    assert response2.status_code == 400