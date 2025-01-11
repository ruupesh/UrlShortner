from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.urls import reverse
from .models import URL
from .serializers import URLSerializer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)



class URLShortnerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        original_url = request.data.get("original_url")
        if not original_url:
            return Response({"error": "Original URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the URL is already cached
        cached_short_url = cache.get(original_url)
        if cached_short_url:
            return Response({"short_url": cached_short_url}, status=status.HTTP_200_OK)

        # Check if the URL already exists in the database
        existing_url = URL.objects.filter(original_url=original_url, user=request.user).first()
        if existing_url:
            short_url = request.build_absolute_uri(reverse("redirect", args=[existing_url.short_url]))
            return Response({"short_url": short_url}, status=status.HTTP_200_OK)

        # Generate a unique short code
        short_code = self.generate_short_code()

        # Create a new short URL
        serializer = URLSerializer(data={"original_url": original_url, "short_url": short_code})
        if serializer.is_valid():
            url_instance = serializer.save(user=request.user)
            short_url = request.build_absolute_uri(reverse("redirect", args=[url_instance.short_url]))

            # Cache the short URL for the original URL
            cache.set(original_url, short_url, timeout=60 * 60 * 24)  # Cache for 24 hours
            cache.set(url_instance.short_url, original_url, timeout=60 * 60 * 24)  # Cache reverse mapping

            return Response({"short_url": short_url}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Retrieve all URLs for the authenticated user
        urls = URL.objects.filter(user=request.user)
        serializer = URLSerializer(urls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def generate_short_code(self):
        """
        Generates a unique short code for the URL.
        """
        while True:
            short_code = f"su/{get_random_string(6)}"  # Generate a random 6-character string
            if not URL.objects.filter(short_url=short_code).exists():
                return short_code


class RedirectView(APIView):
    def get(self, request, short_url):
        # Check if the short URL is cached
        cached_original_url = cache.get(short_url)
        if cached_original_url:
            # If cached, increment the click count in the database
            try:
                url_instance = URL.objects.get(short_url=short_url)
                url_instance.click_count += 1
                url_instance.save()  # Ensure changes are saved
            except URL.DoesNotExist:
                pass
            return HttpResponseRedirect(url_instance.original_url)
            # return Response({"original_url": cached_original_url}, status=status.HTTP_302_FOUND)

        # Fetch from the database if not cached
        try:
            url_instance = URL.objects.get(short_url=short_url)
            url_instance.click_count += 1  # Increment click count
            url_instance.save()  # Save the updated click count

            # Cache the original URL
            cache.set(short_url, url_instance.original_url, timeout=60 * 60 * 24)  # Cache for 24 hours
            return HttpResponseRedirect(url_instance.original_url)
            # return Response({"original_url": url_instance.original_url}, status=status.HTTP_302_FOUND)
        except URL.DoesNotExist:
            return Response({"error": "URL not found"}, status=status.HTTP_404_NOT_FOUND)


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.debug("AnalyticsView GET request received.")
        urls = URL.objects.filter(user=request.user)
        analytics_data = [
            {
                "original_url": url.original_url,
                "short_url": request.build_absolute_uri(reverse("redirect", args=[url.short_url])),
                "click_count": url.click_count,
                "created_at": url.created_at.isoformat(),
            }
            for url in urls
        ]
        return Response(analytics_data, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        Delete a specific URL owned by the authenticated user.
        """

        short_url = request.data.get("short_url")
        current_domain = request.build_absolute_uri("/")
        short_url = short_url.replace(current_domain, "")[:-1]

        if not short_url:
            return Response({"error": "Short URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve and delete the URL
            url_instance = URL.objects.get(short_url=short_url, user=request.user)
            cache.delete(short_url)  # Remove from cache if exists
            url_instance.delete()
            return Response({"message": "URL deleted successfully"}, status=status.HTTP_200_OK)
        except URL.DoesNotExist:
            return Response(
                {"error": "URL not found or not owned by the user"},
                status=status.HTTP_404_NOT_FOUND,
            )

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)