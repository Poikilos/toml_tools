# -*- coding: utf-8 -*-
import os
import sys
import collections

if sys.version_info < (3,7) or sys.implementation.name.lower() == 'ironpython':
    new_dict = collections.OrderedDict
else:
    new_dict = dict


class ReadOnlyDict(object):
    def __init__(self, *args, **kwargs):
        self._dict = new_dict(*args, **kwargs)

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
    
def stem(file_path):
    #type(str) -> str
    return os.path.splitext(os.path.basename(file_path))[0]