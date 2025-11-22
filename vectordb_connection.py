from weaviate.connect import ConnectionParams
from weaviate.classes.init import Auth
from weaviate.classes.init import AdditionalConfig, Timeout
import weaviate
from langchain_weaviate import WeaviateVectorStore


def set_connection():
    client = weaviate.WeaviateClient(connection_params=ConnectionParams.from_params(
        http_host="localhost",
        http_port="8080",
        http_secure=False,
        grpc_host="localhost",
        grpc_port="50051",
        grpc_secure=False,
    ))

    client.connect()
    print(client.is_ready())

    return client