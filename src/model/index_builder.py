import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from llama_index import ServiceContext, VectorStoreIndex
from llama_index.embeddings import AzureOpenAIEmbedding
from llama_index.llms import AzureOpenAI
from llama_index.schema import TextNode
from settings import settings

load_dotenv()


def prepare_context():
    llm = AzureOpenAI(
        engine="gpt-35-turbo",
        model="gpt-35-turbo",
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_BASE_URL"),
    )

    embed_model = AzureOpenAIEmbedding(
        azure_deployment="text-embedding-ada-002",
        model="text-embedding-ada-002",
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_BASE_URL"),
        embed_batch_size=1,
    )

    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )
    return service_context


def build_index(patents_path):
    path = Path(patents_path)
    # Create LlamaIndex nodes, each node is a separate vector
    nodes = []
    for filepath in path.glob("*.json"):
        print(f"Processing file: {filepath}")
        with open(filepath, "r") as f:
            json_content = json.load(f)
        reactions_list = json_content["reactionList"].get("reaction")
        if reactions_list:
            print(f"Number of reactions: {len(reactions_list)}")
            for reaction in reactions_list:
                node = TextNode(text=str(reaction))
                nodes.append(node)

    service_context = prepare_context()
    # Get embeddings and index them
    index = VectorStoreIndex(nodes, service_context=service_context, show_progress=True)
    # By default saves to ./storage
    index.storage_context.persist()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Building vector database of chemical reaction patents using LlamaIndex"
    )
    parser.add_argument(
        "--patents_path",
        type=str,
        default=settings.data_path,
        help="The default path points to all the patents, this may cause rate limits, "
        "consider working with a small subets of files.",
    )
    args = parser.parse_args()
    build_index(args.patents_path)
