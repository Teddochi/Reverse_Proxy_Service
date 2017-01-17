from .context import app
import unittest

from .tests import file_requirements, reverse_proxy_service, statistics
from .tests import bonus_1, bonus_2, bonus_3


class TestDriver(unittest.TestCase):

    # Confirm that Run.sh, Tests.sh, and README exist
    def test_file_requirements(self):
        file_requirements.test(self)

    # Test the functionality of the reverse proxy service
    def test_reverse_proxy_service(self):
        reverse_proxy_service.test(self)

    # Test the Slow_requests endpoint
    def test_statistics(self):
        statistics.test(self)

    # Test the first optional requirement
    def test_bonus_1(self):
        bonus_1.test(self)

    # Test the second optional requirement
    def test_bonus_2(self):
        bonus_2.test(self)

    # Test the third optional requirement
    def test_bonus_3(self):
        bonus_3.test(self)