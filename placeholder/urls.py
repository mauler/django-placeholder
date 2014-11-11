from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'placeholder.views',
    url(r'^upload/$', "placeholder_upload", name="placeholder_upload"),
    url(r'^save/$', "placeholder_save", name="placeholder_save"),
)
