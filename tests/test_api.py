import pytest
from fastapi.testclient import TestClient
import uuid


def test_create_question(client: TestClient):
    """Test creating a new question"""
    response = client.post(
        "/api/v1/questions/",
        json={"text": "What is FastAPI?"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "What is FastAPI?"
    assert "id" in data
    assert "created_at" in data


def test_get_questions(client: TestClient):
    """Test getting all questions"""
    # Create a question first
    client.post(
        "/api/v1/questions/",
        json={"text": "Test question"}
    )
    
    response = client.get("/api/v1/questions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_question_with_answers(client: TestClient):
    """Test getting a question with its answers"""
    # Create a question
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "What is Python?"}
    )
    question_id = question_response.json()["id"]
    
    # Add an answer
    user_id = str(uuid.uuid4())
    client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"user_id": user_id, "text": "Python is a programming language"}
    )
    
    # Get question with answers
    response = client.get(f"/api/v1/questions/{question_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "What is Python?"
    assert len(data["answers"]) == 1
    assert data["answers"][0]["text"] == "Python is a programming language"


def test_delete_question_cascades(client: TestClient):
    """Test that deleting a question deletes its answers"""
    # Create a question
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "To be deleted"}
    )
    question_id = question_response.json()["id"]
    
    # Add an answer
    user_id = str(uuid.uuid4())
    answer_response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"user_id": user_id, "text": "This will be deleted too"}
    )
    answer_id = answer_response.json()["id"]
    
    # Delete the question
    delete_response = client.delete(f"/api/v1/questions/{question_id}")
    assert delete_response.status_code == 204
    
    # Verify question is deleted
    get_response = client.get(f"/api/v1/questions/{question_id}")
    assert get_response.status_code == 404
    
    # Verify answer is also deleted
    answer_response = client.get(f"/api/v1/answers/{answer_id}")
    assert answer_response.status_code == 404


def test_cannot_create_answer_for_nonexistent_question(client: TestClient):
    """Test that creating an answer for a non-existent question fails"""
    user_id = str(uuid.uuid4())
    response = client.post(
        "/api/v1/questions/99999/answers/",
        json={"user_id": user_id, "text": "This should fail"}
    )
    assert response.status_code == 404


def test_empty_text_validation(client: TestClient):
    """Test validation for empty text fields"""
    # Empty question text
    response = client.post(
        "/api/v1/questions/",
        json={"text": ""}
    )
    assert response.status_code == 422
    
    # Empty answer text
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Valid question"}
    )
    question_id = question_response.json()["id"]
    
    user_id = str(uuid.uuid4())
    response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"user_id": user_id, "text": ""}
    )
    assert response.status_code == 422


def test_invalid_user_id(client: TestClient):
    """Test validation for invalid user_id format"""
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Valid question"}
    )
    question_id = question_response.json()["id"]
    
    response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"user_id": "not-a-uuid", "text": "Valid answer"}
    )
    assert response.status_code == 422