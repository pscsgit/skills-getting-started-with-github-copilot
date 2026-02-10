"""Pytest configuration and fixtures for testing the FastAPI application."""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    from app import activities
    
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball": {
            "description": "Team sport focusing on basketball skills and competition",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Soccer": {
            "description": "Outdoor soccer league for all skill levels",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 22,
            "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore scientific concepts through experiments and projects",
            "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu", "rachel@mergington.edu"]
        },
        "Art Class": {
            "description": "Learn painting, drawing, and other visual arts techniques",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Band": {
            "description": "Play in the school band and perform at events",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["noah@mergington.edu", "charlotte@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Reset after test
    activities.clear()
    activities.update(original_activities)
