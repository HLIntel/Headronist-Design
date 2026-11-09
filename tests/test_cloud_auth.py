import io
import os
import unittest
from unittest.mock import patch
from headronist.cloud import application


class CloudAuthTests(unittest.TestCase):
    def test_non_ascii_authorization_fails_closed(self):
        status = []
        env = {"PATH_INFO": "/mcp", "REQUEST_METHOD": "POST", "HTTP_AUTHORIZATION": "Bearer é", "wsgi.input": io.BytesIO()}
        with patch.dict(os.environ, {"HEADRONIST_API_TOKEN": "a" * 24}):
            application(env, lambda code, headers: status.append(code))
        self.assertEqual(status, ["401 Unauthorized"])
