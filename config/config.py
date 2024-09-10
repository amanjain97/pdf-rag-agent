import os
import sys

def getEnvOrDefault(env, default):
    return os.getenv(env) if os.getenv(env) else default

def getEnvOrExit(env):
    return os.getenv(env) if os.getenv(env) else sys.exit(f"{env} is missing")

EM_MODEL_NAME = getEnvOrDefault("EM_MODEL_NAME", "BAAI/bge-small-en-v1.5")
EMBEDDING_DIMENSIONS = getEnvOrDefault("EMBEDDING_DIMENSIONS", 384)
EM_MODEL_KWARGS = {'device': 'cpu'}
EM_ENCODE_KWARGS = {'normalize_embeddings': True}
QDRANT_URL = getEnvOrExit("QDRANT_URL")
QDRANT_API_KEY = getEnvOrExit("QDRANT_API_KEY")
QDRANT_COLLECTION = getEnvOrDefault("QDRANT_COLLECTION", "qa_collection")
TEXT_SPLITTER = { "chunk_size": 100, "chunk_overlap": 20}

SUCCESS_STATUS = "success"
FAILED_STATUS = "failed"