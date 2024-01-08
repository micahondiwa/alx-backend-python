#!/usr/bin/env python3
"""
tests for client module
"""
import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from parameterized import parameterized, parameterized_class
from typing import Dict
from requests import HTTPError
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class"""

    @parameterized.expand([("google", {"login": "google"}), ("abc", {"login": "abc"})])
    @patch("client.get_json")
    def test_org(self, org: str, resp: Dict, mocked_fn: MagicMock) -> None:
        """Test output for GithubOrgClient method org"""
        mocked_fn.return_value = MagicMock(return_value=resp)
        gh_client = GithubOrgClient(org)
        self.assertEqual(gh_client.org(), resp)
        mocked_fn.assert_called_once_with(f"https://api.github.com/orgs/{org}")

    def test_public_repos_url(self) -> None:
        """Test GithubOrgClient property _public_repos_url"""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/users/google/repos",
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos",
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Test output for GithubOrgClient method public_repos"""
        test_payload = {
            "repos_url": "https://api.github.com/users/google/repos",
            "repos": [
                {
                    "name": "episodes.dart",
                },
                {
                    "name": "kratu",
                },
            ],
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch(
            "client.GithubOrgClient._public_repos_url", new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                [
                    "episodes.dart",
                    "kratu",
                ],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Test output for GithubOrgClient method has_license"""
        self.assertEqual(GithubOrgClient("google").has_license(repo, key), expected)


@parameterized_class(
    [
        {
            "org_payload": TEST_PAYLOAD[0][0],
            "repos_payload": TEST_PAYLOAD[0][1],
            "expected_repos": TEST_PAYLOAD[0][2],
            "apache2_repos": TEST_PAYLOAD[0][3],
        },
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient class"""

    @classmethod
    def setUpClass(cls) -> None:
        """method called before tests in an individual class are run"""
        route_payload = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
        }

        def get_payload(url):
            """method to get url payload"""
            if url in route_payload:
                return Mock(**{"json.return_value": route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """method called after tests in an individual class have run"""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """integration test for GithubOrgClient.public_repos without args"""
        self.assertEqual(GithubOrgClient("google").public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """integration test for GithubOrgClient.public_repos with args"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )
