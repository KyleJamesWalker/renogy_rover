"""Schema and Properties"""
from expiringdict import ExpiringDict
from renogy_rover import config
from renogy_rover.driver import client


class Property:
    """Simple Address Property"""
    def __init__(self, addr, length=1):
        self.addr = addr
        self.length = length

    def get_value(self):
        """Get Value from Driver"""
        return client.read(self.addr, self.length)

    def set_value(self, x):
        """Write Value to Driver"""
        raise NotImplementedError("TODO: Write RAW Value, No Processing")


class Numeric(Property):
    """Read Only Numeric Property with Multiplier"""
    def __init__(self, addr, length=1, multiplier=1, unit=None):
        super().__init__(addr, length=length)
        self.multiplier = multiplier
        self.unit = unit if unit is not None else ''

    def get_value(self):
        data = super().get_value()[0]
        # Make sure floats only go to 2 digits
        return round(data * self.multiplier, 2)

    def set_value(self, x):
        raise NotImplementedError("Set not supported")


class SchemaBase(type):
    """Metaclass for Renogy Schemas"""
    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        cls._properties = {}

        for key, value in dct.items():
            if issubclass(value.__class__, Property):
                cls._properties[key] = value
                setattr(cls, key, property(
                    mcs._proxy_cached_getter(cls, key),
                    mcs._proxy_cached_setter(cls, key),
                ))

        return cls

    @classmethod
    def _proxy_cached_getter(mcs, owner, key):
        """Get cached property value"""
        def get_value(self):
            try:
                return self._cache[key]
            except KeyError:
                val = self._properties[key].get_value()
                self._cache[key] = val
                return val
        return get_value

    @classmethod
    def _proxy_cached_setter(mcs, owner, key):
        """Set property value and clear cache"""
        def set_value(self, x):
            self._properties[key].set_value(x)
            try:
                del self._cache[key]
            except KeyError:
                pass
        return set_value


class Schema(metaclass=SchemaBase):
    """Base Schema with Cache"""
    def __init__(self):
        self._cache = ExpiringDict(
            max_len=100,
            max_age_seconds=config.cache_ttl,
        )

    def dump(self):
        """Dump all properties to a dictionary"""
        return {x: getattr(self, x) for x in self._properties}
