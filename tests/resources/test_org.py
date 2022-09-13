"""
Tests for the V2 SDK Org.

"""
from unittest import TestCase, mock

from runeq.config import Config
from runeq.resources.client import GraphClient
from runeq.resources.org import Org, get_org, get_orgs


class TestOrg(TestCase):
    """
    Unit tests for the Org class.

    """

    def setUp(self):
        """
        Set up mock graph client for testing.

        """
        self.mock_client = GraphClient(
            Config(
                client_key_id='test',
                client_access_key='config'
            )
        )

    def test_attributes(self):
        """
        Test attributes for an initialized Org.

        """
        test_org = Org(
            id="org1-id",
            created_at=1629300943.9179766,
            display_name="org1",
        )

        self.assertEqual("org1-id", test_org.id)
        self.assertEqual(1629300943.9179766, test_org.created_at)
        self.assertEqual("org1", test_org.display_name)

    def test_normalize_id(self):
        """
        Test strip id of resource prefix and suffix if they exist.

        """
        self.assertEqual(
            "d4b1c627bd464fe0a5ed940cc8e8e485",
            Org.normalize_id("org-d4b1c627bd464fe0a5ed940cc8e8e485,org")
        )

        self.assertEqual(
            "d4b1c627bd464fe0a5ed940cc8e8e485",
            Org.normalize_id("d4b1c627bd464fe0a5ed940cc8e8e485,org")
        )

        self.assertEqual(
            "d4b1c627bd464fe0a5ed940cc8e8e485",
            Org.normalize_id("org-d4b1c627bd464fe0a5ed940cc8e8e485")
        )

        self.assertEqual(
            "d4b1c627bd464fe0a5ed940cc8e8e485",
            Org.normalize_id("d4b1c627bd464fe0a5ed940cc8e8e485")
        )

    def test_denormalize_id(self):
        """
        Test add id resource prefix and suffix if they don't exist.

        """
        self.assertEqual(
            "org-d4b1c627bd464fe0a5ed940cc8e8e485,org",
            Org.denormalize_id("org-d4b1c627bd464fe0a5ed940cc8e8e485,org")
        )

        self.assertEqual(
            "org-d4b1c627bd464fe0a5ed940cc8e8e485,org",
            Org.denormalize_id("d4b1c627bd464fe0a5ed940cc8e8e485,org")
        )

        self.assertEqual(
            "org-d4b1c627bd464fe0a5ed940cc8e8e485,org",
            Org.denormalize_id("org-d4b1c627bd464fe0a5ed940cc8e8e485")
        )

        self.assertEqual(
            "org-d4b1c627bd464fe0a5ed940cc8e8e485,org",
            Org.denormalize_id("d4b1c627bd464fe0a5ed940cc8e8e485")
        )

    def test_get_org(self):
        """
        Test get org for specified org_id.

        """
        self.mock_client.execute = mock.Mock()
        self.mock_client.execute.side_effect = [
            {
                "org": {
                    "id": "org1-id",
                    "created_at": 1630515986.9949625,
                    "display_name": "org1"
                }
            }
        ]

        org = get_org("org1-id", client=self.mock_client)

        self.assertEqual(
            {
                "id": "org1-id",
                "created_at": 1630515986.9949625,
                "display_name": "org1"
            },
            org.to_dict(),
        )

    def test_get_orgs_basic(self):
        """
        Test get orgs for the initialized user.

        """
        self.mock_client.execute = mock.Mock()
        self.mock_client.execute.side_effect = [
            {
                "user": {
                    "membershipList": {
                        "pageInfo": {
                            "endCursor": None
                        },
                        "memberships": [
                            {
                                "org": {
                                    "id": "org1-id",
                                    "created_at": 1571267538.391721,
                                    "display_name": "org1"
                                }
                            },
                            {
                                "org": {
                                    "id": "org2-id",
                                    "created_at": 1630515986.9949625,
                                    "display_name": "org2"
                                }
                            },
                            {
                                "org": {
                                    "id": "org3-id",
                                    "created_at": 1649888079.066764,
                                    "display_name": "org3"
                                }
                            }
                        ]
                    }
                }
            }
        ]

        orgs = get_orgs(client=self.mock_client)

        self.assertEqual(
            [
                {
                    'created_at': 1571267538.391721,
                    'display_name': 'org1',
                    'id': 'org1-id'
                },
                {
                    'created_at': 1630515986.9949625,
                    'display_name': 'org2',
                    'id': 'org2-id'
                },
                {
                    'created_at': 1649888079.066764,
                    'display_name': 'org3',
                    'id': 'org3-id'
                }
            ],
            orgs.to_list(),
        )

    def test_get_orgs_pagination(self):
        """
        Test get orgs for the initialized user, where the user has to
        page through orgs.

        """
        self.mock_client.execute = mock.Mock()
        self.mock_client.execute.side_effect = [
            {
                "user": {
                    "membershipList": {
                        "pageInfo": {
                            "endCursor": "test_check_next"
                        },
                        "memberships": [
                            {
                                "org": {
                                    "id": "org1-id",
                                    "created_at": 1571267538.391721,
                                    "display_name": "org1"
                                }
                            }
                        ]
                    }
                }
            },
            {
                "user": {
                    "membershipList": {
                        "pageInfo": {
                            "endCursor": None
                        },
                        "memberships": [
                            {
                                "org": {
                                    "id": "org2-id",
                                    "created_at": 1630515986.9949625,
                                    "display_name": "org2"
                                }
                            }
                        ]
                    }
                }
            }
        ]

        orgs = get_orgs(client=self.mock_client)

        self.assertEqual(
            [
                {
                    'created_at': 1571267538.391721,
                    'display_name': 'org1',
                    'id': 'org1-id'
                },
                {
                    'created_at': 1630515986.9949625,
                    'display_name': 'org2',
                    'id': 'org2-id'
                }
            ],
            orgs.to_list(),
        )
