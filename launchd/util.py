# -*- coding: utf-8 -*-

from Foundation import NSDictionary, NSArray
from objc._pythonify import OC_PythonLong, OC_PythonFloat
from objc import pyobjc_unicode


def convert_NS_to_python(val):
    if isinstance(val, (pyobjc_unicode, str)):
        return str(val)
    elif isinstance(val, (OC_PythonLong, int)):
        return int(val)
    elif isinstance(val, (NSDictionary, dict)):
        return convert_NSDictionary_to_dict(val)
    elif isinstance(val, (NSArray, list, tuple)):
        return convert_NSArray_to_tuple(val)
    elif isinstance(val, (OC_PythonFloat,)):
        return float(val)
    else:
        raise TypeError("Unknown type '%s': '%r'!" % (str(type(val)), repr(val)))


def convert_NSArray_to_tuple(nsarray):
    return ((convert_NS_to_python(val) for val in nsarray),)


def convert_NSDictionary_to_dict(nsdict):
    return {convert_NS_to_python(k): convert_NS_to_python(nsdict[k]) for k in nsdict}
