from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from digital_library import settings
from digital_library.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("filter/<slug:category_slug>/", home, name="filter_category"),
    path("user/", include("user_profile.urls")),
    path("book/", include("books.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
