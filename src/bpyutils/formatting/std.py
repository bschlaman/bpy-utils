import datetime
from typing import Any, Iterable
from itertools import islice

from .colors import yel


def fmt(obj: datetime.datetime | float) -> str:
    if isinstance(obj, float):
        return format(obj, ".4f")
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d")
    raise TypeError(f"unsupported type: {type(obj)}")


def compact_repr(target: list | set) -> str:
    """Efficiently generate a compact representation of `target`.
    This function shows up to 4 elements, so anything smaller
    will simply be returned as its default string representation.
    Two elements are printed at the front, and two at the back.

    :param target: the list or set to be compactified
    :returns str representation of the compactified target
    """
    if not isinstance(target, (list, set)):
        raise TypeError("invalid target type: " + type(target))
    if len(target) <= 4:
        return repr(target)
    left = map(str, islice(iter(target), 2))
    right = map(str, islice(iter(target), len(target) -2, None))
    lb, rb = tuple("{}") if isinstance(target, set) else tuple("[]")
    return f"{lb}{str(', '.join(left))}, ... {str(', '.join(right))}{rb}"


def data_print(labeled_data: dict[str, Any]) -> Iterable[str]:
    longest_label_len = max(map(len, labeled_data.keys()))
    total_len = longest_label_len + len(yel(""))
    for label, data in labeled_data.items():
        if isinstance(data, float):
            data = round(data, 5)
        yield f"{yel(str(label))}:".ljust(total_len + 2) + str(data)
