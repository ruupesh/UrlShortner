from django.contrib import admin
from django.urls import path, include
from url_shortner_app.views import RedirectView, URLShortnerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('url_shortner_app.urls')),  # Include the app-level URLs
    path('su/<str:short_url>/', RedirectView.as_view(), name='redirect'),
    # path('shorten/', URLShortnerView.as_view(), name='shorten_url'),
]
