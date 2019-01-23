import json
import unittest

from validator_manager.validator import Validator


class TestServices(unittest.TestCase):
    def load_configuration(self, path):
        with open(path) as f:
            out_data = json.load(f)

        self.config_dict = out_data

    def test_validator(self):
        path = "sample.json"
        self.load_configuration(path)
        validator = Validator(self.config_dict)
        self.assertTrue(validator.get_status())
        self.assertListEqual(validator.get_messages(), [])

    def test_validator_failure(self):
        config_dict = {"entities": [{"model": "Test"}]}
        validator = Validator(config_dict)
        self.assertFalse(validator.get_status())
        expected_result = ["{'entities.0.name': 'Required'}"]
        self.assertListEqual(validator.get_messages(), expected_result)
