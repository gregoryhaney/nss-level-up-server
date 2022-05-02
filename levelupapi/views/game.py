"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType
from levelupapi.views import GameTypeView, game_type



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
     
    def create(self, request):
        """Handle the POST operations
        
            Returns
                Response -- JSON serialized game instance        
        """
            # the first line below gets the user (gamer) that is logged in.
            # use the 'request.auth.user' to get the 'gamer' object based on user
                # the equivalent in SQL:
                    #   db_cursor.execute("""
                    #       SELECT *
                    #       FROM levelupapi_gamer
                    #       WHERE user = ?
                    #       """, (user,)
                    #   )
        gamer = Gamer.objects.get(user=request.auth.user)
        
            # retrieve the 'GameType' object from DB to make sure the game type
            # the user is trying to add for new game (create) actually exists in the DB.
            # data passed in from client is held in 'request.data' dictionary.
                # keys used on the 'request.data' must match what client is passing to server
        
        game_type = GameType.objects.get(pk=request.data["game_type_id"])
        
            # create() ORM method is called to add the game to DB. 
            # fields are passed to FN as parameters
                # SQL equivalent is:
                    #   db_cursor.execute("""
                    #   INSERT INTO levelupapi_game
                    #   (title, maker, number_of_players, skill_level,
                    #   gamer_id, game_type_id) VALUES (?, ?, ?, ?, ?, ?)
                    #   """, (request.data["title"], request.data["maker"],
                    #   request.data["numberOfPlayers"], request.data["skillLevel"], 
                    #   gamer, game_type)) )
        
        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"],
            gamer=gamer,
            game_type=game_type
        )
                # Once 'create' has finished, the 'game' variable is now the new
                # 'game' instance, including the new 'id'. The object can be 
                # serialized and returned to the client, just like in 'retrieve' above.        
        
        serializer = GameSerializer(game)
        return Response(serializer.data)
         
     
     
                    
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




# ================================================================================
# This option was NOT implemented, but the code is here for reference
# It consists of a new CREATE method and a new SERIALIZER.
    # The new serializer is used to validate and save the game in the CREATE
    # method
    # Instead of making a new instance of the 'Game' model, the 'request.data'
    # dictionary is passed to the new serializer as the data. The keys on the
    # dictionary must match what is in the fields of the serializer. After creating
    # the serializer instance, call 'is_valid' to ensure client sent valid data. If the
    # code passes validation, the 'Save' method will add the game to the DB and add
    # an 'id' to the serializer.

# ================= PART I: NEW CREATE METHOD ==============================

# add this line at the top with the other imports
# from django.core.exceptions import ValidationError

# # this will replace the previous create method
# def create(self, request):
#     """Handle POST operations

#     Returns:
#         Response -- JSON serialized game instance
#     """
#     gamer = Gamer.objects.get(user=request.auth.user)
#     serializer = CreateGameSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save(gamer=gamer)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)

# ========== PART II: NEW SERIALIZER  ======================================        
# class CreateGameSerializer(serializers.ModelSerializer):
#      # the Serializer class determines how the Python data should be serialized
#         # to be sent back to the client.
#     # This is a new Serializer class that is being used to do input validation
#     # It includes ONLY the fields expected from the client.
#         # So, no "gamer" field, since that comes from the Auth header and NOT the body
#     """JSON serializer for game to validate/save the new game in the Create method
#     """
#     class Meta:
#         model = Game
#         fields = ('id', 'title', 'maker', 'number_of_players',
#                   'skill_level', 'game_type')
        
        
# ==================================================================
                