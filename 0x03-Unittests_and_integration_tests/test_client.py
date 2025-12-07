#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    #
    # 1️⃣ Test org property
    #
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data"""
        mock_response = {"login": org_name}
        mock_get_json.return_value = mock_response

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, mock_response)

    #
    # 2️⃣ Test _public_repos_url
    #
    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from payload"""
        mock_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

        with patch.object(GithubOrgClient, "org", new=mock_payload):
            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, mock_payload["repos_url"])

    #
    # 3️⃣ Test public_repos()
    #
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Unit-test GithubOrgClient.public_repos"""

        # Mock list of repos returned by get_json
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_payload

        mocked_url = "https://api.github.com/orgs/testorg/repos"

        # Patch _public_repos_url so the client hits this URL
        with patch.object(GithubOrgClient, "_public_repos_url", new=mocked_url):

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)

            # Ensure JSON fetch was done once with correct URL
            mock_get_json.assert_called_once_with(mocked_url)


if __name__ == "__main__":
    unittest.main()
