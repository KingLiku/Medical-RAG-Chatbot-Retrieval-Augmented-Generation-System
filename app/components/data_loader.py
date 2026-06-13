import os
from app.components.load_pdf import load_pdf_files, create_text_chunks
# No need to load the embedding model as it is already done in vector store
from app.components.vector_store import save_vector_store
from app.config.config import DB_FAISS_PATH
from app.common.logger import get_logger

# Import the custom exception class to raise formatted, descriptive errors.
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def process_and_store_pdf():
    try:
        logger.info ("Making the vector store..")
        documents = load_pdf_files()
        text_chunks = create_text_chunks(documents)
        save_vector_store(text_chunks)
        logger.info ("Vector store created successfully. 👍")
    except Exception as e:
        error_msg = CustomException("💔Failed to load vector store.", e)
        # All error messages get stored in logger.py.
        logger.error(str(error_msg))
# This is used to make the function to treat as a main function.
if __name__ == "__main__":
    process_and_store_pdf()
