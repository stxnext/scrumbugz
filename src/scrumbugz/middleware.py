import re
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required

class EnforceHostnameMiddleware(object):
    """
    Enforce the hostname per the ENFORCE_HOSTNAME setting in the project's settings

    The ENFORCE_HOSTNAME can either be a single host or a list of acceptable hosts
    """
    def process_request(self, request):
        """Enforce the host name"""
        allowed_hosts = getattr(settings, 'ENFORCE_HOSTNAME', None)
        secure_only = getattr(settings, 'ENFORCE_SSL', False)

        if settings.DEBUG or not allowed_hosts:
            return None

        host = request.get_host()

        # find the allowed host name(s)
        if isinstance(allowed_hosts, basestring):
            allowed_hosts = [allowed_hosts]

        if host in allowed_hosts and (not secure_only or (secure_only and request.is_secure())):
            return None

        # redirect to the proper host name\
        new_url = "%s://%s%s" % (
            'https' if secure_only or request.is_secure() else 'http',
            allowed_hosts[0], request.get_full_path())

        return HttpResponsePermanentRedirect(new_url)


class RequireLoginMiddleware(object):
    """
    Middleware component that wraps the login_required decorator around
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and
    define LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS in your
    settings.py. For example:
    ------
    LOGIN_REQUIRED_URLS = (
        r'/topsecret/(.*)$',
    )
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$',
        r'/topsecret/logout(.*)$',
    )
    ------
    LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must
    be a valid regex.

    LOGIN_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly
    define any exceptions (like login and logout URLs).
    """
    def __init__(self):
        self.required = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS])
        self.exceptions = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS])

    def process_view(self,request,view_func,view_args,view_kwargs):
        # No need to process URLs if user already logged in
        if request.user.is_authenticated(): return None
        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path): return None
        # Requests matching a restricted URL pattern are returned
        # wrapped with the login_required decorator
        for url in self.required:
            if url.match(request.path): return login_required(view_func)(request,*view_args,**view_kwargs)
        # Explicitly return None for all non-matching requests
        return None