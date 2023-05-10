# SmartGPT - An Efficient Approach to OpenAI's ChatGPT

This repository contains a Python application that interacts with the OpenAI GPT-3.5-turbo model in an efficient manner. It utilizes a multi-step approach to generate, evaluate, and refine responses from the model.

## Contents

* `config/` - This folder contains the Hydra configuration files for the application.
* `SmartGPT.py` - This is the main Python script that runs the application.
* `openai_api_chat_completion.py` - This is a Python module that contains classes and functions for interacting with the OpenAI API.
* `environment.yml` - This file contains the conda environment configuration.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/munirjojoverge/SmartGPT.git
```

2. Navigate into the cloned repository:
```bash
cd SmartGPT
```

3. Create a new conda environment from the `environment.yml` file:
```bash
conda env create -f environment.yml
```

4. Activate the new environment:
```bash
conda activate smartgpt
```

5. Copy your OpenAI key into the appropriate config file in the `config/` directory.

## Usage

You can run the application by executing the `SmartGPT.py` script:

```bash
python SmartGPT.py
```

This will launch the application and begin the interaction with the GPT-3.5-turbo model.

## Promp Frameworks:

### Chain of Thought
    Answer: Let's work this out in a step by step way to be sure we have the right answer

### Relexion: Discover flaws and faulty logic
    You are a researcher tasked with investigating the X response options provided. List the flaws and faulty logic of each answer option. Let's work this out in a step by step way to be sure we have all the errors:

### Resolution
    You are a resolver tasked with 1) finding which of the X answer options the researcher thought was best 2) improving that answer, and 3) Printing the improved answer in full. Let's work this out in a step by step way to be sure we have the right answer:

## References
* Automatically Discovered Chain of Thought: https://arxiv.org/pdf/2305.02897.pdf
* Karpathy Tweet: https://twitter.com/karpathy/status/1...
* Best prompt: Theory of Mind: https://arxiv.org/ftp/arxiv/papers/23...
* Few Shot Improvements: https://sh-tsang.medium.com/review-gp...
* Dera Dialogue Paper: https://arxiv.org/pdf/2303.17071.pdf
* MMLU: https://arxiv.org/pdf/2009.03300v3.pdf
* GPT 4 Technical report: https://arxiv.org/pdf/2303.08774.pdf
* Reflexion paper: https://arxiv.org/abs/2303.11366
* Why AI is Smart and Stupid: https://www.youtube.com/watch?v=SvBR0OGT5VI&t=1s  
* Lennart Heim Video: https://www.youtube.com/watch?v=7EwAdTqGgWM&t=67s  

---

This repo was inspired by: @ai-explained

https://youtu.be/wVzuvf9D9BU