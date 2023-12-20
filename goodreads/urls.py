from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from goodreads.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('books/', include('books.urls')),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),

    path('api-auth/', include('rest_framework.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)