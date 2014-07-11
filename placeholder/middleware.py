from .utils import expire_page


class ExpireCacheMiddleware(object):

    def process_request(self, request):
        if '__placeholder_expire_page' in request.GET:
            expire_page(request.path)

    def process_response(self, request, response):
        if '__placeholder_expire_page' in request.GET:
            expire_page(request.path)
        return response
