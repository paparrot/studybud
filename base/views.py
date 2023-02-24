from django.shortcuts import render, redirect
from .models import Room
from django.http import HttpResponse
from .forms import RoomForm


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


def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms')

    context = {'form': form}
    return render(request, 'room_form.html', context)


def update_room(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('rooms')

    context = {
        'room': room,
        'form': form,
    }

    return render(request, 'room_form.html', context)

def delete_room(request, id):
    room = Room.objects.get(id=id)

    if request.method == "POST":
        room.delete()
        return redirect('rooms')

    return render(request, 'delete.html', { 'object': room})