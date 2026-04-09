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
@pytest.fixture
def scan_service_broken():
    return ScanService(db_collection=None)

def test_analyze_with_fixture(scan_service_broken):
    result = scan_service_broken.analyze_and_save("img_002", b"fake_bytes")
    assert result["label"] == "benign"

# Test 3: Database Save Verification
def test_analyze_saves_to_database(scan_service, mock_db_connection):
    img_id = "scan_123"
    img_bytes = b"data"

    result = scan_service.analyze_and_save(img_id, img_bytes)

    mock_db_connection.insert_one.assert_called_once()
    expected_document = {
        "_id": img_id,
        "result": {"label": "benign", "confidence": 0.98},
        "status": "processed"
    }
    mock_db_connection.insert_one.assert_called_with(expected_document)

# Test 4: Error Handling Test
def test_analyze_handles_database_insert_error(scan_service, mock_db_connection):
    mock_db_connection.insert_one.side_effect = Exception("MongoDB Connection Timeout")
       
    with pytest.raises(Exception, match="Connection Timeout"):
        scan_service.analyze_and_save("scan_456", b"data")
        
    mock_db_connection.insert_one.assert_called_once()

# Test 5: Input Validation Test
def test_analyze_raises_error_on_empty_data(scan_service):
    with pytest.raises(ValueError, match="Image data cannot be empty"):
        scan_service.analyze_and_save("scan_789", b"")    