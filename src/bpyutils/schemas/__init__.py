from typing import Any

import jsonschema

from .common import BASE, TEMPLATE_RECIPE


class CommonRefResolver(jsonschema.RefResolver):
    """Custom RefResolver that enables referencing subschemas
    with /schemas/common/{subschema}
    """

    def resolve_remote(self, uri):
        # base has to come first
        if uri.startswith(BASE["$id"]):
            return BASE
        if uri == TEMPLATE_RECIPE["$id"]:
            return TEMPLATE_RECIPE
        return super().resolve_remote(uri)


def build_validator(root_schema: dict[str, Any]) -> jsonschema.Draft202012Validator:
    resolver = CommonRefResolver.from_schema(root_schema)
    return jsonschema.Draft202012Validator(
        schema=root_schema,
        resolver=resolver,
        format_checker=jsonschema.FormatChecker(),
    )
