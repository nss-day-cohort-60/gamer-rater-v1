"""View module for handling requests about park areas"""
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from gamerraterapi.models import Game, Player, GameReview


class ReviewView(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        game_id = request.data.get('game', None)

        game_that_was_reviewed = None

        if game_id is not None:
            try:
                game_that_was_reviewed = Game.objects.get(pk=game_id)
            except Game.DoesNotExist:
                return Response({'message': 'You sent an invalid game id'}, status=status.HTTP_404_NOT_FOUND)


        review = GameReview()
        review.player = Player.objects.get(user=request.auth.user)
        review.review = request.data['review']
        review.game = game_that_was_reviewed
        review.save()

        serialized_game = ReviewSerializer(review)
        return Response(serialized_game.data, status=status.HTTP_201_CREATED)

class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""

    class Meta:
        model = GameReview
        fields = ('id', 'game', 'player', 'review', 'date_reviewed',)
