def test_get_activities_includes_activity(client, activity):
    # Arrange
    activity_name, details = activity

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()[activity_name] == details


def test_signup_adds_participant(client, activity):
    # Arrange
    activity_name, details = activity
    email = "new-student@example.com"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in details["participants"]


def test_signup_rejects_duplicate_participant(client, activity):
    # Arrange
    activity_name, details = activity
    email = "registered@example.com"
    participants_before = details["participants"].copy()

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is already signed up for this activity"
    }
    assert details["participants"] == participants_before


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "student@example.com"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant(client, activity):
    # Arrange
    activity_name, details = activity
    email = "registered@example.com"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in details["participants"]


def test_unregister_rejects_nonparticipant(client, activity):
    # Arrange
    activity_name, details = activity
    email = "not-registered@example.com"
    participants_before = details["participants"].copy()

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }
    assert details["participants"] == participants_before


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": "student@example.com"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}