from petisco.test_tools import DeployTestBase


class _DeployTestInventory(dict):
    """
    This class implements an inventory that automatically registers classes and functions into a dictionary.
    """

    def add_to(self, container):
        """
        Decorator that automatically adds an asset to the inventory
        Parameters
        ----------
        container: (string) name of inventory entry
        alias: string name to find the asset in the inventory

        Returns
        -------

        """
        if container not in self:

            if not issubclass(container, DeployTestBase):
                raise TypeError(
                    "Only DeployTest objects can be added with the @test_tools decorator"
                )

            self[container.__name__] = container()


deploy_test_inventory = _DeployTestInventory()
deploy_test = deploy_test_inventory.add_to
