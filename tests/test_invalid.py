# -*- coding: utf-8 -*-
from datetime import time

import pytest

from . import toml_tools

from toml_tools._re import timezone

def test_invalid_type_nested():
    with pytest.raises(TypeError):
        toml_tools.dumps({"bytearr": bytearray()})


def test_invalid_time():
    offset_time = time(23, 59, 59, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        toml_tools.dumps({"offset time": offset_time})
