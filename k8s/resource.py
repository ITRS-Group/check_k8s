from k8s.exceptions import MetaNotFound, ConditionsNotFound, StatusNotFound


class Condition:
    def __init__(self, data, meta, textkey="type"):
        assert textkey in data, "Invalid text key: {}".format(textkey)

        self._meta = meta
        self._data = data

        self.type = data["type"]
        self.status = data["status"]
        self.transitioned_at = data["lastTransitionTime"]
        self.text = data[textkey]

    @property
    def message(self):
        return "{kind} {name}: {0} {1} since {2}".format(
            "condition" if self.status == "True" else "condition not",
            self.text,
            self.transitioned_at,
            **self._meta
        )


class Resource:
    def __init__(self, data, kind=None, condition_textkey="type"):
        self._kind = kind or self.__class__.__name__
        self._data = data

        if "metadata" not in data or not data["metadata"]:
            raise MetaNotFound("Malformed response: metadata not found for kind {}".format(self._kind))

        meta = self.meta = dict(kind=self._kind, name=data["metadata"]["name"])

        if "status" not in data or not data["status"]:
            raise StatusNotFound("Malformed response: status not found", **meta)

        status = self._status = data["status"]

        if "conditions" not in status or not len(status["conditions"]):
            raise ConditionsNotFound("No conditions found, cannot check health", **meta)

        self.conditions = [Condition(cond, meta, textkey=condition_textkey) for cond in status["conditions"]]
