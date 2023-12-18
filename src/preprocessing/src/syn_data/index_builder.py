import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from llama_index import ServiceContext, VectorStoreIndex
from llama_index.embeddings import AzureOpenAIEmbedding
from llama_index.llms import AzureOpenAI
from llama_index.schema import TextNode

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


def build_index(patents_path, save_path, prefix="", chunksize=1000, overlap=20):
    # Create LlamaIndex nodes, each node is a separate vector
    nodes = []
    for filepath in patents_path.glob(f"{prefix}*.json"):
        print(f"Processing file: {filepath}")
        reactions_list = filter_reactant_fg(filepath)
        if len(reactions_list) > 0:
            print(f"Number of reactions: {len(reactions_list)}")
            for reaction in reactions_list:
                reaction_text = str(reaction)
                node = TextNode(text=reaction_text)
                nodes.append(node)

    service_context = prepare_context()
    # Get embeddings and index them
    index = VectorStoreIndex(nodes, service_context=service_context, show_progress=True)
    # By default saves to save_path
    index.storage_context.persist(persist_dir=save_path)


def filter_reactant_fg(json_file):
    fg_list = [
        "alpha aryl carboxylic acid",
        "acidic groups",
        "primary amine",
        "secondary amine",
        "aldehyde",
        "ketone",
        "alcohol",
    ]
    with open(json_file, "r") as f:
        json_content = json.load(f)
    reaction_list = json_content["reactionList"].get("reaction")
    good_reactions = []
    if reaction_list:
        for reaction in reaction_list:
            reactant_fg = []
            if "reactant" in reaction["reactantList"].keys():
                reactant_list = reaction["reactantList"].get("reactant")
                # among reactant we want at list one of the fg_list exists
                if isinstance(reactant_list, list):
                    for reactant in reactant_list:
                        if "funcgroups" in reactant.keys():
                            reactant_fg.extend(reactant["funcgroups"])
                elif isinstance(reactant_list, dict):
                    reactant_fg.extend(reactant_list["funcgroups"])
            checker = any([fg in reactant_fg for fg in fg_list])
            if checker:
                good_reactions.append(reaction)
    print(f"after removing: {len(good_reactions)}")
    return good_reactions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Building vector database of chemical reaction patents using LlamaIndex"
    )
    parser.add_argument(
        "--patents_path",
        type=Path,
        default=Path("/datadrive/uspto_json/new_grants/"),
        help="The default path points to all the patents, this may cause rate limits, "
        "consider working with a small subets of files.",
    )
    parser.add_argument(
        "--save_path",
        type=Path,
        default=Path("/datadrive/new_grant/"),
        help="The default path points to all the patents, this may cause rate limits, "
        "consider working with a small subets of files.",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="I2011",
        help="prefix to reduce the number of files to be processed",
    )
    args = parser.parse_args()
    save_path = args.save_path.parent / f"{str(args.save_path.name)}_{args.prefix}"
    save_path.mkdir(parents=True, exist_ok=True)
    build_index(args.patents_path, save_path, prefix=args.prefix)
