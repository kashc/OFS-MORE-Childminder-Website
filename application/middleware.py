from django.conf import settings  # import the settings file
from django.http import HttpResponseRedirect
from re import compile


class CustomAuthenticationMiddleware(object):
    """
    Custom authentication handler to globally protect site with the exception of paths
    tested against regex patterns defined in settings.py
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Default the login url as being authentication exempt
        authentication_exempt_urls = [compile(settings.LOGIN_URL.lstrip('/'))]

        # If further login exempt URLs have been defined in the settings.py file, append these to
        # the collection
        if hasattr(settings, 'AUTHENTICATION_EXEMPT_URLS'):
            authentication_exempt_urls += [compile(expr) for expr in settings.AUTHENTICATION_EXEMPT_URLS]

        # If user is not authenticated and the path they are attempting to navigate to requires a session
        # return the user to the login page
        if not request.user.is_authenticated() and request.path_info != settings.AUTHENTICATION_URL \
                and not any(m.match(request.path_info) for m in authentication_exempt_urls):
            return HttpResponseRedirect(settings.AUTHENTICATION_URL)

        # If request has not been blocked at this point in the execution flow, allow
        # request to continue processing as normal
        return self.get_response(request)


def globalise_url_prefix(request):
    """
    Middleware function to support Django applications being hosted on a
    URL prefixed path (e.g. for use with reverse proxies such as NGINX) rather
    than assuming application available on root index.
    """
    # return URL_PREFIX value defined in django settings.py for use by global view template
    return {'URL_PREFIX': settings.URL_PREFIX}
