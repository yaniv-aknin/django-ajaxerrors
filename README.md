django-ajaxerrors
=================

Simple Django middleware that makes it easy to view Django's technical error page for failed AJAX requests by automagically opening them in a different browser window.

The Problem
-----------
I reckon most if not all Django developers know about Django's useful debug-mode unhandled error page (yeah, this [page](http://docs.djangoproject.com/en/dev/topics/http/views/#the-500-server-error-view)). However, when an AJAX request reaches a faulty view, the error page will be received by your AJAX error handled (assuming you even had one), which is almost always not what you want. You want to see the error page rendered as HTML in your browser, typically in a separate browser tab/window. For example, before I wrote this package, I used to regularly open Chrome's developer tools, find the failed resource in the Resources tab, and then either read through the raw HTML (yuck) or copy and paste it to a file and double click it (tedious).

As [you](http://groups.google.com/group/django-users/browse_thread/thread/820101441f4dc070) [can](http://djangosnippets.org/snippets/650/) [see](http://djangosnippets.org/snippets/802/) this bothered other people, too.

Suggested Solution
------------------
Since the problem is really about ease of development, and since I (and I suspect many other Django developers) do most of my development work locally, I figured the solution can take advantage of the server being a full fledged desktop with a modern browser and a GUI. Enter `ajaxerrors.middleware.ShowAJAXErrors`. This little middleware intercepts all unhandled view exceptions, pickles the technical error page and uses Python's webbrowser module to direct a new browser tab at a special URL that will serve (and remove) the previously stored page.

All this is only triggered if `DEBUG` is true and `request.is_ajax()` (documented [here](http://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.is_ajax)) is true, so pretty much everything you're used to in your development flow should stay the same. Sweet.

Installation Instructions
-------------------------
1. Install like any other Python package with `easy_install` or `pip`, or simply with:
    python setup.py install

2. Add `ajaxerrors.middleware.ShowAJAXErrors` to your settings, typically like so:

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'ajaxerrors.middleware.ShowAJAXErrors'
    )

Additional Settings
-------------------
This package is really simple, I expect many Django developers to be able to read the code just about as quickly as they can digest this 'documentation'. It doesn't have many configuration options, but it does recognize the following:

1. `AJAXERRORS_DO_NOTHING_UNLESS_IN_DEBUG` (boolean): Pretty much what you'd expect. I added it to the codebase as a fail-safe against accidentally leaving the middleware installed in a real deployment. You may want to use it (with caution and assuming you know what you're doing) when debugging the nastier bugs that occur only when DEBUG=False.

2. `AJAXERRORS_WEBBROWSER_OPEN_KWARGS` (mapping): These keyword arguments will be passed verbatim to stdlib's [webbrowser](http://docs.python.org/library/webbrowser.html) package's `open` method. These parameters don't do much on my OSX system, but I assume they actually work on other systems and you may care.

3. `AJAXERRORS_ADDITIONAL_HANDLERS` (iterable): This setting is expected to contain either handler objects or strings that represent the Python import paths of handlers (or any mixture of both). See below to read more about handlers.

4. `AJAXERRORS_PATH` (string): The URL path from which the error pages will be served. It's unlikely that you'll need to change it.

Handlers
--------
This is probably the most complicated feature of this pacakge (and it's not really complicated...). Handlers are callable objects that will be invoked in order after the normal behaviour (of storing and directing the browser to a copy of the technical error page). These callables must receive four arguments: the request object, the exception's type, the exception's value and the traceback (a-la `sys.exc_info()`). A handler can do whatever it wants with this information; handlers are assumed to return None or an HttpResponse instance. The last non-None value returned by a handler (if any) will be sent back to the browser.

An example is worth a thousand words - in ajaxerrors.handlers you can find two handlers I sometimes use:
* `return_empty_dict`: causes unhandled exceptions in AJAX requests to return an HTTP OK response with an empty JSON object.
* `growlnotify`: opens a [Growl](http://growl.info/) notification briefly describing the exception.

Contributing
------------
django-ajaxerrors is licensed under the MIT license, see the `LICENSE` file in this distribution if you're really interested in reading all them small letters.

I'd really like to see this as a feature in Django some day, but first we should see if other people are interested and maybe add more stuff to this really simple utility. Anyway, feel free fork away and send me pull requests. I'll do my sane best to fix any bugs for as long as... well, at least until I lose interest.

If you'd like to discuss something about django-ajaxerrors or if you are otherwise curious about me, please find me at yaniv at aknin dot name, or visit my smashing [Python-centric tech blog](http://tech.blog.aknin.name).
