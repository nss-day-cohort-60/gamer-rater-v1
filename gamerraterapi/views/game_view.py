"""View module for handling requests about park areas"""
import re
from django.core.exceptions import ValidationError
from django.db.models.fields import BooleanField
from django.http import HttpResponseServerError
from django.db.models import Count, Q, When, Case
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from gamerraterapi.models import Game, Player, GameReview, GameCategory, Category


class GamesView(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        new_game = Game()
        new_game.player = Player.objects.get(user=request.auth.user)
        new_game.title = request.data['title']
        new_game.description = request.data['description']
        new_game.designer = request.data['designer']
        new_game.year_released = request.data['year_released']
        new_game.min_players = request.data['min_players']
        new_game.max_players = request.data['max_players']
        new_game.recommended_age = request.data['recommended_age']
        new_game.estimated_time = request.data['estimated_time']
        new_game.save()

        category_ids = request.data['categories']

        for category_id in category_ids:
            game_category = GameCategory()
            game_category.game = new_game
            game_category.category = Category.objects.get(pk=category_id)
            game_category.save()


        serialized_game = GameSerializer(new_game)
        return Response(serialized_game.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        game = Game.objects.get(pk=pk)
        serialized_games = GameSerializer(game)
        return Response(serialized_games.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        edited_game = Game.objects.get(pk=pk)
        edited_game.player = Player.objects.get(user=request.auth.user)
        edited_game.title = request.data['title']
        edited_game.description = request.data['description']
        edited_game.designer = request.data['designer']
        edited_game.year_released = request.data['year_released']
        edited_game.min_players = request.data['min_players']
        edited_game.max_players = request.data['max_players']
        edited_game.recommended_age = request.data['recommended_age']
        edited_game.estimated_time = request.data['estimated_time']
        edited_game.save()

        # wipe them all out and rebuild
        GameCategory.objects.filter(game=edited_game).delete()
        # edited_game.categories.delete()

        # Create the ones the client sent
        category_ids = request.data['categories']

        for category_id in category_ids:
            game_category = GameCategory()
            game_category.game = edited_game
            game_category.category = Category.objects.get(pk=category_id)
            game_category.save()

        serialized_game = GameSerializer(edited_game)
        return Response(serialized_game.data, status=status.HTTP_201_CREATED)



    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 204, 404, or 500 status code
        """

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        serialized_games = GameSerializer(games, many=True)
        return Response(serialized_games.data, status=status.HTTP_200_OK)


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ( 'id', 'full_name')


class GameReviewSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(many=False)

    class Meta:
        model = GameReview
        fields = ( 'id', 'game', 'player', 'date_reviewed', 'review' )


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    game_reviews = GameReviewSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'player', 'title', 'description', 'game_reviews',
                  'designer', 'year_released', 'min_players', 'categories',
                  'max_players', 'recommended_age','estimated_time')
        depth = 1