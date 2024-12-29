#!/usr/bin/env python
import os
import re
from pprint import pprint
import yaml

from pydantic import BaseModel

from openai import OpenAI
from anthropic import Anthropic
from groq import Groq

models = {
  "openai": [],
  "anthropic": [],
  "groq": [],
}

##################################################

#                               _
#   ___  _ __   ___ _ __   __ _(_)
#  / _ \| '_ \ / _ \ '_ \ / _` | |
# | (_) | |_) |  __/ | | | (_| | |
#  \___/| .__/ \___|_| |_|\__,_|_|
#       |_|

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
openai_models = openai_client.models.list()

print("\n\n === OpenAI ===============\n\n")

for model in openai_models.data:
    print(f"Model: {model.id}")
    models["openai"].append(model.id)
    # if re.match(r'.*(tts|audio|embedding|realtime|moderation|gpt-3\.5-turbo-instruct|whisper|davinci|babbage|dall).*', model.id):
    #     print(" === Ignore ===")
    #     continue
    # try:
    #     response = openai_client.chat.completions.create(
    #         messages=[{
    #             "role": "user",
    #             "content": "Just say yes",
    #         }],
    #         model=model.id,
    #     )
    #     print(response.choices[0].message.content)
    #     if re.match(r'.*([Yy][Ee][Ss]).*', response.choices[0].message.content):
    #         models["openai"].append(model.id)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     print(f"Error type: {type(e).__name__}")

#              _   _                     _
#   __ _ _ __ | |_| |__  _ __ ___  _ __ (_) ___
#  / _` | '_ \| __| '_ \| '__/ _ \| '_ \| |/ __|
# | (_| | | | | |_| | | | | | (_) | |_) | | (__
#  \__,_|_| |_|\__|_| |_|_|  \___/| .__/|_|\___|
#                                 |_|

anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
anthropic_models = anthropic_client.models.list()

print("\n\n === Anthropic ===============\n\n\n")

for model in anthropic_models.data:
    print(f"Model: {model.id}")
    models["anthropic"].append(model.id)
    # try:
    #     response = anthropic_client.messages.create(
    #         max_tokens=32,
    #         messages=[{
    #             "role": "user",
    #             "content": "Just say yes",
    #         }],
    #         model=model.id,
    #     )
    #     print(response.content[0].text)
    #     if re.match(r'.*([Yy][Ee][Ss]).*', response.content[0].text):
    #         models["anthropic"].append(model.id)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     print(f"Error type: {type(e).__name__}")

#   __ _ _ __ ___   __ _
#  / _` | '__/ _ \ / _` |
# | (_| | | | (_) | (_| |
#  \__, |_|  \___/ \__, |
#  |___/              |_|

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
groq_models = groq_client.models.list()

print("\n\n === Groq ===============\n\n\n")

for model in groq_models.data:
    print(f"Model: {model.id}")
    models["groq"].append(model.id)
    # if re.match(r'.*(whisper|guard|specdec).*', model.id):
    #     print(" === Ignore ===")
    #     continue
    # try:
    #     response = groq_client.chat.completions.create(
    #         messages=[{
    #             "role": "user",
    #             "content": "Just say 'yes', please.",
    #         }],
    #         model=model.id,
    #     )
    #     print(response.choices[0].message.content)
    #     if re.match(r'.*([Yy][Ee][Ss]).*', response.choices[0].message.content):
    #         models["groq"].append(model.id)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     print(f"Error type: {type(e).__name__}")

##################################################

for provider in models:
    models[provider].sort()

pprint(models)

current_dir = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.join(current_dir, '..', 'tackleberry', 'registry.yaml')
yaml_path = os.path.normpath(yaml_path)

with open(yaml_path, 'w') as file:
    yaml.dump(models, file, default_flow_style=False)
