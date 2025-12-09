#!/usr/bin/env python3
"""
Unit and Integration tests for GithubOrgClient
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


# ---------------------------
# UNIT TESTS
# ---------------------------
class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    # Test org property
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
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

    # Test _public_repos_url
    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from payload"""
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        with patch.object(GithubOrgClient, "org", new=mock_payload):
            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, mock_payload["repos_url"])

    # Test public_repos
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Unit-test GithubOrgClient.public_repos"""
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_payload

        mocked_url = "https://api.github.com/orgs/testorg/repos"

        with patch.object(GithubOrgClient, "_public_repos_url", new=mocked_url):
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)
            mock_get_json.assert_called_once_with(mocked_url)

    # Test has_license (parameterized)
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Unit-test GithubOrgClient.has_license"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


# ---------------------------
# INTEGRATION TESTS
# ---------------------------
@parameterized_class([{
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "apache2_repos": apache2_repos
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get"""
        def mocked_get(url, *args, **kwargs):
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
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos integration"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with apache license"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
