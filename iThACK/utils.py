from typing import Tuple, Dict, Any


def _unpack_dict(**kwargs: Dict) -> Tuple:
    return tuple(kwargs.values())


def attrs(template: Any) -> Tuple:
    return _unpack_dict(**template.__dict__)
