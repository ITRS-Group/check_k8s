class ResourceMeta(type):
    def __call__(cls, *args, **kwargs):
        resource = super(ResourceMeta, cls).__call__(*args, **kwargs)

        assert resource.__kind__, "Resource {} must have a __kind__".format(cls)

        return resource


class Resource(metaclass=ResourceMeta):
    __kind__ = None

    def __init__(self, client):
        self.client = client

    def _request(self, **kwargs):
        return self.client.get(self.__kind__, **kwargs).get("items")

    def check(self, *args, **kwargs):
        raise NotImplementedError
