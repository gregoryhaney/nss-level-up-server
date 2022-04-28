"""View module for handling requests about game types"""
from asyncio import events
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event


class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        # this 'retrieve' method will get a single object from the DB based on
        # the PK in the URL. 
            # ORM is used to get the data
            # Serializer converts the Python data to JSON format
            
        """Handle GET requests for single event type

        Returns:
            Response -- JSON serialized event
        """
        # 'try' block added to provide user better feedback when a non-existing event
        # was entered. EXAMPLE URL: [ http://localhost:8000/events/478 ]
        # Doesn't exist, so returns: [ "message": "Event matching query does not exist" ]
        try:       
            event = Event.objects.get(pk=pk)              # "get" method in ORM
            serializer = EventSerializer(event)           # once retrieved, it's passed to serializer
            return Response(serializer.data)            # serializer.data is passed to response as
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
                                                    # the response body. Using "Response" combines
                                                    # what used to be done with "_set_headers"
                                                    # and "wfile.write" FNs
        
            # above, the "get" method in ORM is retrieving a single Event
            # it is equivalent to the following SQL "execute":
                #  db_cursor.execute("""
                #       SELECT id, description, date, time, game_id, organizer_id
                #       FROM levelupapi_event
                #       WHERE id = ?""",(pk,)
                #  )
        

    def list(self, request):
            # retrieves the entire collection from the DB
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()                         # ORM method "all"
        
        
        # the following three lines allow for passing in a query string parameter via URL.
            # before sending the 'events' list to the serializer, we can check if a query
            # string was passed.
            # EXAMPLE URL: [ http://localhost:8000/events?game=1 ]
            # URL parsing not required because ViewSet class already has done it
        game_id = request.query_params.get('game', None)
        if game_id is not None:
            events = events.filter(game_id=game_id)
     
            # above, the 'request' from the method parameters holds all info for the 
            # request from client. The 'request.query_params' is a dictionary of any query
            # parameters that were in the URL. If "game" is not found on the dictionary,
            # "None" is returned.
            # After getting value of "game_id", the ORM filter method is used to include
            # only events with that game id. It is the equivalent of:
                #   db_cursor.execute(""""
                #       SELECT *
                #       FROM levelupapi_event
                #       WHERE event_id = ?
                #   """", (game_id,)
                #   )   
        
         
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
                            # above, the event variable is now a list of Event
                            # objects. The events are passed to the serializer class.
                            # "many=True" tells serializer that a LIST versus a SINGLE OBJ
                            # is to be serialized.
    
                # above, the ORM method "all" is equivalent to the following SQL code:
                    # SELECT *
                    # FROM levelupapi_event
                    
class EventSerializer(serializers.ModelSerializer):
        # the Serializer class determines how the Python data should be serialized
        # to be sent back to the client.
    """JSON serializer for event
    """
    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'time', 'game_id', 'organizer_id')                  
        
                # above, the Meta class holds the configuration for the serializer.
                # it tells serializer to use "Event" model and to include
                # the listed fields
                