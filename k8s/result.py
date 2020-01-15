import sys

from collections import namedtuple

from k8s.consts import State


Output = namedtuple("Output", ["state", "message", "channel"])


class Result:
    conditions = {}
    _perfdata_mappings = dict(
        ok="ok",
        warning="warning",
        critical="critical",
        unknown="unknown"
    )

    def __init__(self, items, perfdata_mappings=None):
        self._perfdata_mappings.update(perfdata_mappings or {})

        for i in items:
            state, message = i.condition
            if state not in self.conditions:
                self.conditions[state] = []

            self.conditions[state].append(message)

    @property
    def perfdata(self):
        for k, v in self._perfdata_mappings.items():
            count = len(getattr(self, k))
            yield "{}={}".format(v, count)

    def _format_output(self, message, conditions):
        return "{0}\n{conditions}|{perfdata}".format(
            message,
            conditions="\n".join(conditions),
            perfdata=" ".join(self.perfdata)
        )

    @property
    def output(self):
        if self.critical:
            return Output(
                State.CRITICAL,
                self._format_output("One or more errors were found", self.critical),
                sys.stderr
            )
        elif self.warning:
            return Output(
                State.WARNING,
                self._format_output("One or more warnings were found", self.warning),
                sys.stderr
            )

        return Output(
            State.OK,
            self._format_output("All checks were successful", self.ok),
            sys.stdout
        )

    def _get_conditions(self, state):
        if state not in self.conditions:
            return []

        return self.conditions[state]

    @property
    def ok(self):
        return self._get_conditions(State.OK)

    @property
    def warning(self):
        return self._get_conditions(State.WARNING)

    @property
    def critical(self):
        return self._get_conditions(State.CRITICAL)

    @property
    def unknown(self):
        return self._get_conditions(State.UNKNOWN)
