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

---

This repo was inspired by: @ai-explained

https://youtu.be/wVzuvf9D9BU