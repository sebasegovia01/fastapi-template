import pytest
from unittest.mock import Mock
from services.pubsub import publish_message

def test_publish_message_success(mocker):
    """Test successful message publication to Google Cloud Pub/Sub."""
    mock_publisher = mocker.patch('google.cloud.pubsub_v1.PublisherClient')
    mock_future = Mock()
    mock_future.result.return_value = None  # Simulate successful publish
    mock_publisher.return_value.publish.return_value = mock_future
    
    # Call the function
    try:
        publish_message({"id": 1, "name": "John Doe"})
        print("Test passed: Message published successfully.")
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")