from django.contrib import admin
from django.urls import path, include
from url_shortener_app.views import RedirectView, URLShortenerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('url_shortener_app.urls')),  # Include the app-level URLs
    path('<str:short_url>/', RedirectView.as_view(), name='redirect'),
    # path('shorten/', URLShortenerView.as_view(), name='shorten_url'),
]
