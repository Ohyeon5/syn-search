import json

# from llama_index.core import set_global_tokenizer
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.llama_cpp.llama_utils import (
    completion_to_prompt,
    messages_to_prompt,
)

# from transformers import AutoTokenizer

# model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q3_K_S.gguf"
model_path = "/Users/ochoung/Projects/personal-ds/ppl/data/llama-2-7b-chat.Q3_K_S.gguf"

llm = LlamaCPP(
    model_url=None,
    model_path=model_path,
    temperature=0.1,
    max_new_tokens=256,
    context_window=3900,
    generate_kwargs={},
    model_kwargs={},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=False,
)

json_file = "/Users/ochoung/Projects/personal-ds/ppl/data/articles.json"
with open(json_file, "r") as f:
    json_content = json.load(f)

response = llm.complete(
    "Summary the efficacy of Cosentyx given following articles: "
    + json_content[0]["abstract"]
    + json_content[1]["abstract"]
)
print(response.text)

# response_iter = llm.stream_complete("Can you write me a poem about fast cars?")
# for response in response_iter:
#     print(response.delta, end="", flush=True)


# set_global_tokenizer(
#     AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf").encode
# )

# embed_model = HuggingFaceEmbedding(model_name="intfloat/e5-small")
# json_file = "/Users/ochoung/Projects/personal-ds/ppl/data/articles.json"
# with open(json_file, "r") as f:
#     json_content = json.load(f)

# nodes = []
# for article in json_content:
#     node = TextNode(text=str(article))
#     nodes.append(node)
# index = VectorStoreIndex(nodes,mbed_model=embed_model)
# query_engine = index.as_query_engine(llm=llm)
# response = query_engine.query("What is Cosentyx?")
# print(response)
