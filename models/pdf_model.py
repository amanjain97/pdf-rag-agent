from pydantic import BaseModel
from typing import List
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

from utils.file_utils import initialize_qdrant
from config.config import (QDRANT_API_KEY, QDRANT_COLLECTION, QDRANT_URL,
                        EM_ENCODE_KWARGS, EM_MODEL_NAME, EM_MODEL_KWARGS,
)

class PDFModel(BaseModel):
    file_path: str

class QuestionsModel(BaseModel):
    questions: list[str]

class QdrantQuery:
    def __init__(self):
        embedding_model = HuggingFaceEmbeddings(model_name=EM_MODEL_NAME, model_kwargs=EM_MODEL_KWARGS, encode_kwargs=EM_ENCODE_KWARGS)
        qdrant_client = initialize_qdrant(host=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=False)
        self.qdrant_vectordb = Qdrant(qdrant_client, QDRANT_COLLECTION, embedding_model)

    
    def insert_into_vectordb(self, documents: List[Document], filename: str):
        for d in documents:
            d.metadata["source"] = filename
            
        self.qdrant_vectordb.add_documents(documents)

    def get_relevant_docs(self, question: str, k: int = 1):
        relevant_docs = self.qdrant_vectordb.similarity_search(question, k=k)
        return relevant_docs
