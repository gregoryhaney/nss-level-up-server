"""Module for generating events by user report"""
from email.errors import FirstHeaderLineIsContinuationDefect
from django.shortcuts import render
from django.db import connection
from django.views import View
from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all events along with the gamer first name, last name, and id
            db_cursor.execute("""
                    SELECT
                        g.title,
                        e.organizer_id,
                        e.description,
                        e.date,
                        e.time,
                        e.game_id,
                        r.id AS GamerId,
                        r.user_id,
                        u.first_name || " " || 
                        u.last_name AS Name,
                        u.id AS ID
                    FROM levelupapi_game AS g
                    JOIN levelupapi_event as e
                        ON g.id = e.game_id
                    JOIN levelupapi_gamer AS r
                        ON e.organizer_id = r.id
                    JOIN auth_user AS u
                        ON r.id = u.id          
            """)
                
                    
                
            # Pass the db_cursor to the dict_fetch_all function to turn the 
            #   fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the events_by_user list:
                       
            ###  NEW DATA STRUCTURE FOR EVENTS           
            
            # [
            #     {
            #         "gamer_id": 1,
            #         "full_name": "Molly Ringwald",
            #         "events": [
            #         {
            #             "id": 5,
            #             "date": "2020-12-23",
            #             "time": "19:00",
            #             "game_name": "Fortress America"
            #         }
            #         ]
            #     }
            # ]
            
            
            
            
            
            

            events_by_user = [ ]

            for row in dataset:
                # TODO: Create a dictionary called event that includes 
                # the gamer name, event description, game title, date, time,
                # from the row dictionary
                event = {
                    "id": row['ID'],
                    "title": row['title'],
                    "date": row['date'],
                    "time": row['time'],
                    "description": row['description'],
                    "id": row['GamerId']
                }
                
                # See if the gamer has been added to the games_by_user list already
                user_dict = None
                for user_event in events_by_user:
                     if user_event['gamer_id'] == row['GamerId']:
                         user_dict = user_event
                
                
                if user_dict:
                    # If the user_dict is already in the games_by_user list, 
                    # append the game to the games list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the games_by_user list, 
                    # create and add the user to the list
                    events_by_user.append({
                        "gamer_id": row['GamerId'],
                        "full_name": row['Name'],
                        "events": [event]
                    })
        
        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
