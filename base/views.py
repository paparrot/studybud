from django.shortcuts import render, redirect
from .models import Room, Topic
from django.db.models import Q
from django.http import HttpResponse
from .forms import RoomForm


# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    topics = Topic.objects.all()

    if q:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
    else:
        rooms = Room.objects.all()

    rooms_count = rooms.count()
    rooms = rooms[:5]

    return render(request, 'home.html', {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count})


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

    return render(request, 'delete.html', {'object': room})
