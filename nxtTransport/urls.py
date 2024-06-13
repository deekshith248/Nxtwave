from django.contrib import admin
from home import views
from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
urlpatterns = [
path('/create', views.createUser),
path('/createV2', views.createUserV2),
]
