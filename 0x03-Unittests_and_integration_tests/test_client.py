#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    # -------------------------------
    # TEST: GithubOrgClient.org
    # -------------------------------
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected value
           and get_json is called once with correct URL.
        """

        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    # -----------------------------------------
    # TEST: GithubOrgClient._public_repos_url
    # -----------------------------------------
    def test_public_repos_url(self):
        """Unit-test GithubOrgClient._public_repos_url using a patched .org"""

        expected_url = "https://api.github.com/orgs/testorg/repos"

        # Mock payload returned by GithubOrgClient.org
        payload = {"repos_url": expected_url}

        with patch.object(GithubOrgClient, 'org', new=payload):
            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, expected_url)


if __name__ == "__main__":
    unittest.main()
