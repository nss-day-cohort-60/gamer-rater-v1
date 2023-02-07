"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamerraterapi.models import Game, GameCategory, Category


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)


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
        new_game.estimated_time = request.data['time']
        new_game.recommended_age = request.data['age_rating']
        new_game.min_players = request.data['minimum_players']
        new_game.max_players = request.data['maximum_players']
        new_game.title = request.data['title']
        new_game.year_released = request.data['release_date']
        new_game.save()

        categories_selected = request.data['categories']

        for category in categories_selected:
            monkey = GameCategory()
            monkey.game = new_game #   <--- this is an object instance of a game
            monkey.category = Category.objects.get(pk = category)#   <--- this is an object instance of a category
            monkey.save()

        serializer = GameSerializer(new_game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ( 'label', )


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""
    categories = GameCategorySerializer(many=True)

    class Meta:
        model = Game
        fields = (
            'id', 'title', 'description', 'designer', 'year_released',
            'min_players', 'max_players', 'estimated_time', 'recommended_age',
            'categories'
        )
        # depth = 1  # NUCLEAR BOMB OPTION 🧨 💣 🧨