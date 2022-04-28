"""levelup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from levelupapi.views import register_user, login_user, GameTypeView
from levelupapi.views import GameView, EventView
from rest_framework import routers

        # "trailing_slash=False" tells router to accept '/gametypes' instead of '/gametypes/'
        # it prevents errors where the fetch is missing the slash at the end fo the URL
router = routers.DefaultRouter(trailing_slash=False)
        # this sets up the '/gametypes' resource
            # 1st parameter [ r'gametypes ] sets up the url
            # 2nd parameter [ GameTypeView ] tells server which view to use
            #       when it sees the URL in 1st parameter
            # 3rd parameter [ gametype ] is called "base name". Base name is only seen
            #       with a server error. Base name acts as a 'nickname' for the resource.
            #       Normally, this is the singular version of the URL.
router.register(r'gametypes', GameTypeView, 'gametype')
router.register(r'events', EventView, 'event')
router.register(r'games', GameView, 'game')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]

    # Requests to http://localhost:8000/register are routed to "register_user" FN
    # Requests to http://localhost:8000/login are routed to "login_user" FN
    
    