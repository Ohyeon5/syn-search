# Syn-Search
Optimal Drug Synthesis Condition Searching Conversational AI

Drug discovery often involves meticulous chemical compound synthesis. Medicinal chemists adjust synthesis conditions incrementally to find the optimal state. While using known conditions from literature seems logical, chemical reactions are highly sensitive. Even minor changes in reagents or solvents can alter the outcome significantly.

<img src="figs/frontpage.png" alt="syn-search" width=200px class="center"/>

This project aims to create a chat-based search platform using pre-trained LLMs (Hugging Face) for chemists to effortlessly find experimental conditions.

## Project Details
Develop a chat-based search platform using pre-trained Language Models (LMs) from [hugging face](https://huggingface.co/meta-llama), tailored for chemists to efficiently locate experimental conditions.
The platform will leverage the Retrieval Augmented Generation (RAG) approach to cross-reference and bias model responses towards accurate chemistry literature. [llama-index](https://gpt-index.readthedocs.io/en/latest/index.html) will be used to index the chemistry literature.
The model is then deployed on a azure static web app. The backend is built with flask and deployed on azure app service.

Chemistry experties information are going to be retrieved from PubChem, Reacxys, ChemArxiv, etc. Then, these dataset will be prepared as vector database for the RAG approach. The conditions to generate the optimal synthesis conditions for a given chemical synthesis name or reaction smart will be curated during the hackathon.

### Llama 2
In order to access the Llma 2 models, you need to request access from the [Meta website](https://ai.meta.com/resources/models-and-libraries/llama-downloads). Requests takes 1-2 days, so please submit the request prior to the usage date.

### Project Structure
```
src
|_ backend
|_ frontend
|_ model
```

## Setup
Setup python package:

    make env

## Dataset
Various chemistry related journals will be used. The dataset will be stored in `data` folder. Here are some of the journals we are considering:

- [PubChem](https://pubchem.ncbi.nlm.nih.gov/)
- [Reacxys](https://www.elsevier.com/products/reaxys)
- [ChemArxiv](https://chemrxiv.org/)
- [Wikipedia Chemistry Subsection](https://huggingface.co/datasets/wikipedia)

## Reference
- Retrieval Augmented Generation (RAG) approach: https://www.promptingguide.ai/techniques/rag
