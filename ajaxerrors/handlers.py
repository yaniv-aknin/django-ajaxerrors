import os

from django.http import HttpResponse

from ajaxerrors.utils import only_on

def return_empty_dict(request, error_type, error_value, traceback_object):
    return HttpResponse('{}')

@only_on('Darwin')
def growlnotify(request, error_type, error_value, traceback_object):
    def shellquote(s):
        return str(s).replace("'", "'\\''")
    ASSUMED_CHROME_DIRECTORY='/Applications/Google Chrome.app'
    ASSUMED_SAFARI_DIRECTORY='/Applications/Safari.app'
    cmdline = ("growlnotify --message 'AJAX 500: %s: %s'" %
               (shellquote(error_type.__name__), shellquote(error_value)))
    agent = request.META.get('HTTP_USER_AGENT', '')
    if 'Chrome' in agent and os.path.isdir(ASSUMED_CHROME_DIRECTORY):
        cmdline += " --appIcon %r" % (ASSUMED_CHROME_DIRECTORY,)
    elif "Safari" in agent:
        cmdline += " --appIcon %r" % (ASSUMED_SAFARI_DIRECTORY,)
    os.system(cmdline)
