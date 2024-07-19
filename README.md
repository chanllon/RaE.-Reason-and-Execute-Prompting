# RaE. Reason-and-Execute Prompting

RaE is a new prompting method specifically designed for enhancing Multi-Modal Large Language Models to solve geometric questions. This repository provides the code for reproducing RaE prompting method, which is proposed in our paper "**Reason-and-Execute Prompting: Enhancing Multi-Modal Large Language Models for Solving Geometry Questions**" 

For the code of the method, please refer to [RaE](https://github.com/chanllon/RaE.-Reason-and-Execute-Prompting).

The GEOS  dataset is now available on [GEOS](https://geometry.allenai.org).

The Geometry3K  dataset is now available on [Geometry3K](https://lupantech.github.io/inter-gps/).

The GeoQA dataset is now available on [GeoQA](https://github.com/chenjudge/GeoQA).

The GeoQA+  dataset is now available on [GeoQA+](https://github.com/SCNU203/GeoQA-Plus).

The PGPS9K  dataset is now available on [PGPS9K](https://github.com/mingliangzhang2018/PGPS).

The AI2D  dataset is now available on [AI2D](http://allenai.org/plato/diagram-understanding).

The TQA  dataset is now available on [TQA](http://textbookqa.org ).

## Installation
Clone this repo and install with `pip`.
```
git clone https://github.com/chanllon/RaE.-Reason-and-Execute-Prompting
pip install -e ./pal
```

Before running the scripts, set the OpenAI key,
```export OPENAI_API_KEY='sk-...'```


## Run code
We provide a simple and convenient method for running code, please follow the steps below:
1. Run the Main.py program
    ```bash
    python main.py --model ** --dataset ** --prompt **
    ```
2. An example
    ```bash
    python main.py --model GPT4 --dataset GEOS --prompt RaE
    ```
