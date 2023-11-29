python=./env/bin/python

all: env

env: install-llama-index
	${python} -m pip install -e .

env-dev: precommit install-llama-index
	${python} -m pip install -e .

install-llama-index: llama-index.git
	conda env create -f ./environment.yaml -p ./env
	${python} -m pip install poetry
	cd llama-index.git && poetry env use ${python} && poetry install

llama-index.git:
	git clone https://github.com/jerryjliu/llama_index.git llama-index.git --depth 1

precommit:
	bash ./scripts/install_precommit.sh
