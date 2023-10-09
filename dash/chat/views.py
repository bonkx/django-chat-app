# Create your views here.
import json
import random

from chat.models import ChatSession
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render

# Create your views here.


@login_required
def index(request):
    avatar_list = [
        "/static/assets/img/user1-128x128.jpg",
        "/static/assets/img/user3-128x128.jpg",
        "/static/assets/img/user4-128x128.jpg",
        "/static/assets/img/user8-128x128.jpg",
    ]
    user_avatar = random.choice(avatar_list)

    queryset = ChatSession.objects.filter(members=request.user)

    queryset = queryset
    page = request.GET.get("page", 1)
    paginator = Paginator(queryset, 10)

    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    context = {
        "object_list": object_list,
        "user_avatar": user_avatar,
        "avatar_list": avatar_list,
    }

    return render(request, "chat/index.html", context)


@login_required
def create_room(request, id):
    user = request.user
    member_id = id
    members = [user.id, member_id]

    # cek chat session yg ada members = member_id
    queryset = ChatSession.objects.filter(
        members__id=member_id).filter(members=user)

    if queryset.exists():
        # status = "chat exists"
        obj = queryset.first()
    else:
        # status = "chat create"
        obj = ChatSession()
        obj.save()

        # # add member to chat session
        for m in members:
            obj.members.add(m)

    return redirect('room', room_name=obj.id.hex)


@login_required
def room(request, room_name):
    user = request.user
    avatar_list = [
        "/static/assets/img/user1-128x128.jpg",
        "/static/assets/img/user3-128x128.jpg",
        "/static/assets/img/user4-128x128.jpg",
        "/static/assets/img/user8-128x128.jpg",
    ]
    user_avatar = random.choice(avatar_list)

    queryset = ChatSession.objects.filter(members=user)

    queryset = queryset
    page = request.GET.get("page", 1)
    paginator = Paginator(queryset, 10)

    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    member_avatar = random.choice(avatar_list)

    cs = ChatSession.objects.filter(id=room_name).first()
    member = cs.members.all().exclude(id=user.id).first()

    context = {
        "object_list": object_list,
        "user_avatar": user_avatar,
        "avatar_list": avatar_list,
        "room_name": room_name,
        "str_room_name": member.email,
        "member_avatar": member_avatar,
        "last_seen": member.last_login
    }
    return render(request, "chat/room.html", context)


@login_required
def ajax_delete_chat(request, id):
    try:
        ChatSession.objects.filter(id=id).delete()
        messages.success(request, "Delete sukses!")
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
