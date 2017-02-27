# coding: utf-8
# Author: Allen Zou
# 2017/2/23 下午11:50
import yaml

class YamlConfigurator:
    def __init__(self, src, delimiter="/"):
        self._yaml = src
        self._source = yaml.load(src)
        self._cache = {}
        self._delimiter = delimiter

    @property
    def yaml(self):
        return self._yaml

    @property
    def source(self):
        return self._source.copy()

    def get(self, key):
        key = key.lstrip(self._delimiter)
        key = key.rstrip(self._delimiter)
        if key in self._cache:
            return self._cache[key]
        sub = {}
        for k, v in self._source.items():
            prefix = "{key}{delimiter}".format(key=key, delimiter=self._delimiter)
            if k == key:
                sub[""] = v
            elif k.startswith(prefix):
                final_key = k[len(prefix):]
                sub[final_key] = v
        if not sub:
            return None
        if len(sub) == 1 and "" in sub:
            return sub[""]
        return YamlConfigurator(yaml.dump(sub), self._delimiter)

    def get_children(self, prefix=None):
        if prefix is None:
            children = {}
            keys = self._source.keys()
            unique_keys = set()
            for k in keys:
                child_key = k.split(self._delimiter, 1)[0]
                unique_keys.add(child_key)
            for k in unique_keys:
                children[k] = self.get(k)
            return children
        child_tree = self.get(prefix)
        if not isinstance(child_tree, YamlConfigurator):
            raise TypeError("Invalid key")
        return child_tree.get_children()

    def _time_parse(self, val):
        try:
            if val.endswith("s"):
                sec = int(val[:len(val) - 1])
            elif val.endswith("m"):
                sec = int(val[:len(val) - 1]) * 60
            elif val.endswith("h"):
                sec = int(val[:len(val) - 1]) * 60 * 60
            elif val.endswith("d"):
                sec = int(val[:len(val) - 1]) * 60 * 60 * 24
            else:
                raise Exception()
        except:
            raise Exception("Invalid format of time configuration: `%s`" % val)
        return sec * 1000

    def get_time(self, key):
        v = self.get(key)
        if v:
            return self._time_parse(v)
        return None

    def __repr__(self):
        return "<YamlConfigurator at 0x%x: %s>" % (id(self), self._source)

    _GLOBAL_CONF = None
    @classmethod
    def init_global_configurator(cls, src, delimiter="/"):
        cls._GLOBAL_CONF = cls(src, delimiter)

    @classmethod
    def get_global_configurator(cls):
        return cls._GLOBAL_CONF
