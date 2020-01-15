import sys

from collections import namedtuple

from k8s.consts import State, PERFDATA_SEPARATOR


Output = namedtuple("Output", ["state", "message", "channel"])


class Result:
    def __init__(self, cls, items):
        self._messages = {}
        self._perfdata = {v.value: 0 for v in cls.PerfdataMapping}
        conditions = []
        conditions.extend([cls(i).conditions for i in items])

        for r in conditions:
            message, state, perfkey = r
            self._add_message(state, message)
            self._perfdata[perfkey.value] += 1

    def _add_message(self, state, message):
        if state not in self._messages:
            self._messages[state] = []

        self._messages[state].append(message)

    @property
    def perfdata(self):
        return ["{}={}".format(k, v) for k, v in self._perfdata.items()]

    def _get_output(self, state, topic, channel=sys.stderr):
        message = "{0}\n{conditions}|{perfdata}".format(
            topic,
            conditions="\n".join(self._messages[state]),
            perfdata=PERFDATA_SEPARATOR.join(self.perfdata)
        )
        return Output(state, message, channel)

    @property
    def output(self):
        def severity(level):
            return level in self._messages

        if severity(State.CRITICAL):
            return self._get_output(State.CRITICAL, "One or more errors were detected")
        elif severity(State.WARNING):
            return self._get_output(State.WARNING, "One or more warnings were detected")

        return self._get_output(State.OK, "All checks were successful", channel=sys.stdout)
