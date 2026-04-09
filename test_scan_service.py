import pytest
from unittest.mock import Mock, MagicMock
from scan_service import ScanService

@pytest.fixture
def mock_db_connection():
    mock_col = MagicMock()
    return mock_col

@pytest.fixture
def scan_service(mock_db_connection):
    return ScanService(db_collection=mock_db_connection)

# Test 1: Basic functionality test
def test_analyze_returns_correct_dict():
    service = ScanService(db_collection=None)
    result = service.analyze_and_save("img_001", b"fake_bytes")
    assert result["label"] == "benign"
    assert result["confidence"] == 0.98

# Test 2: Using Fixtures