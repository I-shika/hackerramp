from rest_framework import serializers
from .models import Photos, Styling,Products

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ['photos']

class StylingSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)

    class Meta:
        model = Styling
        fields = ['username', 'photos','productId']  # Include any other fields needed

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields='__all__'
