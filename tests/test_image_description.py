from utils.llm_utils import QwenImageToText
import unittest


class TestImageDescription(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.qwen_class = QwenImageToText()
        cls.test_image = "data/sample_pictures/014.JPG"


    def test_image_to_uri(self):
        res = self.qwen_class.file_to_data_url(self.test_image)
        self.assertTrue(res.startswith("data:image/jpeg;base64"))
        self.assertGreater(len(res), 100)