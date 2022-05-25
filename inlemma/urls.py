from django.urls import include, path, re_path
from ckeditor_uploader.views import upload
from django.conf import settings
from django.views.static import serve
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', include('home.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('', include('accounts.urls')),
    path('profile/', include('profiles.urls')),
    re_path(r'^ckeditor/upload/', login_required(upload), name='ckeditor_upload'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

# serving media files only on debug mode
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^img/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]