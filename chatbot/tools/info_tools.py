from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import models
from typing import Annotated


embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

QDRANT_URL = 'http://localhost:6333'

qdrant_pizzas = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name='pizzas',
    url=QDRANT_URL,
    distance=models.Distance.DOT
)

qdrant_pizzeria = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name='pizzeria',
    url=QDRANT_URL,
    distance=models.Distance.DOT
)


@tool
def fetch_pizza_details(
    query: Annotated[str, 'A description of the information needed.'],
    type: Annotated[str, 'The type of pizza you want to retrieve information about. Must be one of the following: '
                         '[margherita, pepperoni, hawaiian, neapoletana, capricciosa, romana, carbonara, vegetariana, four cheese, caprese]']
) -> str:
    """
    Retrieves detailed, contextual information about a specific type of pizza, such as origin,
    history, interesting facts, cultural significance, or meaning of its name.
    It is designed for use when there is a need to obtain in-depth knowledge about the background or cultural aspects of particular pizza.
    It should not be used for ingredient-related queries or to retrieve information about pizzas not included in the predefined list of types.
    Returns a string containing detailed descriptive information about the specified type of pizza.
    """
    filter = models.Filter(
        must=[
            models.FieldCondition(
                key=f"metadata.type",
                match=models.MatchValue(value=type)
            )
        ]
    )

    retrieved_docs = qdrant_pizzas.similarity_search(query=query, filter=filter, k=3)
    response = '\n'.join([doc.page_content for doc in retrieved_docs])
    return response


@tool
def fetch_pizzeria_info(
    query: Annotated[str, 'A description of the information needed.']
) -> str:
    """
    Provides answers to frequently asked questions about the pizzeria, such as:
    opening hours, location, accepted payment methods or delivery times.
    Intended for situations where there is a need to address general inquiries about the pizzeria itself.
    It is not suitable for menu or ingredient-related queries.
    The function returns a string containing the relevant details about the pizzeria.
    """
    retrieved_docs = qdrant_pizzeria.similarity_search(query=query, k=3)
    response = '\n'.join([doc.page_content for doc in retrieved_docs])
    return response
