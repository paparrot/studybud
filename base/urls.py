from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('rooms/', views.rooms, name="rooms"),
    path('rooms/<int:id>', views.room, name="room"),
    path('rooms/create', views.create_room, name="create-room"),
    path('rooms/<int:id>/update', views.update_room, name="update-room"),
    path('rooms/<int:id>/delete', views.delete_room, name="delete-room")
]
