from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import URLShortnerView, RedirectView, AnalyticsView, RegisterView

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT Token endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token endpoint
    path('shorten/', URLShortnerView.as_view(), name='shorten_url'),
    # path('<str:short_url>/', RedirectView.as_view(), name='redirect'),
]
