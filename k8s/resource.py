class ResourceMeta(type):
    def __call__(cls, *args, **kwargs):
        resource = super(ResourceMeta, cls).__call__(*args, **kwargs)

        # assert resource.__kind__, "Resource {} must have a __kind__".format(cls)

        return resource


class Resource(metaclass=ResourceMeta):
    def __init__(self, data, kind=None):
        self._data = data
        self._kind = kind or self.__class__.__name__
        self._status = data["status"]

    @property
    def name(self):
        return self._data["metadata"]["name"]

    @property
    def meta(self):
        return dict(kind=self._kind, name=self.name)

    @property
    def conditions(self):
        return self._status["conditions"]
