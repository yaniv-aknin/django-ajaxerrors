import sys
from random import randint
import webbrowser

from django.conf import settings as django_settings
from django.views.debug import technical_500_response

from ajaxerrors.utils import DefaultedAttributes, get_callable

NEW_TAB = 2

settings = DefaultedAttributes(django_settings, dict(
    AJAXERRORS_DO_NOTHING_UNLESS_IN_DEBUG=True,
    AJAXERRORS_WEBBROWSER_OPEN_KWARGS={},
    AJAXERRORS_ADDITIONAL_HANDLERS=[],
))

class ShowAJAXErrors(object):
    def __init__(self):
        self.technical_responses = {}
        self.browser = webbrowser.get()
        self.handlers = [get_callable(callable) for callable in settings.AJAXERRORS_ADDITIONAL_HANDLERS]
    def process_request(self, request):
        return self.technical_responses.pop(request.path, None)
    def process_exception(self, request, exception):
        if not request.is_ajax():
            return None

        if not settings.DEBUG and settings.AJAXERRORS_DO_NOTHING_UNLESS_IN_DEBUG:
            return None

        token = '/ajax-errors/%032x' % (randint(0, 2**128),)
        self.technical_responses[token] = technical_500_response(request, *sys.exc_info())
        self.browser.open(request.build_absolute_uri(location=token), **settings.AJAXERRORS_WEBBROWSER_OPEN_KWARGS)

        response = None
        for handler in self.handlers:
            handler_response = handler(request, *sys.exc_info())
            if handler_response is not None:
                response = handler_response
        return response
