"""Tests for the FastAPI application."""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that /activities returns all available activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert len(data) == 9

    def test_get_activities_has_correct_structure(self, client):
        """Test that activity objects have the correct structure."""
        response = client.get("/activities")
        data = response.json()
        activity = data["Chess Club"]
        
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_get_activities_includes_participants(self, client):
        """Test that activities include their current participants."""
        response = client.get("/activities")
        data = response.json()
        
        chess_club = data["Chess Club"]
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_for_activity_success(self, client):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds the participant to the activity."""
        client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        
        response = client.get("/activities")
        data = response.json()
        assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]

    def test_signup_for_nonexistent_activity(self, client):
        """Test that signup fails for nonexistent activity."""
        response = client.post(
            "/activities/Nonexistent%20Activity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_student(self, client):
        """Test that a student cannot sign up for the same activity twice."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_multiple_students(self, client):
        """Test that multiple different students can sign up."""
        client.post(
            "/activities/Chess%20Club/signup?email=student1@mergington.edu"
        )
        client.post(
            "/activities/Chess%20Club/signup?email=student2@mergington.edu"
        )
        
        response = client.get("/activities")
        data = response.json()
        participants = data["Chess Club"]["participants"]
        
        assert "student1@mergington.edu" in participants
        assert "student2@mergington.edu" in participants
        assert len(participants) == 4  # 2 original + 2 new


class TestUnregisterFromActivity:
    """Tests for the POST /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, client):
        """Test successful unregister from an activity."""
        response = client.post(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
        assert "michael@mergington.edu" in data["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes the participant."""
        client.post(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        
        response = client.get("/activities")
        data = response.json()
        assert "michael@mergington.edu" not in data["Chess Club"]["participants"]
        assert len(data["Chess Club"]["participants"]) == 1

    def test_unregister_nonexistent_activity(self, client):
        """Test that unregister fails for nonexistent activity."""
        response = client.post(
            "/activities/Nonexistent%20Activity/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_not_registered_student(self, client):
        """Test that unregister fails for student not registered in activity."""
        response = client.post(
            "/activities/Chess%20Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]

    def test_unregister_multiple_participants(self, client):
        """Test unregistering one of multiple participants."""
        # First, add a new participant
        client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        
        # Unregister one
        client.post(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        
        response = client.get("/activities")
        data = response.json()
        participants = data["Chess Club"]["participants"]
        
        assert "michael@mergington.edu" not in participants
        assert "daniel@mergington.edu" in participants
        assert "newstudent@mergington.edu" in participants
        assert len(participants) == 2


class TestSignupAndUnregisterFlow:
    """Integration tests for signup and unregister flows."""

    def test_signup_then_unregister(self, client):
        """Test signing up and then unregistering."""
        # Sign up
        response1 = client.post(
            "/activities/Basketball/signup?email=testuser@mergington.edu"
        )
        assert response1.status_code == 200
        
        # Verify signup
        response2 = client.get("/activities")
        assert "testuser@mergington.edu" in response2.json()["Basketball"]["participants"]
        
        # Unregister
        response3 = client.post(
            "/activities/Basketball/unregister?email=testuser@mergington.edu"
        )
        assert response3.status_code == 200
        
        # Verify unregister
        response4 = client.get("/activities")
        assert "testuser@mergington.edu" not in response4.json()["Basketball"]["participants"]

    def test_signup_unregister_can_signup_again(self, client):
        """Test that a student can sign up again after unregistering."""
        email = "testuser@mergington.edu"
        
        # Sign up
        response1 = client.post(
            f"/activities/Basketball/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Unregister
        response2 = client.post(
            f"/activities/Basketball/unregister?email={email}"
        )
        assert response2.status_code == 200
        
        # Sign up again
        response3 = client.post(
            f"/activities/Basketball/signup?email={email}"
        )
        assert response3.status_code == 200
        
        # Verify they're registered
        response4 = client.get("/activities")
        assert email in response4.json()["Basketball"]["participants"]
