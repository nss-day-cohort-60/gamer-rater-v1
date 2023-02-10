"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamerraterapi.models import (
    Game, GameCategory, Category, GameReview,
    Player
)


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for single game

        Returns:
            Response -- JSON serialized game
        """
        game_to_update = Game.objects.get(pk=pk)
        game_to_update.description = request.data['description']
        game_to_update.designer = request.data['designer']
        game_to_update.estimated_time = request.data['estimated_time']
        game_to_update.recommended_age = request.data['recommended_age']
        game_to_update.min_players = request.data['min_players']
        game_to_update.max_players = request.data['max_players']
        game_to_update.title = request.data['title']
        game_to_update.year_released = request.data['year_released']
        game_to_update.save()

        categories_selected = request.data['categories']

        # Remove all category relationships for this game
        current_relationships = GameCategory.objects.filter(game__id=pk)
        current_relationships.delete()

        # Define relationships to categories sent by client
        for category in categories_selected:
            monkey = GameCategory()
            monkey.game = game_to_update #   <--- this is an object instance of a game
            monkey.category = Category.objects.get(pk = category)#   <--- this is an object instance of a category
            monkey.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)



    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new game

        Returns:
            Response -- JSON serialized dictionary representation of the new game
        """
        new_game = Game()
        new_game.description = request.data['description']
        new_game.designer = request.data['designer']
        new_game.estimated_time = request.data['estimated_time']
        new_game.recommended_age = request.data['recommended_age']
        new_game.min_players = request.data['min_players']
        new_game.max_players = request.data['max_players']
        new_game.title = request.data['title']
        new_game.year_released = request.data['year_released']
        new_game.save()

        categories_selected = request.data['categories']

        for category in categories_selected:
            monkey = GameCategory()
            monkey.game = new_game #   <--- this is an object instance of a game
            monkey.category = Category.objects.get(pk = category)#   <--- this is an object instance of a category
            monkey.save()

        serializer = GameSerializer(new_game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class GameReviewPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ( 'full_name', )

class GameReviewSerializer(serializers.ModelSerializer):
    player = GameReviewPlayerSerializer()

    class Meta:
        model = GameReview
        fields = ( 'id', 'date_reviewed', 'review', 'player')

class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ( 'label', 'id', )


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""
    categories = GameCategorySerializer(many=True)
    game_reviews = GameReviewSerializer(many=True)

    class Meta:
        model = Game
        fields = (
            'id', 'title', 'description', 'designer', 'year_released',
            'min_players', 'max_players', 'estimated_time', 'recommended_age',
            'categories', 'game_reviews'
        )
