from typing import Any

import jsonschema

from .common import BASE, TEMPLATE_RECIPE


def build_validator(root_schema: dict[str, Any]) -> jsonschema.Draft202012Validator:
    resolver = jsonschema.RefResolver.from_schema(
        root_schema,
        store={
            BASE["$id"]: BASE,
            TEMPLATE_RECIPE["$id"]: TEMPLATE_RECIPE,
        },
    )

    return jsonschema.Draft202012Validator(
        schema=root_schema,
        resolver=resolver,
        format_checker=jsonschema.FormatChecker(),
    )
