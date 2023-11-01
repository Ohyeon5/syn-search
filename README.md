# syn-search
Optimal Drug Synthesis Condition Searching Conversational AI

Drug discovery often involves meticulous chemical compound synthesis. Medicinal chemists adjust synthesis conditions incrementally to find the optimal state. While using known conditions from literature seems logical, chemical reactions are highly sensitive. Even minor changes in reagents or solvents can alter the outcome significantly.

This project aims to create a chat-based search platform using pre-trained LLMs (Hugging Face) for chemists to effortlessly find experimental conditions.

## Setup
Setup python package:

    make

If make doesn't work, manually set upt the environment:

	conda env create -f ./environment.yaml -p ./env
	./env/bin/python -m pip install -e .

Then, activate the environment:

    conda activate ./env
