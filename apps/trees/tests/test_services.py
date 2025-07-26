from decimal import Decimal

from django.test import TestCase

from apps.trees.models import PlantedTree, Tree
from apps.trees.services import plant_tree, plant_trees
from apps.users.models import Account, User


class UserPlantTreeMethodsTestCase(TestCase):
    def setUp(self) -> None:  # noqa: D401, N802
        self.account = Account.objects.create(name='Forest')

        self.user = User.objects.create_user(
            username='fulano', email='ful@email.com', password='password'
        )

        self.user.accounts.add(self.account)

        self.tree1 = Tree.objects.create(
            name='Ipê Amarelo', scientific_name='Handroanthus albus'
        )
        self.tree2 = Tree.objects.create(
            name='Sakura', scientific_name='Cerasus serrulata'
        )

    def test_plant_tree_creates_planted_tree(self) -> None:
        """Calling plant_tree service should persist and link a instance."""
        planted = plant_tree(
            user=self.user,
            account=self.account,
            tree=self.tree1,
            latitude=Decimal('15.000000'),
            longitude=Decimal('30.000000'),
        )

        assert isinstance(planted, PlantedTree)
        assert planted.user == self.user
        assert planted.account == self.account
        assert planted.tree == self.tree1

        assert PlantedTree.objects.filter(id=planted.id).exists()

    def test_plant_trees_bulk_creates_planted_trees(self) -> None:
        """Calling plant_trees should create multiple PlantedTree records."""
        EXPECTED_TREES = 2
        plants_input = [
            (
                self.tree1,
                (
                    Decimal('12.000000'),
                    Decimal('34.000000'),
                ),
            ),
            (
                self.tree2,
                (
                    Decimal('56.000000'),
                    Decimal('78.000000'),
                ),
            ),
        ]

        planted_list = plant_trees(
            user=self.user, account=self.account, plants=plants_input
        )

        assert len(planted_list) == EXPECTED_TREES
        for planted in planted_list:
            assert isinstance(planted, PlantedTree)
            assert planted.user == self.user
            assert planted.account == self.account

        assert (
            PlantedTree.objects.filter(user=self.user).count()
            == EXPECTED_TREES
        )
