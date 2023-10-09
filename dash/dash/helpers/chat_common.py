
from channels.db import database_sync_to_async
from chat.models import ChatSession, ChatSessionMessage
from chat.serializers import ChatSessionMessageSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone


@database_sync_to_async
def update_chat_online(user, is_online):
    # update chat online
    pass


@database_sync_to_async
def update_last_login(self, user_id):
    # update last login
    # print("user connect: ", user_id)
    User.objects.filter(pk=user_id).update(last_login=timezone.now())


@database_sync_to_async
def get_last_10_messages(self, chatId, user_id, chat_type='chat'):
    # print(f"user : {user_id}")

    # update is_read message utk message yg user!=current_user
    is_read = ChatSessionMessage.objects.select_related(
        'user', 'chatsession')\
        .filter(chat_session_id=chatId)\
        .exclude(user_id=user_id).update(is_read=True)
    # print(f"is_read: {is_read}")

    messages = ChatSessionMessage.objects.filter(
        chat_session_id=chatId).order_by('-created')[:25]

    return ChatSessionMessageSerializer(messages, many=True).data


@database_sync_to_async
def get_chat_member(self, chatId, user_id, chat_type='chat'):
    # chat_session = get_current_chat(chatId)
    # print(chat_session)
    # abstract_user = AbstractUser.objects.filter(user_id=user_id).first()
    # # print(abstract_user)
    # if abstract_user.role == AbstractUser.PETANI:
    #     member = AbstractUser.objects.filter(
    #         pegawai_penyuluh=chat_session.pegawaipenyuluh).first()
    # elif abstract_user.role == AbstractUser.PENYULUH:
    #     member = AbstractUser.objects.filter(
    #         petani=chat_session.petani).first()

    res = {
        # 'id': member.user.id,
        # 'is_online': member.is_online,
        # 'last_login': member.user.last_login,
    }
    # print(res)

    return res


@database_sync_to_async
def save_chat(self, user, chatID, message, image=None, chat_type='chat'):
    _now = timezone.now()
    # # print(_now)

    message = ChatSessionMessage.objects.create(
        user=user, chat_session_id=chatID, message=message, image=image
    )

    # # update updated_at chat session for ordering
    ChatSession.objects.filter(pk=chatID).update(updated=_now)

    srz = ChatSessionMessageSerializer(message, many=False)
    return srz.data
