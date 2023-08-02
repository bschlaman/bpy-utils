"""This module provides utilities for injecting templates
with keyvalues"""


import string
from typing import Union


class RecipeInjector:
    """Utility for injecting keys and values into a template.
    Together, the template and keyvalues are a 'Recipe'.
    """

    def __init__(self, template: str):
        self.template = template

    def _validate_template_formatable(self, keyvalues: list[dict[str, str]]):
        """Validates if `template` placeholders are all present
        in `keyvalues`
        """
        try:
            # 1) test for excess fields
            # coerce key to string to supress type warning
            dummy_keyvalues = {str(_["key"]): "" for _ in keyvalues}
            self.template.format(**dummy_keyvalues)
            # 2) test for excess keys
            assert set(
                key for _, key, _, _ in string.Formatter().parse(self.template) if key
            ) == set(_["key"] for _ in keyvalues)
        except (AssertionError, KeyError) as e:
            raise Exception(f"parameter mismatch: {e!r}") from e

    def _construct_kv_dict(self, keyvalues: list[dict[str, str]]):
        return {kv["key"]: kv["value"] for kv in keyvalues}

    def construct_string(self, keyvalues: list[dict[str, str]]):
        # surface any obvious problems with the template and keyvalues
        self._validate_template_formatable(keyvalues)
        return self.template.format(**self._construct_kv_dict(keyvalues))


class SchemaInjectorCartesian:
    """
    DEPRECATED
    ==========

    Injector for one template and many values.  Deprecated
    in favor of either many templates + many values or single template single value
    """

    def __init__(self, template: str):
        self.template = template

    def _validate_template_formatable(
        self, schema: list[dict[str, Union[str, list[str]]]]
    ):
        """Validates if `template` placeholders are all present
        in `schema`
        """
        try:
            # 1) test for excess fields
            # coerce key to string to supress type warning
            dummy_parameters = {str(_["key"]): "" for _ in schema}
            self.template.format(**dummy_parameters)
            # 2) test for excess keys
            assert set(
                key for _, key, _, _ in string.Formatter().parse(self.template) if key
            ) == set(_["key"] for _ in schema)
        except (AssertionError, KeyError) as e:
            raise Exception(f"parameter mismatch: {e!r}") from e

    def _inject_schema_parameters(self, schema: list[dict[str, Union[str, list[str]]]]):
        def _format_rec(root, i=0):
            if i == len(schema):
                return [root]
            key = str(schema[i]["key"])
            return [
                path
                for value in schema[i]["values"]
                for path in _format_rec(root.replace("{" + key + "}", value), i + 1)
            ]

        return _format_rec(self.template)

    def construct_string(self, schema: list[dict[str, Union[str, list[str]]]]):
        # surface any obvious problems with the path schema
        self._validate_template_formatable(schema)
        # this util can generate a cartesian product, but for now,
        # we are only interested in a single result
        return self._inject_schema_parameters(schema)[0]
