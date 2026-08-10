# import base64
# import mimetypes
# from pathlib import Path
#
# from langchain_core.messages import SystemMessage, HumanMessage
#
# from models.image_metadata import BaseRecord
# from utils.llm_utils import invoke_qwen_with_retry, qwen_llm
#
#
# class QwenImageToText:
#
#     def __init__(self):
#         self.structured_llm = qwen_llm.with_structured_output(schema=BaseRecord)
#
#         self.prompt = """Describe the image with exactly TWO things:
# 1. A short, purely descriptive one-line description of what's on the image
# 2. A one-word tag naming the main object (this MUST NOT be in the description)
#
# Example:
# - description: loading bay of a building in Reading
# - tag: van
# """
#
#     def describe_image(self, image_path: str) -> BaseRecord:
#         image_url = self.file_to_data_url(image_path)
#
#         messages = [
#             SystemMessage(content=self.prompt),
#             HumanMessage(
#                 content=[
#                     {"type": "image_url", "image_url": {"url": image_url}},
#                     {"type": "text", "text": "Return ONLY structured output"},
#                 ]
#             ),
#         ]
#
#         try:
#             result = invoke_qwen_with_retry(self.structured_llm, messages)
#         except Exception:
#             raise
#
#         return result
#
#     @classmethod
#     def file_to_data_url(cls, img_path: str) -> str:
#         path = Path(img_path)
#         if not path.exists():
#             raise FileNotFoundError(f"Image file not found: {img_path}")
#
#         mime_type, _ = mimetypes.guess_type(str(path))
#         mime_type = mime_type or "image/jpeg"
#
#         with path.open("rb") as f:
#             encoded = base64.b64encode(f.read()).decode("utf-8")
#
#         return f"data:{mime_type};base64,{encoded}"
