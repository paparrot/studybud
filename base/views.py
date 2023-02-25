from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room, Topic, User, Message
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

    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q) |
        Q(room__name__icontains=q)
    )[:3]

    rooms_count = rooms.count()
    rooms = rooms[:5]

    return render(request, 'home.html', {
        'rooms': rooms,
        'topics': topics,
        'rooms_count': rooms_count,
        'room_messages': room_messages
    })


def rooms(request):
    _rooms = Room.objects.all()
    context = {'rooms': _rooms}
    return render(request, 'rooms.html', context)


def room(request, id):
    try:
        _room = Room.objects.get(id=id)
        _room_messages = _room.message_set.all()
        _room_participants = _room.participants.all()
    except Room.DoesNotExist:
        return HttpResponse("Not found")

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=_room,
            body=request.POST.get('body')
        )
        _room.participants.add(request.user)
        return redirect('room', id=_room.id)

    context = {'room': _room, 'room_messages': _room_messages, 'participants': _room_participants}
    return render(request, 'room.html', context)


@login_required(login_url='login')
def create_room(request):
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')

    topics = Topic.objects.all()
    form = RoomForm()
    context = {'form': form, 'topics': topics}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def update_room(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if request.user != room.host:
        messages.error('You are not allowed here!')
        return redirect('rooms')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    topics = Topic.objects.all()
    context = {
        'room': room,
        'form': form,
        'topics': topics,
    }

    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def delete_room(request, id):
    room = Room.objects.get(id=id)

    if request.method == "POST":
        room.delete()
        return redirect('rooms')

    return render(request, 'delete.html', {'object': room})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login_user.html', {})


def register_user(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
            return redirect('register')

    return render(request, 'register_user.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def delete_message(request, id):
    message = Message.objects.get(id=id)
    room = message.room

    if request.user != message.user:
        messages.error('You are not author of this message')
        return redirect('room', room.id)

    if request.method == 'POST':
        message.delete()
        return redirect('room', room.id)

    return render(request, 'delete.html', {'object': message})


def user(request, id):
    _user = User.objects.get(id=id)
    _rooms = _user.room_set.all()
    _room_messages = _user.message_set.all()
    _topics = Topic.objects.all()

    context = {'user': _user, 'rooms': _rooms, 'topics': _topics, 'room_messages': _room_messages}
    return render(request, 'profile.html', context)
