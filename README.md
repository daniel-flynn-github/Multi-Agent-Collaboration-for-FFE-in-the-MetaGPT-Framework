# Multi Agent-Collaboration for FFE in the MetaGPT Framework

**Repository for: Multi-Agent-Collaboration-for-FFE-in-the-MetaGPT-Framework Dissertation Project**\
[Report](./dissertation-paper.pdf)



New Code:

All the files in `src/MetaGPT/roles/...` other than the `Role.py` base class and `init.py`\
All the files in `src/MetaGPT/actions/...` other than the `Action.py` base class, `init.py`, and `ActionOutput.py`

Modified Code:

`src/MetaGPT/startup.py`
`src/MetaGPT/environment.py`
`src/MetaGPT/roles/init.py`
`src/MetaGPT/actions/init.py`

DISCLAIMER: ALL OTHER CODE IS FROM THE ORIGINAL METAGPT PROJECT AND IS NOT MY OWN


## Build instructions

## Configuration:

You must first configure the LLM you choose to use and its API key in the corresponding fields found in `.../src/MetaGPT/config/key.yaml`. This version of MetaGPT only reliably supports GPT-3 and GPT-4 models. To gain access to API credits, a payment will have to be made to OpenAI. A run with GPT-3 only costs approximatley 7 cents. A run with GPT-4 costs upwards of a dollar.

Required `key.yaml` for GPT-3.5:

`OPENAI_API_MODEL: "gpt-3.5-turbo-0125"`
`OPENAI_API_KEY: "{your OpenAI api key}"`

OpenAI API credits can be purchased here: https://platform.openai.com/usage


### Requirements

* Python 3.9
* Packages: listed in `src/MetaGPT/requirements.txt` 
* Tested on Windows 11

### Build steps

Navigate to `.../src/MetaGPT/` in a console environment\
Run `pip install -r requirements. txt` to install the required packages\
Configure the LLM as described above\
Run `python startup.py` to execute the program\

### Test steps

Run `python startup.py -example_scenario` to load the program with an example innovation scenario.\
Observe the output in console and files that generated in `.../src/MetaGPT/workspace`

