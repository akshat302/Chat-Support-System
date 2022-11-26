from django.urls import path
from chat_support.views import send_msg, receive_reply, save_reply, get_msg

urlpatterns = [
    path('send_msg/', send_msg, name="send_msg"),
    path('receive_reply/<int:user_id>/<int:msg_id>/', receive_reply, name="receive_reply"),
    path('save_reply/', save_reply, name="save_reply"),
    path('get_msg/', get_msg, name="get_msg")
]