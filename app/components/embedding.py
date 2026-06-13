# Import HuggingFaceEmbeddings class from langchain_huggingface package.
from langchain_huggingface import HuggingFaceEmbeddings
# Import the custom logging utility to log information and error messages.
from app.common.logger import get_logger
# Import the custom exception class to handle formatting of errors.
from app.common.custom_exception import CustomException

# Initialize the logger for this module using the current module name.
logger = get_logger(__name__)

def get_embedding_model():
    """
    Initializes and returns the Hugging Face embedding model.
    This model converts text chunks into vector representations (embeddings).

    Returns:
        HuggingFaceEmbeddings: The initialized embedding model object.
    """
    try:
        logger.info("🚨 Initializing your Hugging Face embedding model...")

        # Load the sentence-transformers model (all-MiniLM-L6-v2) to generate text embeddings
        model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        logger.info("Successfully loaded the embedding model.")
        return model

    except Exception as e:
        # Wrap the caught exception inside our CustomException class with descriptive details
        error_msg = CustomException("💔 Failed to load embedding model!", e)
        # Log the error message using our logger
        logger.error(str(error_msg))
        # Re-raise the exception to inform the calling function that loading failed
        raise error_msg
