# RaE. Reason-and-Execute Prompting

GeoQKG is the pre-training-free representation method that comprehensively extracts the relational information among key elements of a question and stores it in a knowledge structure. This repository provides the code for reproducing GeoQKG method, which is proposed in our paper "**knowledge-structure chimera: towards pre-training-free representation for multimodal geometry question**" 

For the code of the method, please refer to [RaE](https://github.com/chanllon/RaE.-Reason-and-Execute-Prompting).

The GEOS  dataset is now available on [GEOS](https://geometry.allenai.org).

The Geometry3K  dataset is now available on [Geometry3K](https://lupantech.github.io/inter-gps/).

The GeoQA dataset is now available on [GeoQA](https://github.com/chenjudge/GeoQA)).

The GeoQA+  dataset is now available on [GeoQA+](https://github.com/SCNU203/GeoQA-Plus)).

The PGPS9K  dataset is now available on [PGPS9K](https://github.com/mingliangzhang2018/PGPS).

The AI2D  dataset is now available on [AI2D](http://allenai.org/plato/diagram understanding).

The TQA  dataset is now available on [TQA](http://textbookqa.org ).

## Construct question knowledge graph
To construct a comprehensive question knowledge graph, please follow the steps below:
1. Enter the 'GeoQKG' root directory
    ```bash
    cd GeoQKG
    ```
2. Construct a comprehensive question knowledge graph through different rules
    ```bash
    python Graph_Generation_module.py
    ```
## Design adaptive tasks
To adapt question representations utilizing knowledge graphs, we devised four independent downstream tasks: similarity prediction, difficulty evaluation, image-text retrieval, and geometric question answering.
1. Question similarity task:

    Enter the 'Similar' directory
   ```bash
    cd Similar
    ```
   Predict the similarity of questions through the question knowledge graphs
    ```bash
    python Sim_predict_moudle.py
    ```
3. Question difficulty task:

   Enter the 'Difficult' directory
    ```bash
    cd Difficult
    ```
    Predict the difficulty of questions through the question knowledge graphs
    ```bash
    python Diff_predict_moudle.py
    ```

4. Image-text retrieval:

    Enter the 'Image and text retrieval' directory
   ```bash
    cd Image and text retrieval
    ```
   Execute image and text retrieval tasks

   ```bash
    python Sim_text-diagram.py
    ```
   
6. Geometric question answering：

   (1) Implementation of our method in answering geometric question tasks

   Enter the 'GeoQAnswer' directory
    ```bash
    cd GeoQAnswer
    ```
    To have an initial trial of our toolkit, you can use the provided cmd script:
    ```bash
    python run_mwptoolkit.py --model=GraphtoTree --dataset=geo3k --task_type=single_equation --equation_fix=prefix --k_fold=5 --test_step=5 --gpu_id=0
    ```
   (2) Implementation of GPT3.5 in answering geometric question tasks：

   Enter the 'GPT-3.5GeoQAnswer' directory
   ```bash
    cd GPT-3.5GeoQAnswer
    ```
    Implement GPT3.5 answering
   ```bash
    python testgptapi.py
    ```
   (3) Implementation of GPT4.0 in answering geometric question tasks：

   Enter the 'GPT-4.0GeoQAnswer' directory
   ```bash
    cd GPT-4.0GeoQAnswer
    ```
    Implement GPT4.0 answering in all input scenarios (text, diagrams, formal language, prompts)
   ```bash
    python testgpt-all.py
    ```
