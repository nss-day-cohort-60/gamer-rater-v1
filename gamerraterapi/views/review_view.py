"""View module for handling requests about game reviews"""
import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamerraterapi.models import GameReview, Game, Player


class GameReviewView(ViewSet):
    """Gamer rater game reviews view"""

    def list(self, request):
        """Handle GET requests to get all game reviews

        Returns:
            Response -- JSON serialized list of game reviews
        """
        games = Game.objects.all()
        serializer = GameReviewSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new game

        Returns:
            Response -- JSON serialized dictionary representation of the new game
        """
        try:
            game = Game.objects.get(pk=request.data['game'])
        except Game.DoesNotExist:
            return Response({'message': 'You sent an invalid game ID'}, status=status.HTTP_404_NOT_FOUND)

        try:
            authenticated_player = Player.objects.get(user=request.auth.user)
        except Player.DoesNotExist:
            return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)

        review_text = request.data.get('review', None)
        if review_text is None:
            return Response({'message': 'Please submit the review text. It cannot be blank.'}, status=status.HTTP_400_BAD_REQUEST)

        game_review = GameReview()
        game_review.review = review_text
        game_review.game = game
        game_review.player = authenticated_player
        game_review.date_reviewed = datetime.datetime.now()
        game_review.save()

        serializer = GameReviewSerializer(game_review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ReviewPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ( 'full_name', )


class GameReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for game reviews"""
    player = ReviewPlayerSerializer()

    class Meta:
        model = GameReview
        fields = ( 'id', 'player', 'game', 'date_reviewed', 'review',)