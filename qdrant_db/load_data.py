from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from typing import List
import os
import pathlib
import uuid

load_dotenv()


DATA_FOLDER_PATH = pathlib.Path(__file__).parent / 'data'
VECTOR_SIZE = 1536
DISTANCE = models.Distance.DOT

qdrant_client = QdrantClient("http://qdrant:6333")
embeddings = OpenAIEmbeddings(model='text-embedding-3-small')


def create_collection(client: QdrantClient, collection_name) -> QdrantVectorStore:
    """Creates new collection in Qdrant"""
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)

    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=DISTANCE)
    )

    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
        distance=DISTANCE
    )


def get_documents(folder_path: pathlib.Path, metadata_key: str, chunk_size: int, chunk_overlap: int) -> List[Document]:
    """Loads document from a file and splits it into smaller chunks"""
    docs = []

    for file in os.listdir(folder_path):
        file_path = folder_path / file
        metadata = {metadata_key: file.split('.')[0].lower()}

        with open(file_path, 'r') as f:
            content = f.read().replace('\n', ' ')

        document = Document(
            page_content=content,
            metadata=metadata,
        )

        docs.append(document)

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)


if __name__ == '__main__':
    collection_name = 'pizzas'
    vector_store = create_collection(qdrant_client, collection_name)
    folder_path = DATA_FOLDER_PATH / 'pizzas'
    docs = get_documents(folder_path, metadata_key='type', chunk_size=300, chunk_overlap=50)
    ids = [str(uuid.uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=ids)
    print(f"Uploaded {len(docs)} points to collection '{collection_name}'.")

    collection_name = 'pizzeria'
    vector_store = create_collection(qdrant_client, collection_name)
    folder_path = DATA_FOLDER_PATH / 'FAQs'
    docs = get_documents(folder_path, metadata_key='file', chunk_size=200, chunk_overlap=30)
    ids = [str(uuid.uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=ids)
    print(f"Uploaded {len(docs)} points to collection '{collection_name}'.")
