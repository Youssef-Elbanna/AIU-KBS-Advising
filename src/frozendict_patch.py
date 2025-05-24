import sys
import collections.abc
import collections

# Patch collections.Mapping for Python 3.13+ compatibility
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

# Now import frozendict after the patch
from frozendict import frozendict

# Monkey patch frozendict to inherit from collections.abc.Mapping instead of collections.Mapping
frozendict.__bases__ = (collections.abc.Mapping,) 