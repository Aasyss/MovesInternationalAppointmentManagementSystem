from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room
from userregistration.models import User, UserProfile
# Create your views here.



@require_POST
def create_room(request, uuid):
    name = request.POST.get('name','')
    url = request.POST.get('url','')

    Room.objects.create(uuid=uuid, client=name, url=url)

    return JsonResponse({'message': 'Room Created'})


@login_required
def admin(request):
    rooms = Room.objects.all()
    users = User.objects.filter(is_staff=True)

    return render(request, 'live_chat/admin.html', {
        'rooms': rooms,
        'users' : users
    })

@login_required
def room(request, uuid):
    room = Room.objects.get(uuid=uuid)

    if room.status == Room.WAITING:
        room.status = Room.ACTIVE
        room.agent = request.user
        room.save()

    return render(request, 'live_chat/room.html', {
        'room': room,

    })

@login_required
def delete_room(request, uuid):
    if request.user.has_perm('live_chat.delete_room'):
        room = Room.objects.get(uuid=uuid)
        room.delete()
        messages.error(request, "room was deleted")
        return redirect('/chat-admin/')
    else:
        messages.error(request, "you donot have access to delete rooms")
        return redirect('/chat-admin/')