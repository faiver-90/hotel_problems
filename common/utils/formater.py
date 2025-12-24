from typing import Any


def formater_str_models(*args: Any) -> str:
    return " | ".join(map(str, args))
