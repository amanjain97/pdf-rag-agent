import PyPDF2
import logging

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from config.config import QDRANT_COLLECTION, EMBEDDING_DIMENSIONS

ALLOWED_EXTENSIONS = ['pdf']
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_pdf(filepath):
    try:
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            if reader.is_encrypted:
                return False, 'PDF is encrypted'
        return True, 'Valid PDF'
    except Exception as e:
        return False, str(e)


def initialize_qdrant(host: str, api_key: str, prefer_grpc: bool):
    qdrant_client = QdrantClient(url=host, api_key=api_key, prefer_grpc=prefer_grpc)

    def create_collection(collection_name: str):
        try:
            qdrant_client.get_collection(collection_name=collection_name)
            logger.info(f"Collection {collection_name} already exists.")
        except Exception:
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=EMBEDDING_DIMENSIONS, distance=Distance.COSINE),
                
            ) 
            logger.info(f"Collection {collection_name} is successfully created.")

    create_collection(QDRANT_COLLECTION)
    return qdrant_client
