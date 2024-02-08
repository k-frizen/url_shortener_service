import json
import unittest

from url_shortner.app import app


class TestApp(unittest.TestCase):

    def setUp(self) -> None:
        self.task_url = "https://botoeducation.notion.site/Backend-developer-test-task-1338fc57e3254397a95ca430ea2f8d33"
        self.app = app.test_client()
        self.url_data = {'url': self.task_url}

    def test_generation_shorten_(self):
        response = self.app.put('/api/url', json=self.url_data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertIn("url", data)

    def test_delete_short_url(self):
        short_url_response = self.app.put('/api/url', json=self.url_data)
        data = json.loads(short_url_response.data.decode('utf-8'))
        short_code = data.get("url").split('/')[-1]

        remove_url_response = self.app.delete(f'/api/url/{short_code}')
        self.assertEqual(remove_url_response.status_code, 200)

        error_deleting_response = self.app.delete(f'/api/url/{short_code}')
        self.assertEqual(error_deleting_response.status_code, 500)
        error_data = json.loads(error_deleting_response.data.decode('utf-8'))
        self.assertIn("error", error_data)

    def test_redirect_to_original_url(self):
        response = self.app.put('/api/url', json=self.url_data)
        data = json.loads(response.data.decode('utf-8'))
        short_code = data.get("url").split('/')[-1]

        response = self.app.get(f'/{short_code}')
        self.assertEqual(response.status_code, 302)

    def test_incorrect_redirection(self):
        response = self.app.get('/url_does_not_exist')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn("error", data)


if __name__ == '__main__':
    unittest.main()
