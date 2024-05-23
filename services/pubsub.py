# Import necessary libraries from Google Cloud SDK and Python standard libraries.
from google.cloud import pubsub_v1
from google.oauth2.service_account import Credentials
from os import getenv, path
from dotenv import load_dotenv

# Load environment variables from a .env file.
load_dotenv()

# Retrieve Google Cloud Platform project ID and Pub/Sub topic ID from environment variables,
# providing default values if not set.
project_id = getenv("GCP_PROJECT_ID", "your-gcp-project-id")
topic_id = getenv("PUBSUB_TOPIC_ID", "my-new-topic")
gcp_credentials = getenv("GCP_CREDENTIALS")

# Construct the full path to the service account credentials file,
# assuming it's located two directories above the current file.
credentials_path = path.join(path.dirname(path.dirname(__file__)), gcp_credentials)

# Initialize the Credentials object from a service account file which allows
# the application to authenticate and interact with Google Cloud services.
credentials = Credentials.from_service_account_file(credentials_path)

# Create a PublisherClient with the credentials, which is used to publish messages to Pub/Sub topics.
publisher = pubsub_v1.PublisherClient(credentials=credentials)

# Construct the full path for the Pub/Sub topic which identifies where messages should be published.
topic_path = publisher.topic_path(project_id, topic_id)

def publish_message(data: any) -> None:
    """
    Publishes a message to a specified Google Cloud Pub/Sub topic.
    
    Parameters:
    - data (any): The data to be sent to the Pub/Sub topic. This data can be of any type that can be converted to a string.
    
    Returns:
    - None: This function does not return anything but prints the result to the console.

    The function converts the input data to a string, then encodes it to bytes as required by the Pub/Sub API.
    It then publishes the bytes to the configured Pub/Sub topic. If successful, it prints a confirmation message.
    If an exception occurs during publishing, it catches the exception and prints an error message.
    """
    # Convert the input data to a string representation.
    data_str = str(data)
    # Encode the string data to bytes, as required by the Google Pub/Sub API.
    data_bytes = data_str.encode("utf-8")

    try:
        # Attempt to publish the bytes data to the Pub/Sub topic and wait for the result.
        publish_future = publisher.publish(topic_path, data_bytes)
        publish_future.result()  # Wait for the publish to complete.
        print(f"Posted message to topic: {topic_id}")
    except Exception as e:
        # Print an error message if something goes wrong during the publish process.
        print(f"Error posting message: {e}")
