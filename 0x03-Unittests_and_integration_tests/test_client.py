#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Unit-test GithubOrgClient.has_license"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org property"""
        mock_response = {"login": org_name}
        mock_get_json.return_value = mock_response
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, mock_response)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Unit-test GithubOrgClient.public_repos"""
        mock_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = mock_payload
        client = GithubOrgClient("testorg")
        with patch.object(client, "_public_repos_url", new="https://api.github.com/orgs/testorg/repos"):
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")


if __name__ == "__main__":
    unittest.main()
