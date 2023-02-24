from django.shortcuts import render

_rooms = [
    {
        'id': 1,
        'name': 'Lets learn python'
    },
    {
        'id': 2,
        'name': 'Design with me'
    },
    {
        'id': 3,
        'name': 'Frontend developers'
    }
]


# Create your views here.
def home(request):
    return render(request, 'home.html')


def rooms(request):
    context = {'rooms': _rooms}
    return render(request, 'rooms.html', context)


def room(request, id):
    _room = None

    for i in _rooms:
        if i['id'] == id:
            _room = i
            break

    context = {'room': _room}
    return render(request, 'room.html', context)
