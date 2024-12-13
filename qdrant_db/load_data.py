from qdrant_client import QdrantClient, models
from openai import OpenAI
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from typing import List
import os
import pathlib
import uuid

load_dotenv()


qdrantClient = QdrantClient("http://qdrant")
openaiClient = OpenAI()

DATA_FOLDER_PATH = pathlib.Path(__file__).parent / 'data'


def get_documents(file_path: pathlib.Path, metadata: dict) -> List[Document]:
    """Loads document from a file and splits it into smaller chunks"""
    with open(file_path, 'r') as f:
        content = f.read().replace('\n', ' ')

    document = Document(
        page_content=content,
        metadata=metadata,
    )

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    return splitter.split_documents([document])


def generate_points(docs: List[Document], metadata_key: str) -> List[models.PointStruct]:
    """Generates embeddings and PointStruct objects from a list of documents"""
    points = []

    for doc in docs:
        response = openaiClient.embeddings.create(
            model='text-embedding-3-small',
            input=doc.page_content
        )
        embed = response.data[0].embedding

        point = models.PointStruct(
            id=str(uuid.uuid4()),
            vector=embed,
            payload={
                'metadata': {'type': doc.metadata.get(metadata_key)},
                'page_content': doc.page_content
            }
        )

        points.append(point)

    return points


def process_folder_and_uplaod(folder_name: str, collection_name: str, metadata_key: str) -> None:
    """Processes all the files in the folder and send them to Qdrant within the specified collection"""
    folder_path = DATA_FOLDER_PATH / folder_name
    files = os.listdir(folder_path)
    points = []

    for file in files:
        file_path = folder_path / file
        metadata = {metadata_key: file.split('.')[0].lower()}
        docs = get_documents(file_path, metadata)
        pts = generate_points(docs, metadata_key)
        points.extend(pts)

    if not qdrantClient.collection_exists(collection_name):
        qdrantClient.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.DOT)
        )

    qdrantClient.upload_points(
        collection_name=collection_name,
        points=points,
        wait=True
    )
    print(f"Uploaded {len(points)} points to collection '{collection_name}'.")


if __name__ == "__main__":
    process_folder_and_uplaod(
        folder_name='pizzas',
        collection_name='pizzas',
        metadata_key='pizza_type'
    )

    process_folder_and_uplaod(
        folder_name='FAQs',
        collection_name='pizzeria',
        metadata_key='file'
    )
