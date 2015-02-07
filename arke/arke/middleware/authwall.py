from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

_pattern = compile("^login/?")


class Authwall(object):
    def process_request(self, req):
        assert hasattr(req, 'user'), "Authwall Middleware requires Django auth to be enabled."
        if not req.user.is_authenticated() and not _pattern.match(req.path_info.lstrip('/')):
            return HttpResponseRedirect("/login")
