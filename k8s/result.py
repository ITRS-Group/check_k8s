import sys

from collections import namedtuple

from k8s.consts import (
    NaemonState,
    PERFDATA_SEPARATOR,
    RESULT_SUCCESS,
    RESULT_CRITICAL,
    RESULT_WARNING,
)
from k8s.ignore import get_expression_pattern, is_ignored_resource

Output = namedtuple("Output", ["state", "message", "channel"])


class Result:
    def __init__(self, cls, items, expressions):
        self._messages = {}
        self._perfdata = {v.value: 0 for v in cls.PerfMap}
        self._expression_patterns = get_expression_pattern(expressions)
        self._register_conditions([cls(i).condition for i in items])

    def _register_conditions(self, conditions):
        """Registers conditions perfdata and messages

        :param conditions: [(message<str>, status<NaemonStatus>), ...]
        """

        for message, status in conditions:
            # Skip adding to result if resource is in ignore list
            if is_ignored_resource(message, self._expression_patterns):
                continue
            if status.state not in self._messages:
                self._messages[status.state] = []

            self._perfdata[status.perfkey.value] += 1
            self._messages[status.state].append(message)

    @property
    def perfdata(self):
        """Converts the Resource's perfdata items into Naemon perfdata string pairs

        Example:
        dict(available=5, unavailable=3) => ["available=5", "unavailable=3"]

        :return: List of Naemon perfdata pairs
        """

        return ["{}={}".format(k, v) for k, v in self._perfdata.items()]

    def _get_output(self, state, summary, channel=sys.stdout):
        """Produces an Output object for accessing Naemon state, messages and channel

        :param state: NaemonState object
        :param summary: Result summary string, e.g. "All checks were successful"
        :param channel: Output channel
        :return: Output object
        """

        # messages can be empty if all are ignored
        if len(self._messages):
            message = "{0}\n{conditions}|{perfdata}\n".format(
                summary,
                conditions="\n".join(self._messages[state]),
                perfdata=PERFDATA_SEPARATOR.join(self.perfdata),
            )
        else:
            message = "{0}\n|{perfdata}\n".format(
                summary,
                perfdata=PERFDATA_SEPARATOR.join(self.perfdata),
            )
        return Output(state, message, channel)

    @property
    def output(self):
        def severity(level):
            return level in self._messages

        if severity(NaemonState.CRITICAL):
            return self._get_output(NaemonState.CRITICAL, RESULT_CRITICAL)
        elif severity(NaemonState.WARNING):
            return self._get_output(NaemonState.WARNING, RESULT_WARNING)

        return self._get_output(NaemonState.OK, RESULT_SUCCESS, channel=sys.stdout)
