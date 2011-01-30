from functools import wraps
import os
from contextlib import contextmanager
import platform

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

class DefaultedAttributes(object):
    def __init__(self, underlying, defaults):
        self.underlying = underlying
        self.defaults = defaults
    def __getattr__(self, name):
        if hasattr(self.underlying, name):
            return getattr(self.underlying, name)
        try:
            return self.defaults[name]
        except KeyError, error:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.underlying.__class__.__name__, name))

# WARNING: This is a near copy from django.template.loader.find_template_loader. Maybe I'm blind, but despite django's
#           heavy use of string imports I couldn't find an exposed utility function like this in django's source.
def get_callable(callable):
    if isinstance(callable, basestring):
        module, attr = callable.rsplit('.', 1)
        try:
            mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Error importing ajaxerrors callable %s: "%s"' % (callable, e))
        try:
            callable = getattr(mod, attr)
        except AttributeError, e:
            raise ImproperlyConfigured('Error importing ajaxerrors callable %s: "%s"' % (callable, e))
    return callable

def only_on(system):
    def decor(func):
        @wraps(func)
        def callable(*args, **kwargs):
            if platform.system() != system:
                return
            return func(*args, **kwargs)
        return callable
    return decor

@contextmanager
def altered_umask(umask):
    old_umask = os.umask(umask)
    try:
        yield
    finally:
        os.umask(old_umask)
