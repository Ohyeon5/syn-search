# Data preprocessing for SynSearch
SynSearch utilizes the RAG approach to generate responses. To do this, we make index vectors for USPTO data (other datasets are coming). Also, to make chemical representation more accessible (e.g., smiles), we added a `functional group annotator` to the preprocessing pipeline.

## Requirements
- llama-index
- rdkit

## Setup
```
make env-data
```

## Llama Index
Use `from llama_index.indices.composability import ComposableGraph`

## References
- [Blog by Ryan Nguyen, how to use index correctly](https://howaibuildthis.substack.com/p/llamaindex-how-to-use-index-correctly)
