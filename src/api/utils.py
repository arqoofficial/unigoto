from sentence_transformers import SentenceTransformer

__all__ = [
    "get_embedding_model",
]

_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return _embedding_model
