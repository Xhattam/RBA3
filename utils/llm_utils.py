import base64
import mimetypes
import requests

from config import settings
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PrompTemplate


class QwenImageToText:

    def __init__(self):
        self.api_url = settings.hf_api_url
        self.model_name = settings.qwen_model_name
        self.headers = {
            "Authorization": f"Bearer {settings.hf_token}",
        }



    def file_to_data_url(self, img_path):
        mime_type, _ = mimetypes.guess_type(img_path)
        mime_type = mime_type or "image/jpg"
        with open(img_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        return f"data:{mime_type};base64,{encoded}"


    def query(self, payload):



        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()['choices'][0]['message']

    response = query({
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image in one sentence."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg"
                        }
                    }
                ]
            }
        ],
        "model": "Qwen/Qwen2.5-VL-7B-Instruct:featherless-ai"
    })

    print(response["choices"][0]["message"])