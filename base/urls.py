from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register"),
    path('', views.home, name="home"),
    path('rooms/', views.rooms, name="rooms"),
    path('rooms/<int:id>', views.room, name="room"),
    path('rooms/create', views.create_room, name="create-room"),
    path('rooms/<int:id>/update', views.update_room, name="update-room"),
    path('rooms/<int:id>/delete', views.delete_room, name="delete-room"),
    path('messages/<int:id>/delete', views.delete_message, name='delete-message'),
]
