import os
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

from account import urls as account
from sales import urls as sales
from surgalt import urls as surgalt

# from tmz import urls as train_urls
from django.conf.urls.i18n import i18n_patterns

schema_view = get_schema_view(
    openapi.Info(
        title="Zumo API",
        default_version='v1',
        description="Zumo description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="do.damdinsuren@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', RedirectView.as_view(url='/bff/')),
    path('redoc', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),

    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui')] if os.environ.get(
    'DEBUG') == 'TRUE' else []

urlpatterns += [
    path('bff/', admin.site.urls),
    # path('ckeditor', include('ckeditor_uploader.urls')),
    # Rest API

    path('api/account/', include(account)),
    path('api/sales/', include(sales)),
    path('api/surgalt/', include(surgalt)),
]
# translate hiigdeh url end nemeh
# urlpatterns += i18n_patterns(
# )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Zumo admin"
admin.site.site_title = "Zumo admin site"
admin.site.index_title = "Zumo Admin"
