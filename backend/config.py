from google import genai
from dotenv import load_dotenv
import os
import logging
import tempfile

# Load environment variables from .env file
load_dotenv()  

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Loading environment variables...")

# Get environment variables
GOOGLE_API_KEY = os.getenv("GEMMA_API_KEY")

if not GOOGLE_API_KEY:
    logger.error("GEMMA_API_KEY is not set in the environment variables.")
    raise ValueError("GEMMA_API_KEY is not set in the environment variables.")
else:
    logger.info("GEMMA_API_KEY is set.")
    # Initialize the Google GenAI client
    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
        logger.info("Google GenAI client initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Google GenAI client: {e}")
        raise
# Define the model name
MODEL_NAME = "gemma-3-27b-it"

# Define the content configuration
CONTENT_CONFIG = genai.types.GenerateContentConfig(
    response_mime_type="text/plain",
)

# Define the content type
CONTENT_TYPE = genai.types.Content(
    role="user",
    parts=[
        genai.types.Part.from_text(text="Extract the items purchased from this receipt and respond in each item in it's own line along with the quanity and the total price. ensure you capture all the items. just straight to the point no more words"),
    ],
)

# Define the file upload function
def upload_file(file_path):
    try:
        with open(file_path, "rb") as file:
            uploaded_file = client.files.upload(file=file)
            logger.info(f"File {file_path} uploaded successfully.")
            return uploaded_file
    except Exception as e:
        logger.error(f"Failed to upload file {file_path}: {e}")
        raise
# Define the function to generate content
def generate_content(file_path):
    try:
        # Upload the file
        files = [
        # Please ensure that the file is available in local system working direrctory or change the file path.
        client.files.upload(file=file_path),]

        # Create the content with the uploaded file
        contents = [
            CONTENT_TYPE,
            genai.types.Content(
                role="user",
                parts=[
                    genai.types.Part.from_uri(
                        file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                    ),
                ],
            ),
        ]

        # Generate content using the model
        message = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=CONTENT_CONFIG,
        )
        logger.info("Content generated successfully.")
        return message.text
    except Exception as e:
        logger.error(f"Failed to generate content: {e}")
        raise
# Example usage
if __name__ == "__main__":
    # Path to the file to be uploaded
    file_path = "image.png"  # Change this to your file path

    # Generate content from the file
    try:
        result = generate_content(file_path)
        print(result)
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
    
    

