from src.app import activities

def test_signup_invalid_activity(client):
    # Arrange
    email = "test@student.edu"
    invalid_activity = "Nonexistent Activity"

    # Act
    response = client.post(f"/activities/{invalid_activity.replace(' ', '%20')}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "not found" in result["detail"]

def test_unregister_invalid_activity(client):
    # Arrange
    email = "test@student.edu"
    invalid_activity = "Nonexistent Activity"

    # Act
    response = client.post(f"/activities/{invalid_activity.replace(' ', '%20')}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "not found" in result["detail"]

def test_signup_empty_email(client):
    # Arrange - Outlier: empty email
    email = ""
    activity = "Soccer Team"

    # Act
    response = client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "Invalid email" in result["detail"]

def test_signup_long_email(client):
    # Arrange - Outlier: very long email (over 254 chars)
    email = "a" * 250 + "@student.edu"  # Total length > 254
    activity = "Soccer Team"

    # Act
    response = client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "Invalid email" in result["detail"]

def test_signup_special_chars_email(client):
    # Arrange - Outlier: email with special chars
    email = "test<script>@student.edu"
    activity = "Soccer Team"

    # Act
    response = client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "Invalid email" in result["detail"]

def test_unregister_invalid_email(client):
    # Arrange
    email = "invalid"
    activity = "Soccer Team"

    # Act
    response = client.post(f"/activities/{activity.replace(' ', '%20')}/unregister?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "Invalid email" in result["detail"]

def test_response_data_structure(client):
    # Arrange - Test data validation in response

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for activity, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)
        assert details["max_participants"] > 0
        # Validate participants are strings (basic data validation)
        for participant in details["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email check