import pytest
import logging

from k8s.ignore import remove_ignored


message = "All checks were successful\n\
Pod name: some message\n\
Pod multiple1: some message\n \
Pod multiple2: some message,\n\
Pod some other text diff_position: some message\n, \
Pod with_symbols,;-!: some message"


def check_message(lines, name):
    for line in lines:
        assert name not in line


def test_ignore_resource_single(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    lines = remove_ignored(message, ["name"])
    assert "name:" in caplog.text
    check_message(lines, "name:")


def test_ignore_resource_single(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    lines = remove_ignored(message, ["name"])
    assert "name:" in caplog.text
    check_message(lines, "name:")


def test_ignore_different_position(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    lines = remove_ignored(message, ["diff_position"])
    assert "diff_position:" in caplog.text
    check_message(lines, "diff_position:")


def test_ignore_with_symbol(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    lines = remove_ignored(message, ["with_symbols,;-!"])
    assert "with_symbols,;-!" in caplog.text
    check_message(lines, "with_symbols,;-!")


def test_ignore_all(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    lines = remove_ignored(message, ["name", "multiple", "diff_position", "with_symbols,;-!"])
    assert len(lines) == 1
    assert "All checks were successful\n" == lines[0]


def test_ignore_all_regex(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    lines = remove_ignored(message, ["\S*"]) 
    assert len(lines) == 1
    assert "All checks were successful\n" == lines[0]
