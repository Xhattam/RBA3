# from fastapi import Depends, HTTPException, status, FastAPI, Request
# from fastapi.exceptions import RequestValidationError
#
#
# app = FastAPI(name="RBA3 - Reading Berkshire Archives Automation App")
#
# @app.get("/health")
# def health_check():
#     return {"status": "ok"}
#

from config import settings
from utils.llm_utils import qwen_llm

from core.metadata_generation import QwenImageToText

qwen_class = QwenImageToText()

img_path = "data/sample_pictures/014.JPG"

res = qwen_class.describe_image(img_path)

print(res)
