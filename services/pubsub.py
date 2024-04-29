from google.cloud import pubsub_v1
from google.oauth2.service_account import Credentials
from os import getenv, path
from dotenv import load_dotenv

load_dotenv()

project_id = getenv("GCP_PROJECT_ID", "your-gcp-project-id")
topic_id = getenv("PUBSUB_TOPIC_ID", "my-new-topic")
gcp_credentials = getenv("GCP_CREDENTIALS")

# credentials base path
credentials_path = path.join(path.dirname(path.dirname(__file__)), gcp_credentials)

credentials = Credentials.from_service_account_file(credentials_path)
publisher = pubsub_v1.PublisherClient(credentials=credentials)

topic_path = publisher.topic_path(project_id, topic_id)


def publish_message(data: any) -> None:
    """Publish a created user message to the Pub/Sub topic."""
    data_str = str(data)  # string parsing
    data_bytes = data_str.encode("utf-8")  # bytes parsing
    try:
        publish_future = publisher.publish(topic_path, data_bytes)
        publish_future.result()
        print(f"Posted message to topic: {topic_id}")
    except Exception as e:
        print(f"Error posting message: {e}")
