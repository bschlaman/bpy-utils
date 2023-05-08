"""Common schemas which can be referenced by other schemas.
Do not import schemas prefixed with "_" directly.  Instead, import
the TEMPLATES only.
"""

__all__ = ["BASE", "TEMPLATE_RECIPE"]

_PYTHON_TEMPLATE = {"format": "uri-template"}

_URL_TEMPLATE = {"pattern": r"^https?://[^\s]*$", "format": "uri-template"}

_S3_URI = {"pattern": r"^s3:\/\/([\w\.-]+\/)*[\w\.-]+\.yml$"}

_RECIPE_KEYVALUES = {
    "description": (
        "List of objects that have both a key string and a value. Useful for injecting"
        " both keys and values into a template."
    ),
    "type": "array",
    "uniqueItems": True,
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": ["key", "value"],
        "properties": {
            "key": {"type": "string", "minLength": 1},
            "value": {"type": "string"},
        },
    },
}

TEMPLATE_RECIPE = {
    "$schema": "http://json-schema.org/draft-2020-12/schema#",
    "$id": "/schemas/common/template_recipe",
    "schema_version": "1.0",
    "description": (
        "A template plus an array of key value pairs that are injected into the"
        " template"
    ),
    "type": "object",
    "additionalProperties": False,
    "required": ["template", "keyvalues"],
    "properties": {
        # TODO: should change this to /template
        "template": {"$ref": "/schemas/common/base/url_template"},
        "keyvalues": {"$ref": "/schemas/common/base/keyvalues"},
    },
}

# TEMPLATE_RECIPE_CARTESIAN = {
#     "$schema": "http://json-schema.org/draft-2020-12/schema#",
#     "$id": "/schemas/common/template_recipe_cartesian",
#     "schema_version": "1.0",
#     "description": "One or more templates plus an array of keys with one or more values to generate a caresian product of templates and key-value pairs",
# }

BASE = {
    "$schema": "http://json-schema.org/draft-2020-12/schema#",
    "$id": "/schemas/common/base",
    "schema_version": "1.0",
    "description": (
        "A base collection of shared JSON schemas"
        " representing common patterns and data structures"
        " used across applications"
    ),
    "$defs": {
        "python_template": _PYTHON_TEMPLATE,
        "url_template": _URL_TEMPLATE,
        "s3_uri": _S3_URI,
        "text": {"type": "string", "minLength": 2},
        "keyvalues": _RECIPE_KEYVALUES,
    },
}
