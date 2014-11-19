from json import loads

from .__init__ import world
from .utils import expire_page


def get_current_request():
    return getattr(world, "request", None)


def get_current_user():
    request = get_current_request()
    if request:
        return getattr(request, "user", None)


class WorldMiddleware(object):
    def process_request(self, request):
        world.request = request


class MultiEditMiddleware(object):

    def process_request(self, request):
        if '__placeholder_multiedit' in request.GET:
            world.__placeholder_multiedit = \
                loads(request.GET['__placeholder_multiedit'])


class ExpireCacheMiddleware(object):

    def process_request(self, request):
        if '__placeholder_expire_page' in request.GET:
            expire_page(request.path)

    def process_response(self, request, response):
        if '__placeholder_expire_page' in request.GET:
            expire_page(request.path)
        return response
