from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from chat_support.models import Message
import json

app_name = "chat_support"
# Create your views here.

def send_msg(request):

    if request.method == "POST":

        data = request.POST
        print("HHEHHHE", data)
        user_id = data.get("user_id")
        message_text = data.get("message_text")
        timestamp = timezone.now()

        message = Message.objects.create(user_id=user_id, message_text=message_text,timestamp=timestamp, parent_id=None, is_reply=False)
        
        ctx = {
            "msg_id" : message.id
        }
        
        return HttpResponse(json.dumps(ctx), status=201)
    
    return HttpResponse(status=401)


def receive_reply(request, user_id, msg_id):
 
    if request.method == "GET":

        data = Message.objects.filter(user_id=user_id, parent_id_id=msg_id).first()

        if data is not None:
            timestamp = data.timestamp
            timestamp_str = timestamp.strftime("%D, %H:%M:%S") 

            ctx = {
                "user_id": user_id,
                "reply_message":data.message_text,
                "timestamp": timestamp_str,
                "reply_ready": True
            }
        else:
            ctx = {
                "user_id": None,
                "reply_message":None,
                "timestamp":None,
                "reply_ready": False
            }

        return HttpResponse(json.dumps(ctx), content_type="application/json", status=200)

def save_reply(request):

    if request.method == "POST":

        data = request.POST

        user_id = data.get("user_id")
        msg_id = data.get("msg_id")
        reply_text = data.get("message_text")

        timestamp = timezone.now()

        reply = Message.objects.create(user_id=user_id, message_text=reply_text, timestamp=timestamp, parent_id_id=msg_id, is_reply=True)

        ctx = {
            "msg_id":reply.id
        }

        return HttpResponse(json.dumps(ctx), status=201)