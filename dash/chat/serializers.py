from chat.models import ChatSession, ChatSessionMessage
from django.contrib.auth.models import User
from rest_framework import serializers


class ChatUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        user = obj
        name = f"{user.first_name} {user.last_name}"
        return name

    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'last_login',
        ]


class ChatSessionMessageSerializer(serializers.ModelSerializer):
    nama = serializers.SerializerMethodField()

    def get_nama(self, obj):
        # get role user
        user = obj.user
        name = f"{user.first_name} {user.last_name}"
        return name

    class Meta:
        model = ChatSessionMessage
        fields = "__all__"


class SimpleChatSessionSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField()

    def get_uri(self, obj):
        return obj.id.hex

    class Meta:
        model = ChatSession
        fields = "__all__"


class ChatSessionSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()

    def get_uri(self, obj):
        return obj.id.hex

    def get_last_message(self, obj):
        return obj.get_last_message()

    def get_member(self, obj):
        context = self.context
        user = None
        request = context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            member = obj.members.all().exclude(id=user.id).first()
            srz = ChatUserSerializer(member)
            return srz.data

        return None

    class Meta:
        model = ChatSession
        fields = "__all__"
