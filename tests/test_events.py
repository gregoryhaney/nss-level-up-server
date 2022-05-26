#
# If you need any resources created 
# before a test is run, do it in setUp(). 
# Below, set up FN does three things:
#
#  1. Registers a Gamer in the testing database.
#  2. Captures the authentication Token from the response.
#  3. Seeds the testing database with a GameType.
#
#  All FNs dealing with integration testing must start with " test_  "
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Event, Gamer, Game
from levelupapi.views.event import EventSerializer
from asyncio import events
from urllib import request
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action


class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events']
    
    def setUp(self):
        # Grab the first Gamer object from the database and add their token to the headers
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")



    
        
        
        # NEED TO DEBUG ONE LINE IN THIS ONE:
        
            
    def test_list_events(self):
        """Test list of all events"""
        url = '/events'

        response = self.client.get(url)
        
        # Get all the events in the DB and serialize them to get the expected output
        all_events = Event.objects.all()
        expected = EventSerializer(all_events, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEqual(expected.data, response.data)
        
       
        
    def test_get_event(self):
        """Test to GET a single event
        """
        # Grab a game object from the database
        event = Event.objects.first()

        url = f'/events/{event.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Like before, run the event through the serializer that's being used in view
        expected = EventSerializer(event)

        # Assert that the response matches the expected return data
        self.assertEqual(expected.data, response.data)
        
        
    
    
        
    def test_delete_event(self):
        """Test delete for an event"""
        event = Event.objects.first()

        url = f'/events/{event.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Test that it was deleted by trying to _get_ the event
        # The response should return a 404
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)





    def test_create_game(self):
            """Create the event test"""
            url = "/events"

            # Define the Event properties
            # The keys should match what the create method is expecting
            # Make sure this matches the code you have
            
            event = {
                "description": "TestDescription",
                "date": "2022-05-26",
                "time": "16:00:00",
                "game_id": 1                       
            }

            response = self.client.post(url, event, format='json')

            # The _expected_ output should come first when using an assertion with 2 arguments
            # The _actual_ output will be the second argument
            # We _expect_ the status to be status.HTTP_201_CREATED and it _actually_ was response.status_code
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            
            # Get the last event added to the database, it should be the one just created
            new_event = Event.objects.last()

            # Since the create method should return the serialized version of the newly created event,
            # Use the serializer you're using in the create method to serialize the "new_event"
            # Depending on your code this might be different
            expected = EventSerializer(new_event)   

            # Now we can test that the expected output matches what was actually returned
        
            self.assertEqual(expected.data, response.data)
            
            
            
            
    def test_change_event(self):
        """test update for an event"""
        # Grab the first event in the DB
        event = Event.objects.first()

        url = f'/events/{event.id}'

        updated_event = {
            "description": f'{event.description} updated',
            "date": event.date,
            "time": event.time,
            "game": event.game_id
        }

        response = self.client.put(url, updated_event, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Refresh the game object to reflect any changes in the database
        event.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_event['description'], event.description)