from django.core.cache import cache
from django.http import HttpRequest
from django.utils.cache import get_cache_key


def expire_page(path):
    request = HttpRequest()
    request.path = path
    key = get_cache_key(request)
    if key in cache:
        cache.delete(key)
