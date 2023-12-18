# data preprocessing
env-data:
	conda env create -f ./scripts/env_data.yaml
	~/miniconda3/envs/syn-data/bin/python -m pip install -e ./src/preprocessing/.

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
