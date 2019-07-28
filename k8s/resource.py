class Condition:
    def __init__(self, data, meta, text_key="message"):
        assert text_key in data, "Invalid text key: {}".format(text_key)

        self._meta = meta
        self._data = data

        self.type = data["type"]
        self.status = data["status"]
        self.transitioned_at = data["lastTransitionTime"]
        self.text = data[text_key]

    @property
    def message(self):
        return "{kind} {name}: {0} since {1}".format(
            self.text,
            self.transitioned_at,
            **self._meta
        )


class ResourceMeta(type):
    def __call__(cls, *args, **kwargs):
        resource = super(ResourceMeta, cls).__call__(*args, **kwargs)

        # assert resource.__kind__, "Resource {} must have a __kind__".format(cls)

        return resource


class Resource(metaclass=ResourceMeta):
    def __init__(self, data, kind=None, condition_text_key="message"):
        self._data = data
        self._kind = kind or self.__class__.__name__
        self._status = data["status"]
        self._conditions = [
            Condition(cond, self.meta, text_key=condition_text_key)
            for cond in self._status["conditions"]
        ]

    @property
    def name(self):
        return self._data["metadata"]["name"]

    @property
    def meta(self):
        return dict(kind=self._kind, name=self.name)

    @property
    def conditions(self):
        return self._conditions
