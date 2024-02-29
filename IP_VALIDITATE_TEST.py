import unittest
from firewall import AdvancedFirewallApp  # Adjust the import statement as per your script's name

class TestIPValidation(unittest.TestCase):

    def test_validate_ip_valid(self):
        self.assertTrue(AdvancedFirewallApp.validate_ip("192.168.1.1"))
        self.assertTrue(AdvancedFirewallApp.validate_ip("10.10.10.0/24"))

    def test_validate_ip_invalid(self):
        self.assertFalse(AdvancedFirewallApp.validate_ip("999.999.999.999"))
        self.assertFalse(AdvancedFirewallApp.validate_ip("abcd"))
