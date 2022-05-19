import re
import logging

resource_pattern = re.compile(r"\S+:{1}")


def get_expression_pattern(expressions):
    expression_patterns = []
    if expressions:
        for expression in expressions:
            expression_patterns.append(re.compile(r"{}".format(expression)))
    return expression_patterns


def is_ignored_resource(line, expressions):
    word = re.search(resource_pattern, line)
    for expression in expressions:
        found = re.search(expression, word.group())
        if found:
            logging.debug("Ignoring results for " + word.group())
            return True
    return False
