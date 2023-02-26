from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.api.serializers import RoomSerializer
from base.models import Room


@api_view(['GET'])
def get_routes(request):
    data = {
        'routes': [
            'GET /api',
            'GET /api/rooms',
            'GET /api/rooms/:id'
        ]
    }
    return Response(data)


@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_room(request, id):
    room = Room.objects.get(id=id)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
