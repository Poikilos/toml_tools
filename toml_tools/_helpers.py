# -*- coding: utf-8 -*-

class ReadOnlyDict(object):
    def __init__(self, _dict):
        self._dict = _dict

    def __getitem__(self, key):
        return self._dict[key]
    
    def __contains__(self, key):
        return key in self._dict
    
    def keys(self):
        return self._dict.keys()
    
    def values(self):
        return self._dict.values()
    
    def items(self):
        return self._dict.items()