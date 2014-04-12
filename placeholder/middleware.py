from .utils import expire_page


class ExpireCacheMiddleware(object):
    def process_request(self, request):
        if '__placeholder_expire_page' in request.GET:
            expire_page(request.path)
