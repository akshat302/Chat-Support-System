from django.urls import path
from chat_support.views import send_msg, receive_reply, save_reply

urlpatterns = [
    path('send_msg/', send_msg, name="send_msg"),
    path('receive_reply/<int:user_id>/<int:msg_id>/', receive_reply, name="receive_reply"),
    path('save_reply/', send_reply, name="save_reply")
]