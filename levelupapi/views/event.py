"""View module for handling requests about game types"""
from asyncio import events
from urllib import request
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer
from rest_framework.decorators import action

class EventView(ViewSet):
    """Level Up events view"""

        # @action is a 'decorator', which allows us to create a custom
        # action that the API will support. In this case, we want the client
        # to make a request to allow a gamer to sign up for an event.
        # @action requires above: "from rest_framework.decorators import action"
        # in @action, specify the supported HTTP method(s), e.g.: post, delete, etc.
        # "detail=True" means the URL will include the PK.
        # the route is named after the FN, so to call this method, the
        # URL would look like: [ http://localhost:8000/events/2/signup ]

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
            """POST request for a User to sign up for an Event"""

            gamer = Gamer.objects.get(user=request.auth.user)
            event = Event.objects.get(pk=pk)
            event.attendees.add(gamer)
            return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

                # ABOVE: just like with the "create" method below, we get the
                # Gamer that is logged in and the Event by its PK. The
                # 'ManyToManyField' - attendees - on the 'Event' model handles
                # the heavy lifting.
                # The 'add' method on 'attendees' creates the relationship btwn 
                # this Event and Gamer by adding "event_id" && "gamer_id" to
                # the join table. It returns an HTTP 201 response to the client.

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
            """DELETE request for a User to leave an Event"""
            gamer = Gamer.objects.get(user=request.auth.user)
            event = Event.objects.get(pk=pk)
            event.attendees.remove(gamer)
            return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)
    
    
    @property
    def joined(self):
            return self.__joined
        
    @joined.setter
    def joined(self, value):
            self.__joined = value
    
    
    
    
    
    
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
        
        gamer = Gamer.objects.get(user=request.auth.user)
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
                
                # set the 'joined' property on every event 
        for event in events:
                # check if gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()
                    # ABOVE: the 'all' method gets every gamer attending the event.
                    # 'gamer in event...' evals to True or False depending on
                    # whether gamer is in attendees list
            
         
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
                            # above, the event variable is now a list of Event
                            # objects. The events are passed to the serializer class.
                            # "many=True" tells serializer that a LIST versus a SINGLE OBJ
                            # is to be serialized.
    
                # above, the ORM method "all" is equivalent to the following SQL code:
                    # SELECT *
                    # FROM levelupapi_event


    def create(self, request):
        """Handle the POST operations
        
            Returns
                Response -- JSON serialized event instance        
        """
            # the first line below gets the user (gamer) that is logged in.
            # use the 'request.auth.user' to get the 'organizer' object based on user
                # the equivalent in SQL:
                    #   db_cursor.execute("""
                    #       SELECT *
                    #       FROM levelupapi_gamer
                    #       WHERE user = ?
                    #       """, (user,)
                    #   )
        gamer = Gamer.objects.get(user=request.auth.user)
        
            # Retrieve the 'Game' object from DB to make sure the game
            # the user is trying to add for a new event (create) actually exists in the DB.
            # Data passed in from client is held in 'request.data' dictionary.
                # keys used on the 'request.data' must match what client is passing to server
        
        game = Game.objects.get(pk=request.data["game_id"])
        
            # create() ORM method is called to add the event to DB. 
            # fields are passed to FN as parameters
                # SQL equivalent is:
                    #   db_cursor.execute("""
                    #   INSERT INTO levelupapi_event
                    #   (description, date, time, game_id, organizer_id)
                    #   VALUES (?, ?, ?, ?, ?)
                    #   """, (request.data["description"], request.data["date"],
                    #   request.data["time"], game, gamer)) ) 
        
        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            game=game,
            organizer=gamer
        )
                # Once 'create' has finished, the 'event' variable is now the new
                # 'event' instance, including the new 'id'. The object can be 
                # serialized and returned to the client, just like in 'retrieve' above.        
        
        serializer = EventSerializer(event)
        return Response(serializer.data)  
    
    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)   
    
    
    
    
    # Similar to above with "retrieve" and "update" methods, this method
    # "destroy" takes the PK as an argument. The PK is used to get the
    # single object, then calls the "DELETE" from the ORM to remove it from DB.
    # The response back to client is HTTP 204.       
           
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
                    
class EventSerializer(serializers.ModelSerializer):
        # the Serializer class determines how the Python data should be serialized
        # to be sent back to the client.
    """JSON serializer for event
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'organizer',
                  'description', 'date', 'time', 'attendees', 'joined')                  
        
                # above, the Meta class holds the configuration for the serializer.
                # it tells serializer to use "Event" model and to include
                # the listed fields
    
class CreateEventSerializer(serializers.ModelSerializer):
     # the Serializer class determines how the Python data should be serialized
        # to be sent back to the client.
    # This is a new Serializer class that is being used to do input validation
    # It includes ONLY the fields expected from the client.
        # So, no "organizer" field, since that comes from the Auth header and NOT the body
    """JSON serializer for game to validate/save the new game in the Create method
    """
    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'time', 'game_id')               
   
    
    
  # ===========================================================
  # ======= ORIGINAL UPDATE METHOD (before adding validation) 
  
#   def update(self, request, pk):
#         """Handle the PUT requests for an event
        
#             RETURNs: 
#                 Response -- Empty body with 204 status code
#         """
#             # just like in the RETRIEVE method above, we get the Event
#             # object we want from the DB (1st line below). The next
#             # several lines set up the fields on Event to the incoming values
#             # from the client (just like the CREATE method above).
#             # Once all fields are set, changes are SAVEd to the DB.
#                 # this UPDATE method will be called when a PUT request is
#                 # made to [ http://localhost:8000/events/<event_id>]
        
#         event = Event.objects.get(pk=pk)
#         event.description = request.data["description"]
#         event.date = request.data["date"]
#         event.time = request.data["time"]
#         event.game_id = request.data["game_id"]
    
#         gamer = Gamer.objects.get(user=request.auth.user)
#         event.organizer_id = gamer
       
#         event.save()

#         return Response(None, status=status.HTTP_204_NO_CONTENT)         
               