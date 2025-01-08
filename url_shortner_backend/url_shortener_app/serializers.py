from rest_framework import serializers
from .models import URL

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ['original_url']

    def create(self, validated_data):
        url = URL.objects.create(**validated_data)
        return url
