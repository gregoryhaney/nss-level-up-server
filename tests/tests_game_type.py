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
from levelupapi.models import GameType, Gamer
from levelupapi.views.game_type import GameTypeSerializer


class GameTypeTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events']
    
    def setUp(self):
        # Grab the first Gamer object from the database and add their token to the headers
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


    
        
        
    def test_get_gametypes(self):
        """Get GameType Test
        """
        # Grab a gametype object from the database
        gametype = GameType.objects.first()

        url = f'/gametypes/{gametype.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Like before, run the game through the serializer that's being used in view
        expected = GameTypeSerializer(gametype)

        # Assert that the response matches the expected return data
        self.assertEqual(expected.data, response.data)
        
        
        
    def test_list_gametypes(self):
        """Test list gametypes"""
        url = '/gametypes'

        response = self.client.get(url)
        
        # Get all the gametypes in the DB and serialize them to get the expected output
        all_gametypes = GameType.objects.all()
        expected = GameTypeSerializer(all_gametypes, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEqual(expected.data, response.data)
        
