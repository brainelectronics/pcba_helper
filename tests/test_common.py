#!/usr/bin/env python3

import logging
from pathlib import Path

import pytest

from pcba_helper.common import (
    LOG_LEVELS,
    create_hash,
    read_file,
    save_file,
    verify_password,
)


def test_log_levels() -> None:
    assert LOG_LEVELS[0] == logging.CRITICAL
    assert LOG_LEVELS[1] == logging.ERROR
    assert LOG_LEVELS[2] == logging.WARNING
    assert LOG_LEVELS[3] == logging.INFO
    assert LOG_LEVELS[4] == logging.DEBUG

@pytest.mark.parametrize(
    "name, data",
    [
        ("txt", "Hello World"),
        ("txt", "Hello World\nFrom testing"),
        ("raise", "Something"),
    ]
)
def test_read_save(name: str, data: str, tmp_path: Path) -> None:
    p = tmp_path / f"data.{name}"

    save_file(filename=p, content=data)

    if name == "txt":
        name = "read"
        if "\n" in data:
            name = "readline"

    assert read_file(filename=p) == data if name != "readline" else data.split()
    assert len(list(tmp_path.iterdir())) == 1

@pytest.mark.parametrize(
    "password",
    [
        ("asdf"),
        ("12qwertz34"),
    ]
)
def test_hash(password: str) -> None:
    tmp_hash = create_hash(password=password)
    assert verify_password(password=password, hash=tmp_hash)
