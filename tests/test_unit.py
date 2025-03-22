import unittest
from src.additel_sdk.notYetImplemented.unit import Unit

class DummyParent:
    def __init__(self, response=None):
        self._response = response

    def cmd(self, command):
        # We ignore command checks since it's a dummy.
        return self._response

    def send_command(self, command):
        # Dummy implementation for send_command used by other Unit methods.
        pass

class TestUnitTemp(unittest.TestCase):
    def test_get_unit_temp_success(self):
        # When parent.cmd returns a valid response, getUnitTemp should return the split list.
        dummy_response = "Celsius,1"
        parent = DummyParent(response=dummy_response)
        unit = Unit(parent)
        self.assertEqual(unit.getUnitTemp(), ["Celsius", "1"])

    def test_get_unit_temp_failure(self):
        # When parent.cmd returns None, getUnitTemp should raise a ValueError.
        parent = DummyParent(response=None)
        unit = Unit(parent)
        with self.assertRaises(ValueError):
            unit.getUnitTemp()

if __name__ == "__main__":
    unittest.main()