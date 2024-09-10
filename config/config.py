import os

def getEnvOrDefault(env, default):
    return os.getenv(env) if os.getenv(env) else default

EM_MODEL_NAME = getEnvOrDefault("EM_MODEL_NAME", "BAAI/bge-small-en-v1.5")
EMBEDDING_DIMENSIONS = getEnvOrDefault("EMBEDDING_DIMENSIONS", 384)
EM_MODEL_KWARGS = {'device': 'cpu'}
EM_ENCODE_KWARGS = {'normalize_embeddings': True}
TEXT_SPLITTER = { "chunk_size": 100, "chunk_overlap": 20}

SUCCESS_STATUS = "success"
FAILED_STATUS = "failed"