"""View module for handling requests about category types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamerraterapi.models import Category


class CategoryView(ViewSet):
    """Level up category types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single category type

        Returns:
            Response -- JSON serialized category type
        """
        pass


    def list(self, request):
        """Handle GET requests to get all category types

        Returns:
            Response -- JSON serialized list of category types
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new category

        Returns:
            Response -- JSON serialized dictionary representation of the new category
        """
        pass


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for category types"""

    class Meta:
        model = Category
        fields = ( 'id', 'label', )