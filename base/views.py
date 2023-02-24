from django.shortcuts import render
from .models import Room
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'home.html')


def rooms(request):
    _rooms = Room.objects.all()
    context = {'rooms': _rooms}
    return render(request, 'rooms.html', context)


def room(request, id):
    try:
        _room = Room.objects.get(id=id)
    except Room.DoesNotExist:
        return HttpResponse("Not found")

    context = {'room': _room}
    return render(request, 'room.html', context)
