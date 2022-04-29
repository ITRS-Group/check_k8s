import re
import logging

resource_pattern = re.compile(r"\S+:{1}")


def remove_ignored(message, expressions):
    expression_patterns = []
    for expression in expressions:
        expression_patterns.append(re.compile(r"{}".format(expression)))

    lines = message.splitlines(True)
    lines[1:] = [
        line for line in lines[1:] if not is_ignored_resource(line, expression_patterns)
    ]
    return lines


def is_ignored_resource(line, expressions):
    word = re.search(resource_pattern, line)
    for expression in expressions:
        found = re.search(expression, word.group())
        if found:
            logging.debug("Ignoring results for " + word.group())
            return True
    return False
