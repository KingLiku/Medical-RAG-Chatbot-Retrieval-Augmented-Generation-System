import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Import the custom logging utility to log information and error messages.
from app.common.logger import get_logger
# Import the custom exception class to raise formatted, descriptive errors.
from app.common.custom_exception import CustomException
# Import config variables: path to PDF data, and parameters for text splitting.
from app.config.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP

# Initialize the logger for this module using the current module name.
logger = get_logger(__name__)

def load_pdf_files():
    """
    Loads all PDF documents from the configured directory.
    
    Returns:
        list: A list of loaded LangChain Document objects.
    """
    try:
        # Check if the configured data directory exists before loading
        if not os.path.exists(DATA_PATH):
            raise CustomException("Data path doesn't exist!")
        
        logger.info(f"Loading PDF files from: {DATA_PATH}")
        
        # DirectoryLoader loads all matching files in the directory.
        # We target all files ending with '.pdf' using PyPDFLoader to parse each file.
        loader = DirectoryLoader(
            DATA_PATH,
            glob="*.pdf",
            loader_cls=PyPDFLoader
        )
        
        # Load and parse the PDFs into document objects
        documents = loader.load()
        
        if not documents:
            logger.warning("No PDF documents were found in the data path.")
        else:
            logger.info(f"Successfully fetched {len(documents)} document pages.")
            
        return documents
    except Exception as e:
        # Wrap the exception in our CustomException class with descriptive details
        error_msg = CustomException("💔Failed to load your pdf!", e)
        # Log the error string using our logger
        logger.error(str(error_msg))
        return []

def create_text_chunks(documents):
    """
    Splits the loaded documents into smaller text chunks for processing.
    
    Args:
        documents (list): A list of LangChain Document objects.
        
    Returns:
        list: A list of split LangChain Document chunks.
    """
    try:
        if not documents:
            raise CustomException("No documents were provided to split!")
            
        logger.info(f"Splitting the {len(documents)} document pages into text chunks...")
        
        # Set up the text splitter with the configured chunk size and overlap
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        
        # Split the loaded document pages into smaller chunks
        text_chunks = text_splitter.split_documents(documents)
        
        logger.info(f"Generated {len(text_chunks)} text chunks.")
        return text_chunks
    except Exception as e:
        # Wrap the exception in our CustomException class with descriptive details
        error_msg = CustomException("Failed to generate the text chunks properly!", e)
        # Log the error string
        logger.error(str(error_msg))
        return []
