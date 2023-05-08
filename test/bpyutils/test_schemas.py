import unittest

import jsonschema.exceptions

from bpyutils.schemas import build_validator


class TestSchemas(unittest.TestCase):
    def setUp(self):
        self.root_schema = {
            "$schema": "http://json-schema.org/draft-2020-12/schema#",
            "additionalProperties": False,
        }
        self.validator = build_validator(self.root_schema)

    def test_base_schemas(self):
        schema = {"hi": "test"}
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.validator.validate(schema)
