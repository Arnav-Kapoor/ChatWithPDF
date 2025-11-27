from weaviate.connect import ConnectionParams
from weaviate.classes.init import Auth
from weaviate.classes.init import AdditionalConfig, Timeout
import weaviate
from langchain_weaviate import WeaviateVectorStore


def set_connection():
    client = weaviate.WeaviateClient(connection_params=ConnectionParams.from_params(
        http_host="amazing-stays-extras-intake.trycloudflare.com",
        # http_port="8080",
        http_port=None,
        http_secure=True,
        grpc_host="amazing-stays-extras-intake.trycloudflare.com",
        # grpc_port="50051",
        grpc_port=None,
        grpc_secure=True,
    ))

    client.connect()
    print(client.is_ready())

    return client