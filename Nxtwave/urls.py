"""
URL configuration for Nxtwave project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from home import views
from nxtTransport import views as transport_views
from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
urlpatterns = [
path('r/',include('home.urls')),
path('home/sayHelloWithName', views.say_hello_with_name),
path('home/sayHelloWithNameV2', views.say_hello_with_nameV2),
path('home/saveUserDetails', views.save_user_details),
path('404/', views.handle_not_found),
    path('500/', views.handle_server_error),
    path('user/create', transport_views.createUser),
#     path('user/createV2', transport_views.createUserV2),
    path('user/addTransportRequest', transport_views.addTransportRequest),
    path('user/addRide', transport_views.addRide),
    path('user/getTransportRequests', transport_views.getTransportRequests),
     path('user/getMatchingRides', transport_views.getMatchingRides),
     path('user/applyForRide', transport_views.applyForRide),

# path('home/saveUserDetails', views.save_user_details)
]
