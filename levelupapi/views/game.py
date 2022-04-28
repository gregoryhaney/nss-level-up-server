"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game
from levelupapi.views import GameTypeView


class GameView(ViewSet):
    """Level up game view"""

    def retrieve(self, request, pk):
        # this 'retrieve' method will get a single object from the DB based on
        # the PK in the URL. 
            # ORM is used to get the data
            # Serializer converts the Python data to JSON format
            
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game
        """
        
        # 'try' block added to provide user better feedback when a non-existing game 
        # was entered. EXAMPLE URL: [ http://localhost:8000/games/478 ]
        # Doesn't exist, so returns: [ "message": "Game matching query does not exist" ]
        try:       
            game = Game.objects.get(pk=pk)              # "get" method in ORM
            serializer = GameSerializer(game)           # once retrieved, it's passed to serializer
            return Response(serializer.data)            # serializer.data is passed to response as
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
                                                    # the response body. Using "Response" combines
                                                    # what used to be done with "_set_headers"
                                                    # and "wfile.write" FNs
        
            # above, the "get" method in ORM is retrieving a single Game
            # it is equivalent to the following SQL "execute":
                #  db_cursor.execute("""
                #       SELECT id, title, maker, number__players, skill_level, game_type_id, gamer_id
                #       FROM levelupapi_game
                #       WHERE id = ?""",(pk,)
                #  )
        

    def list(self, request):
            # retrieves the entire collection from the DB
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()                         # ORM method "all"
        
            # the following three lines allow for passing in a query string parameter via URL.
            # before sending the 'games' list to the serializer, we can check if a query
            # string was passed.
            # EXAMPLE URL: [ http://localhost:8000/games?type=1 ]
            # URL parsing not required because ViewSet class already has done it
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
     
            # above, the 'request' from the method parameters holds all info for the 
            # request from client. The 'request.query_params' is a dictionary of any query
            # parameters that were in the URL. If "type" is not found on the dictionary,
            # "None" is returned.
            # After getting value of "game_type", the ORM filter method is used to include
            # only games with that game type. It is the equivalent of:
                #   db_cursor.execute(""""
                #       SELECT *
                #       FROM levelupapi_game
                #       WHERE game_type_id = ?
                #   """", (game_type,)
                #   )
         
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
                            # above, the game variable is now a list of Game
                            # objects. The games are passed to the serializer class.
                            # "many=True" tells serializer that a LIST versus a SINGLE OBJ
                            # is to be serialized.
    
                # above, the ORM method "all" is equivalent to the following SQL code:
                    # SELECT *
                    # FROM levelupapi_game
                    
class GameSerializer(serializers.ModelSerializer):
        # the Serializer class determines how the Python data should be serialized
        # to be sent back to the client.
    """JSON serializer for game
    """
    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players',
                  'skill_level', 'game_type', 'gamer')
        depth = 2
        
                # above, the Meta class holds the configuration for the serializer.
                # it tells serializer to use "Game" model and to include
                # the listed fields
                
        # UPDATED: in the Meta class, I added the [ depth = 2 ]. This allows for display of
        # expanded data from associated tables. For example, using the "game_type_id" as
        # an FK to get info from 'gametype' DB table; or the "gamer_id" as an FK to get
        # all the info from the 'gamer' table in the DB.
            # IMPORTANT: if doing this, omit the "_id" for the particular field, otherwise it
            # will only return the id and not the desired expansion data.
            # i.e.: WITHOUT [depth], use "game_type_id". WITH [depth], use "game_type"
                