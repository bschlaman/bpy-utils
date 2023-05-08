import unittest

import jsonschema.exceptions

from bpyutils.schemas import build_validator


class TestSchemasRefs(unittest.TestCase):
    """Test functionality around constructing schema validators"""

    def setUp(self):
        self.root_schema = {
            "$schema": "http://json-schema.org/draft-2020-12/schema#",
            "description": "Schema for testing purposes",
            "additionalProperties": False,
            "type": "object",
            "required": ["prop0", "prop1"],
            "properties": {"prop0": {"type": "string"}, "prop1": {"type": "string"}},
        }
        self.validator = build_validator(self.root_schema)
        self.sample_template_recipe = {
            "template": "https://schlamalama.com/path1/{api}/{version}/data.json",
            "keyvalues": [
                {"key": "api", "value": "get_data"},
                {"key": "version", "value": "1.0"},
            ],
        }

    def test_basic_failure(self):
        d = {"prop0": "test"}
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.validator.validate(d)

    def test_basic_success(self):
        d = {"prop0": "test0", "prop1": "test1"}
        self.validator.validate(d)

    def test_invalid_ref_path(self):
        self.root_schema["properties"]["prop0"] = { "$ref": "/schemas/common/xyz" }
        print(self.root_schema)
        self.validator = build_validator(self.root_schema)
        d = {"prop0": "test0", "prop1": "test1"}
        with self.assertRaises(jsonschema.exceptions.RefResolutionError):
            self.validator.validate(d)

    def test_invalid_base_ref_path(self):
        self.root_schema["properties"]["prop0"] = { "$ref": "/schemas/common/base/xyz" }
        self.validator = build_validator(self.root_schema)
        d = {"prop0": "test0", "prop1": "test1"}
        with self.assertRaises(jsonschema.exceptions.RefResolutionError):
            self.validator.validate(d)

    def test_can_reference_common_schemas(self):
        self.root_schema["properties"]["prop0"] = {
            "prop0": {"$ref": "/schemas/common/base/template_recipe"},
        }
        self.validator = build_validator(self.root_schema)
        d = {"prop0": self.sample_template_recipe, "prop1": "test1"}
        self.validator.validate(d)

    def test_can_reference_common_base_schemas(self):
        self.root_schema["properties"] = {
            "prop0": {"$ref": "/schemas/common/base/text"},
            "prop1": {"$ref": "/schemas/common/base/python_template"},
        }
        self.validator = build_validator(self.root_schema)
        d = {"prop0": "test0", "prop1": "var = {var}"}
        self.validator.validate(d)


class TestSchemas(unittest.TestCase):
    """Test the actual schemas and subschemas"""

    def setUp(self):
        self.root_schema = {
            "$schema": "http://json-schema.org/draft-2020-12/schema#",
            "description": "Schema for testing purposes",
            "additionalProperties": False,
            "type": "object",
            "required": ["prop0", "prop1"],
            "properties": {"prop0": {"type": "string"}, "prop1": {"type": "string"}},
        }
        self.validator = build_validator(self.root_schema)
        self.sample_template_recipe = {
            "template": "https://schlamalama.com/path1/{api}/{version}/data.json",
            "keyvalues": [
                {"key": "api", "value": "get_data"},
                {"key": "version", "value": "1.0"},
            ],
        }

    def test_basic_failure_with_replacment(self):
        self.root_schema["properties"]["prop0"] = {"type": "number"}
        self.validator = build_validator(self.root_schema)
        d = {"prop0": "test0", "prop1": "test1"}
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.validator.validate(d)

    def test_base_python_template_success_no_template(self):
        self.root_schema["properties"]["prop0"] = {
            "$ref": "/schemas/common/base/python_template",
        }
        self.validator = build_validator(self.root_schema)
        d = {"prop0": "just normal text", "prop1": "test1"}
        self.validator.validate(d)

    def test_base_python_template_success_with_template(self):
        self.root_schema["properties"]["prop0"] = {
            "$ref": "/schemas/common/base/python_template",
        }
        self.validator = build_validator(self.root_schema)
        d = {"prop0": "just {param} text", "prop1": "test1"}
        self.validator.validate(d)

    def test_base_url_template_fail(self):
        self.root_schema["properties"]["prop0"] = {
            "$ref": "/schemas/common/base/url_template",
        }
        self.validator = build_validator(self.root_schema)
        d = {"prop0": "just normal text", "prop1": "test1"}
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.validator.validate(d)

    def test_base_url_template_success(self):
        self.root_schema["properties"]["prop0"] = {
            "$ref": "/schemas/common/base/url_template",
        }
        self.validator = build_validator(self.root_schema)
        d = {"prop0": "https://localhost:80/{api}", "prop1": "test1"}
        self.validator.validate(d)

    def test_base_s3_uri_fail(self):
        self.root_schema["properties"]["prop0"] = {
            "$ref": "/schemas/common/base/s3_uri",
        }
        self.validator = build_validator(self.root_schema)
        d = {"prop0": "https://localhost:80/", "prop1": "test1"}
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.validator.validate(d)

    def test_base_s3_uri_success(self):
        self.root_schema["properties"]["prop0"] = {
            "$ref": "/schemas/common/base/s3_uri",
        }
        self.validator = build_validator(self.root_schema)
        d = {"prop0": "s3://bucket-1/path/path2/file.wav", "prop1": "test1"}
        self.validator.validate(d)
