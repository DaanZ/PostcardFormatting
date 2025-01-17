import json
import os

import requests
import time

from dotenv import load_dotenv

from chatgpt import llm_chat
from history import History

load_dotenv()

api_key = os.environ["LEONARDO_API_KEY"]
authorization = "Bearer %s" % api_key

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}


def get_models():
    url = "https://cloud.leonardo.ai/api/rest/v1/platformModels"
    response = requests.get(url, headers=headers)
    return response.json()["custom_models"]


def get_model_id(model_name):
    models = get_models()

    for model in models:
        if model["name"] == model_name:
            return model["id"]

    return None


def request_generate_image(text: str, amount: int = 4, width=1024, height=1024,
                           model_name: str = "Leonardo Vision XL", alchemy: bool = False):
    #model_id = get_model_id(model_name)

    payload = {
        "width": width,
        "height": height,
        "modelId": "6b645e3a-d64f-4341-a6d8-7a3690fbf042",
        "prompt": text,
        "num_images": 4,
        "alchemy": alchemy,
        "enhancePrompt": False,
        "promptMagicVersion": "v3"
    }

    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    generation_id = response.json()['sdGenerationJob']['generationId']
    return generation_id


def request_generated_image(generation_id):
    url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id

    for i in range(20):
        time.sleep(0.5)

        response = requests.get(url, headers=headers)
        text = json.loads(response.content)
        if len(text["generations_by_pk"]["generated_images"]) != 0:
            return text["generations_by_pk"]["generated_images"]
        else:
            print(text)
    return None


# Generate with an image prompt
def generate_leonardo(text, amount=4, width=1472, height=832, alchemy=False):

    if len(text) > 1500:
        history = History()
        history.user(text)
        history.system("Summarize the image prompt from the user; Only return the summary:")

        text = llm_chat(history)

    generation_id = request_generate_image(text, amount, width, height, alchemy=alchemy)
    return request_generated_image(generation_id)


if __name__ == "__main__":
    #print(get_models())
    print(generate_leonardo("Lunar Moth from papercraft", alchemy=True))