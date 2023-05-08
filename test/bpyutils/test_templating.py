import unittest

from bpyutils.templating.injection import RecipeInjector


class TestTemplating(unittest.TestCase):
    def setUp(self):
        self.test_template = "https://schlamalama.com/path1/{api}/{version}/data.json"
        self.test_schema = [
            {"key": "api", "value": "get_data"},
            {"key": "version", "value": "1.0"},
        ]
        self.injector = RecipeInjector(self.test_template)

    def test_template_injection(self):
        self.assertEqual(
            self.injector.construct_string(self.test_schema),
            "https://schlamalama.com/path1/get_data/1.0/data.json",
        )

    def test_template_injection_too_few_keyvalues(self):
        self.test_template = "https://schlamalama.com/path1/{api}/{version}/{file}"
        with self.assertRaises(Exception) as e:
            self.injector.construct_string(self.test_schema)
            self.assertIsInstance(e.exception, KeyError)

    def test_template_injection_too_many_keyvalues(self):
        self.test_schema.append({"key": "xxx", "value": "yyy"})
        with self.assertRaises(Exception) as e:
            self.injector.construct_string(self.test_schema)
            self.assertIsInstance(e.exception, AssertionError)
