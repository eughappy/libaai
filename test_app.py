# file: test_app.py
import unittest
from io import BytesIO
from libaai import app
import os
from PIL import Image, ImageDraw, ImageFont

class LibaAITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Ensure test image exists
        os.makedirs("tests", exist_ok=True)
        image_path = "tests/sample_image.png"
        if not os.path.exists(image_path):
            img = Image.new('RGB', (200, 60), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            d.text((10, 10), "Test OCR Text", fill=(0, 0, 0))
            img.save(image_path)

    def test_chat_endpoint(self):
        response = self.app.post('/chat', json={'message': 'I love SF events'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json)
        self.assertIn('intent', response.json)

    def test_upload_endpoint_with_image(self):
        with open('tests/sample_image.png', 'rb') as img:
            data = {'image': (BytesIO(img.read()), 'sample_image.png')}
            response = self.app.post('/upload', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn('extracted_text', response.json)

    def test_upload_endpoint_no_file(self):
        response = self.app.post('/upload')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()