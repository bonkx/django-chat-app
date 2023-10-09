import json

from chat.serializers import ChatUserSerializer
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse


def ajax_search_user(request):
    # print(request.POST)
    searched = request.POST.get('search')
    qs = User.objects.filter(
        Q(email__contains=searched) |
        Q(username__contains=searched)
    ).exclude(id=request.user.id)[:20]

    srz = ChatUserSerializer(qs, many=True)

    res = {'search': searched, 'data': srz.data}
    return JsonResponse(res, safe=False)
