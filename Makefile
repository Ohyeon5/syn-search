python=./env/bin/python

all: env

env: 
	conda env create -f ./environment.yaml -p ./env
	${python} -m pip install -e .
