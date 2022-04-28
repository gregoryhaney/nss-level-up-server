"""View module for handling requests about game types"""
from email import message
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        # this 'retrieve' method will get a single object from the DB based on
        # the PK in the URL. 
            # ORM is used to get the data
            # Serializer converts the Python data to JSON format
            
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        # 'try' block added to provide user better feedback when a non-existing game type
        # was entered. EXAMPLE URL: [ http://localhost:8000/gametypes/478 ]
        # Doesn't exist, so returns: [ "message": "GameType matching query does not exist" ]
                
        try:
            game_type = GameType.objects.get(pk=pk)     # "get" method in ORM
            serializer = GameTypeSerializer(game_type)  # once retrieved, it's passed to serializer
            return Response(serializer.data)            # serializer.data is passed to response as
        except GameType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
                                                        # the response body. Using "Response" combines
                                                        # what used to be done with "_set_headers"
                                                        # and "wfile.write" FNs
        
            # above, the "get" method in ORM is retrieving a single GameType
            # it is equivalent to the following SQL "execute":
                #  db_cursor.execute("""
                #       SELECT id, label
                #       FROM levelupapi_gametype
                #       WHERE id = ?""",(pk,)
                #  )
        

    def list(self, request):
            # retrieves the entire collection from the DB
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game_types = GameType.objects.all()                         # ORM method "all"
        serializer = GameTypeSerializer(game_types, many=True)
        return Response(serializer.data)
                            # above, the game_types variable is now a list of GameType
                            # objects. The game_types are passed to the serializer class.
                            # "many=True" tells serializer that a LIST versus a SINGLE OBJ
                            # is to be serialized.
    
                # above, the ORM method "all" is equivalent to the following SQL code:
                    # SELECT *
                    # FROM levelupapi_gametype
                    
class GameTypeSerializer(serializers.ModelSerializer):
        # the Serializer class determines how the Python data should be serialized
        # to be sent back to the client.
    """JSON serializer for game types
    """
    class Meta:
        model = GameType
        fields = ('id', 'label')
        
                # above, the Meta class holds the configuration for the serializer.
                # it tells serializer to use "GameType" model and to include
                # the "id" and "label" fields
                