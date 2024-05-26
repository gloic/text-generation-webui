#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate textgen

python server.py
# TheBloke_Phind-CodeLlama-34B-v2-GPTQ_gptq-4bit-64g-actorder_True
# TheBloke_MythoMax-L2-13B-GPTQ_gptq-4bit-32g-actorder_True
