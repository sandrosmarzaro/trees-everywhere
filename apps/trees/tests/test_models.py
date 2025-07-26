from http import HTTPStatus
from uuid import UUID

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.trees.models import PlantedTree, Tree
from apps.users.models import Account, User


class PlantedTreeViewsTestCase(TestCase):
    def setUp(self) -> None:  # noqa: D401, N802
        self.account1 = Account.objects.create(name='Reforestation')
        self.account2 = Account.objects.create(name='Protected Zone')

        self.user1 = User.objects.create_user(
            username='fulano', email='fulano@email.com', password='test1234'
        )
        self.user2 = User.objects.create_user(
            username='ciclano', email='ciclano@email.com', password='abc123'
        )
        self.user3 = User.objects.create_user(
            username='euclaciano', email='eu@email.com', password='password'
        )

        self.user1.accounts.add(self.account1)
        self.user2.accounts.add(self.account1)
        self.user3.accounts.add(self.account2)

        self.tree1 = Tree.objects.create(
            name='Ipê Amarelo', scientific_name='Handroanthus albus'
        )
        self.tree2 = Tree.objects.create(
            name='Sakura', scientific_name='Cerasus serrulata'
        )

        self.client = APIClient()
        url = reverse('trees:planted-tree-create')

        self.client.force_authenticate(user=self.user1)
        data = {
            'account_id': self.account1.id,
            'tree_id': self.tree1.id,
            'latitude': '12.345678',
            'longitude': '-12.345678',
        }
        response = self.client.post(url, data)
        assert response.status_code == HTTPStatus.CREATED
        self.user1_tree1 = PlantedTree.objects.get(id=response.data['id'])

        data = {
            'account_id': self.account1.id,
            'tree_id': self.tree2.id,
            'latitude': '11.111111',
            'longitude': '22.222222',
        }
        response = self.client.post(url, data)
        assert response.status_code == HTTPStatus.CREATED
        self.user1_tree2 = PlantedTree.objects.get(id=response.data['id'])

        self.client.force_authenticate(user=self.user2)
        data = {
            'account_id': self.account1.id,
            'tree_id': self.tree1.id,
            'latitude': '33.333333',
            'longitude': '44.444444',
        }
        response = self.client.post(url, data)
        assert response.status_code == HTTPStatus.CREATED
        self.user2_tree = PlantedTree.objects.get(id=response.data['id'])

        self.client.force_authenticate(user=self.user3)
        data = {
            'account_id': self.account2.id,
            'tree_id': self.tree2.id,
            'latitude': '55.555555',
            'longitude': '66.666666',
        }
        response = self.client.post(url, data)
        assert response.status_code == HTTPStatus.CREATED
        self.user3_tree = PlantedTree.objects.get(id=response.data['id'])

    def test_list_my_planted_trees(self) -> None:
        """Authenticated user should see only their own planted trees."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('trees:planted-tree-list-by-user')
        response = self.client.get(url)

        assert response.status_code == HTTPStatus.OK

        returned_ids = {UUID(item['id']) for item in response.data}
        expected_ids = {self.user1_tree1.id, self.user1_tree2.id}
        assert returned_ids == expected_ids

    def test_access_other_user_planted_tree_returns_403(self) -> None:
        """Trying to retrieve another user's planted tree returns 403."""
        self.client.force_authenticate(user=self.user1)

        url = reverse('trees:planted-tree-detail', args=[self.user2_tree.id])
        response = self.client.get(url)

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_list_planted_trees_by_accounts(self) -> None:
        """User sees plantings for all members of their accounts."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('trees:planted-tree-list-by-accounts')
        response = self.client.get(url)

        assert response.status_code == HTTPStatus.OK

        returned_ids = {UUID(item['id']) for item in response.data}
        expected_ids = {
            self.user1_tree1.id,
            self.user1_tree2.id,
            self.user2_tree.id,
        }
        assert returned_ids == expected_ids
        assert self.user3_tree.id not in returned_ids
