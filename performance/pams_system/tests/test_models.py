from pams_system.tests.base_test import BaseTest
from pams_system.models.maps import MapSet

class MapTest(BaseTest):

    def test_create_map_succeeds(self):
        """
        createing  map models successfully
        """
        map_ = self.create_map()
        self.assertIsInstance(map_,MapSet)


    