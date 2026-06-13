import os

from langchain_community.vectorstores import FAISS

from app.common.custom_exception import CustomException
from app.common.logger import get_logger
from app.components.embedding import get_embedding_model
from app.config.config import DB_FAISS_PATH

logger = get_logger(__name__)


def load_vector_store():
    try:
        embedding_model = get_embedding_model()
        if os.path.exists(DB_FAISS_PATH):
            logger.info("Loading the existing vector store....🙂")
            return FAISS.load_local(
                DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True
            )
        else:
            logger.warning("No vector store found! 😢")
    except Exception as e:
        error_msg = CustomException("💔Failed to load vector store.", e)
        # All error messages get stored in logger.py.
        logger.error(str(error_msg))
        raise error_msg


def save_vector_store(text_chunks):
    try:
        if not text_chunks:
            raise CustomException ("No text chunks are found!")
        logger.info ("Generating your new vector store....")
        embedding_model = get_embedding_model()
        db = FAISS.from_documents(text_chunks, embedding_model)
        logger.info ("Saving vectorstore .......")
        db.save_local(DB_FAISS_PATH)
        logger.info ("Vector stored saved successfully 🙂")
        return db
    except Exception as e:
        error_msg = CustomException("💔Failed to create your vector store.", e)
        # All error messages get stored in logger.py.
        logger.error(str(error_msg))
        raise error_msg
