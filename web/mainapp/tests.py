import os
from django.test import TestCase, Client


class TestUploadFile(TestCase):

    def test_sample_file(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        client = Client()
        with open(base_dir + '/mainapp/testdata/sample.xlsx', 'rb') as fp:
            response = client.post('/', {"file": fp})
        response_status = response.status_code
        response_content = response.content
        # SQL storing success in the first time or violate constraint in the second time
        self.assertTrue(response_status == 200 or (
            response_status == 400 and response_content == b'SQL Constraint Violation'))
