import pytest
import logging

from k8s.ignore import get_expression_pattern,is_ignored_resource


message = ["Pod name: some message",
"Pod multiple1: some message",
"Pod multiple2: some message",
"Pod some other text diff_position: some message",
"Pod with_symbols,;-!: some message"]

def ignore_from_list(lines, expressions):
    count = 0
    expression_patterns = get_expression_pattern(expressions)
    for line in lines:
        if(is_ignored_resource(line, expression_patterns)):
            count+=1
    return count


def test_ignore_resource_single(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    count = ignore_from_list(message, ["name"])
    assert "name:" in caplog.text
    assert count == 1


def test_ignore_resource_multiple(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    count = ignore_from_list(message, ["multiple"])
    assert "multiple1:" in caplog.text
    assert "multiple2:" in caplog.text
    assert count == 2


def test_ignore_different_position(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    count = ignore_from_list(message, ["diff_position"])
    assert "diff_position:" in caplog.text
    assert count == 1


def test_ignore_with_symbol(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    count = ignore_from_list(message, ["with_symbols,;-!"])
    assert "with_symbols,;-!" in caplog.text
    assert count == 1


def test_ignore_all(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    count = ignore_from_list(message, ["name", "multiple", "diff_position", "with_symbols,;-!"])
    assert count == 5


def test_ignore_all_regex(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.clear()
    count = ignore_from_list(message, ["\S*"]) 
    assert count == 5
