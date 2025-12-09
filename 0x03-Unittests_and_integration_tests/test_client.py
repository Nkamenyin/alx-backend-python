#!/usr/bin/env python3
"""
Integration tests for GithubOrgClient.public_repos
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Mock requests.get for integration testing"""

        def mocked_get(url):
            mock_response = Mock()

            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = None

            return mock_response

        cls.get_patcher = patch("requests.get", side_effect=mocked_get)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop requests.get patcher"""
        cls.get_patcher.stop()

    # ✅ ✅ ✅ REQUIRED INTEGRATION TEST
    def test_public_repos(self):
        """Test public_repos integration"""

        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    # ✅ ✅ ✅ REQUIRED APACHE LICENSE FILTER TEST
    def test_public_repos_with_license(self):
        """Test public_repos with apache license"""

        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
