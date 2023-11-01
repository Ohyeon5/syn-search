# Syn-Search
Optimal Drug Synthesis Condition Searching Conversational AI

Drug discovery often involves meticulous chemical compound synthesis. Medicinal chemists adjust synthesis conditions incrementally to find the optimal state. While using known conditions from literature seems logical, chemical reactions are highly sensitive. Even minor changes in reagents or solvents can alter the outcome significantly.

<img src="figs/frontpage.png" alt="syn-search" width=200px class="center"/>

This project aims to create a chat-based search platform using pre-trained LLMs (Hugging Face) for chemists to effortlessly find experimental conditions.

## Project Details
We fine-tune the pre-trained LLMs (LlaMa) shared in [hugging face](hhttps://huggingface.co/meta-llama). The model is then deployed on a azure static web app. The backend is built with flask and deployed on azure app service.

This model will be fine-tuned with chemistry related journals such as PubChem, Reacxys, ChemArxiv, etc. The model will be trained to generate the optimal synthesis conditions for a given chemical synthesis name or reaction smart.

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
