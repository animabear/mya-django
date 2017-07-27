# coding=utf-8

import numbers
import collections

def isNum(bar):
    return isinstance(bar, numbers.Number)


def dict_merge(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = dict_merge(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d