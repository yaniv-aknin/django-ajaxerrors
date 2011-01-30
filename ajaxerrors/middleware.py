import sys
import os
import tempfile
from random import randint
import webbrowser
import cPickle as pickle

from django.conf import settings as django_settings
from django.views.debug import technical_500_response

from ajaxerrors.utils import DefaultedAttributes, get_callable, altered_umask

NEW_TAB = 2

settings = DefaultedAttributes(django_settings, dict(
    AJAXERRORS_DO_NOTHING_UNLESS_IN_DEBUG=True,
    AJAXERRORS_WEBBROWSER_OPEN_KWARGS={},
    AJAXERRORS_ADDITIONAL_HANDLERS=[],
    AJAXERRORS_PATH='/ajax-errors',
))

class ShowAJAXErrors(object):
    def __init__(self):
        self.browser = webbrowser.get()
        self.handlers = [get_callable(callable) for callable in settings.AJAXERRORS_ADDITIONAL_HANDLERS]
        self.directory = os.path.join(tempfile.gettempdir(), 'ajax-errors')
        if not os.path.isdir(self.directory):
            with altered_umask(0):
                os.mkdir(self.directory, 01777)

    def process_request(self, request):
        if request.path != settings.AJAXERRORS_PATH:
            return None
        token_path = os.path.join(self.directory, os.path.basename(request.GET.get('token', '')))
        if not os.path.isfile(token_path) or not os.stat(token_path).st_uid == os.getuid():
            return None
        with file(token_path) as handle:
            os.remove(token_path)
            return pickle.load(handle)

    def process_exception(self, request, exception):
        if not request.is_ajax():
            return None

        if not settings.DEBUG and settings.AJAXERRORS_DO_NOTHING_UNLESS_IN_DEBUG:
            return None

        token = '%032x' % (randint(0, 2**128),)
        with altered_umask(0077):
            with file(os.path.join(self.directory, token), 'w') as handle:
                pickle.dump(technical_500_response(request, *sys.exc_info()), handle)
        self.browser.open(request.build_absolute_uri(location=settings.AJAXERRORS_PATH + '?token=' + token),
                          **settings.AJAXERRORS_WEBBROWSER_OPEN_KWARGS)

        response = None
        for handler in self.handlers:
            handler_response = handler(request, *sys.exc_info())
            if handler_response is not None:
                response = handler_response
        return response
