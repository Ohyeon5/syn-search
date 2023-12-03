all: env

# ml
env-ml: precommit install-llama-index
	conda activate syn-ml && pip install -e .

install-llama-index: llama-index.git
	conda env create -f ./scripts/env_model.yaml
	conda activate syn-ml && pip install poetry
	conda activate syn-ml && cd llama-index.git && poetry install

llama-index.git:
	git clone https://github.com/jerryjliu/llama_index.git llama-index.git --depth 1

# backend (fastapi)
env-backend:
	conda env create -f ./scripts/env_backend.yaml && install-llama-index

start-fastapi:
	uvicorn src.backend.main:app --host localhost --port 8000 --reload

# frontend (svelte)
env-frontend:
	cd src && npm init vite
	cd src/frontend
	npm install

# dev
precommit:
	bash ./scripts/install_precommit.sh
