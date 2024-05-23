import pytest
from unittest.mock import Mock, patch
from services.pubsub import publish_message

def test_publish_message_failure(mocker):
    """Test failure in message publication to Google Cloud Pub/Sub."""
    mock_publisher = mocker.patch('google.cloud.pubsub_v1.PublisherClient')
    mock_future = Mock()
    mock_future.result.side_effect = Exception("Publish failed")  # Simulate failure in publish
    mock_publisher.return_value.publish.return_value = mock_future
    
    # Call the function expecting it to handle the failure
    try:
        publish_message({"id": 2, "name": "Jane Doe"})
        print("Test passed: Handled publish failure.")
    except Exception:
        pytest.fail("Test failed: Did not handle the exception properly.")

def test_publish_message_exception_handling(capsys):
    """
    Test the exception handling in the publish_message function when publishing fails.
    """
    with patch('google.cloud.pubsub_v1.PublisherClient.publish', new_callable=Mock) as mock_publish:
        # Configure the mock to raise an exception when called
        mock_publish.side_effect = Exception("Test exception")

        # Call the function with data that triggers the exception
        publish_message({"test": "data"})

        captured = capsys.readouterr()

        # Check if the error message was printed as expected
        assert "Error posting message: Test exception" in captured.out or captured.err

        # Ensure the publish method was called, indicating that the function attempted to publish
        mock_publish.assert_called_once()