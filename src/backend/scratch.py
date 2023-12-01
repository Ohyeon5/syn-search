import os
from pathlib import Path

from dotenv import load_dotenv

# import graphsignal
# from tqdm import tqdm
from llama_index import (  # SimpleDirectoryReader,; VectorStoreIndex,; get_response_synthesizer,
    ServiceContext,
    StorageContext,
    download_loader,
    load_index_from_storage,
    set_global_service_context,
)
from llama_index.embeddings import AzureOpenAIEmbedding
from llama_index.llms import AzureOpenAI
from llama_index.node_parser import JSONNodeParser

# from llama_index.postprocessor import SimilarityPostprocessor
# from llama_index.query_engine import RetrieverQueryEngine
# from llama_index.retrievers import VectorIndexRetriever
# from llama_index.schema import TextNode

load_dotenv()

# graphsignal.configure(
# api_key=os.getenv("OPENAI_API_KEY"), deployment="text-embedding-ada-002"
# )
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

json_parser = JSONNodeParser()
service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embed_model,
    # text_splitter=json_parser,
)

set_global_service_context(service_context)


JSONReader = download_loader("JSONReader")
loader = JSONReader()
path = Path("/mnt/uspto_json/grants/")
glob_len = len(list(path.glob("*.json")))

batch_size = 25
counter = 0
# import time

# for i, filepath in enumerate(tqdm(path.glob("*.json"), total=glob_len)):
# nodes = []
# indices = []
# indices_summaries = []

path = Path("/home/azureuser/jczestochowska/syn-search/data/test_batch")
# documents = SimpleDirectoryReader(path).load_data()
# index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)
# index.storage_context.persist()

# # WORKS
# # creating index
# documents = []
# for filepath in path.glob("*.json"):
#     print(filepath)
#     with open(filepath, "r") as f:
#         json_content = json.load(f)
#     reactions_list = json_content["reactionList"].get("reaction")
#     if reactions_list:
#         print(f"Number of reactions: {len(reactions_list)}")
#         for reaction in reactions_list:
#             node = TextNode(text=str(reaction))
#             nodes.append(node)
#     break
# index = VectorStoreIndex(nodes, service_context=service_context, show_progress=True)
# index.storage_context.persist()
# # END WORKS

# WORKS
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
# query_engine = index.as_query_engine()
# response = query_engine.query("How to prepare chalcone hydrazone?")
# print(response)
# END WORKS

# WORKS
# storage_context = StorageContext.from_defaults(persist_dir="./storage")
# index = load_index_from_storage(storage_context)
# retriever = VectorIndexRetriever(
#     index=index,
#     similarity_top_k=5,
# )
# # configure response synthesizer
# response_synthesizer = get_response_synthesizer()
# # assemble query engine
# query_engine = RetrieverQueryEngine(
#     retriever=retriever,
# )
# # query
# response = query_engine.query("How to prepare chalcone hydrazone?")
# print(response)
# END WORKS


# response = query_engine.query("What are the reactants to obtain chalcone hydrazone?")

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)

system_prompt = """
- You are an AI assistant that answers questions in a friendly manner.
- During the chat you will receive context to base your replies on.
- The context will be a JSON file containing information about a chemical reaction.
"""

chat_engine = index.as_chat_engine(
    chat_mode="context",
    system_prompt=system_prompt,
)

query_engine = index.as_chat_engine()
response = query_engine.chat("How to prepare fuschin hydrazone?")
print(response)

# from llama_index.indices.composability import ComposableGraph

# graph = ComposableGraph.from_indices(GPTTreeIndex, indices, index_summaries=indices_summaries)

# # index.storage_context.persist()
# # query_engine = index.as_query_engine()
# # graph.save_to_disk("graph.json")

# # set query config


# # index = ComposableGraph.load_from_disk("graph.json")

# text = ""
# response = graph.query(text, query_configs=query_configs)

# print(f"Your questions was {text}: \nThe answer is: {str(response)}")
