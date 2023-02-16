"""View module for handling requests about park areas"""
import re
from django.core.exceptions import ValidationError
from django.db.models.fields import BooleanField
from django.http import HttpResponseServerError
from django.db.models import Count, Q, When, Case
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from gamerraterapi.models import Game, Player, Category


class CategoryView(ViewSet):
    """GamerRater category"""

    def list(self, request):
        """Handle GET requests to category resource

        Returns:
            Response -- JSON serialized list of category
        """
        categories = Category.objects.all()
        serialized_categories = CategorySerializer(categories, many=True)
        return Response(serialized_categories.data, status=status.HTTP_200_OK)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for category"""

    class Meta:
        model = Category
        fields = ('id', 'label', )
