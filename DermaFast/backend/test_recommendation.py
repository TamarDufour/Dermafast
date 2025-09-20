import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.auth import AuthService

# Mock AuthService.get_current_user to bypass authentication for tests
async def override_get_current_user():
    return {"national_id": "test_user"}

app.dependency_overrides[AuthService.get_current_user] = override_get_current_user

client = TestClient(app)

# Mock Supabase client
mock_supabase_client = MagicMock()

@pytest.fixture(autouse=True)
def override_supabase_client():
    with patch('backend.app.main.supabase', mock_supabase_client):
        yield

def test_recommendation_plastic_surgeon_high_cnn():
    # Mock Supabase responses
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = MagicMock(error=None)
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.side_effect = [
        MagicMock(data=[{"cnn_result": 0.5}]), # High CNN result
        MagicMock(data=[{"q1": False, "q2": False, "q3": False, "q4": False, "q5": False}]), # 0 yes answers
    ]
    mock_supabase_client.table.return_value.select.return_value.in_.return_value.eq.return_value.execute.return_value = MagicMock(data=[]) # No melanoma selected

    response = client.post("/api/save_similar_moles", json={"selected_ids": ["img1"]})

    assert response.status_code == 200
    data = response.json()
    assert "plastic surgeon" in data["recommendation"]

def test_recommendation_plastic_surgeon_many_yes_answers():
    # Mock Supabase responses
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = MagicMock(error=None)
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.side_effect = [
        MagicMock(data=[{"cnn_result": 0.1}]), # Low CNN result
        MagicMock(data=[{"q1": True, "q2": True, "q3": False, "q4": False, "q5": False}]), # 2 yes answers
    ]
    mock_supabase_client.table.return_value.select.return_value.in_.return_value.eq.return_value.execute.return_value = MagicMock(data=[]) # No melanoma selected

    response = client.post("/api/save_similar_moles", json={"selected_ids": ["img1"]})

    assert response.status_code == 200
    data = response.json()
    assert "plastic surgeon" in data["recommendation"]

def test_recommendation_plastic_surgeon_melanoma_selection():
    # Mock Supabase responses
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = MagicMock(error=None)
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.side_effect = [
        MagicMock(data=[{"cnn_result": 0.1}]), # Low CNN result
        MagicMock(data=[{"q1": False, "q2": False, "q3": False, "q4": False, "q5": False}]), # 0 yes answers
    ]
    mock_supabase_client.table.return_value.select.return_value.in_.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"dx": "mel"}]) # Melanoma selected

    response = client.post("/api/save_similar_moles", json={"selected_ids": ["img1"]})

    assert response.status_code == 200
    data = response.json()
    assert "plastic surgeon" in data["recommendation"]

def test_recommendation_dermatologist_medium_cnn():
    # Mock Supabase responses
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = MagicMock(error=None)
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.side_effect = [
        MagicMock(data=[{"cnn_result": 0.3}]), # Medium CNN result
        MagicMock(data=[{"q1": False, "q2": False, "q3": False, "q4": False, "q5": False}]), # 0 yes answers
    ]
    mock_supabase_client.table.return_value.select.return_value.in_.return_value.eq.return_value.execute.return_value = MagicMock(data=[]) # No melanoma selected

    response = client.post("/api/save_similar_moles", json={"selected_ids": ["img1"]})

    assert response.status_code == 200
    data = response.json()
    assert "dermatologist" in data["recommendation"]
    assert "plastic surgeon" not in data["recommendation"]

def test_recommendation_dermatologist_one_yes_answer():
    # Mock Supabase responses
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = MagicMock(error=None)
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.side_effect = [
        MagicMock(data=[{"cnn_result": 0.1}]), # Low CNN result
        MagicMock(data=[{"q1": True, "q2": False, "q3": False, "q4": False, "q5": False}]), # 1 yes answer
    ]
    mock_supabase_client.table.return_value.select.return_value.in_.return_value.eq.return_value.execute.return_value = MagicMock(data=[]) # No melanoma selected

    response = client.post("/api/save_similar_moles", json={"selected_ids": ["img1"]})

    assert response.status_code == 200
    data = response.json()
    assert "dermatologist" in data["recommendation"]
    assert "plastic surgeon" not in data["recommendation"]

def test_recommendation_monitoring():
    # Mock Supabase responses
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = MagicMock(error=None)
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.side_effect = [
        MagicMock(data=[{"cnn_result": 0.1}]), # Low CNN result
        MagicMock(data=[{"q1": False, "q2": False, "q3": False, "q4": False, "q5": False}]), # 0 yes answers
    ]
    mock_supabase_client.table.return_value.select.return_value.in_.return_value.eq.return_value.execute.return_value = MagicMock(data=[]) # No melanoma selected

    response = client.post("/api/save_similar_moles", json={"selected_ids": ["img1"]})

    assert response.status_code == 200
    data = response.json()
    assert "continue monitoring" in data["recommendation"]

def test_recommendation_plastic_surgeon_cnn_exact_0_4():
    # Mock Supabase responses
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = MagicMock(error=None)
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.side_effect = [
        MagicMock(data=[{"cnn_result": 0.4}]), # CNN result exactly 0.4
        MagicMock(data=[{"q1": False, "q2": False, "q3": False, "q4": False, "q5": False}]), # 0 yes answers
    ]
    mock_supabase_client.table.return_value.select.return_value.in_.return_value.eq.return_value.execute.return_value = MagicMock(data=[]) # No melanoma selected

    response = client.post("/api/save_similar_moles", json={"selected_ids": ["img1"]})

    assert response.status_code == 200
    data = response.json()
    assert "plastic surgeon" in data["recommendation"]
