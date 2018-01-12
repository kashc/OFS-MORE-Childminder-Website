from django.conf import settings  # import the settings file


def url_prefix(request):
    # return the value you want as a dictionary. you may add multiple values in there.
    return {'URL_PREFIX': settings.URL_PREFIX}
