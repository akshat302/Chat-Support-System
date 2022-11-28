from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from chat_support.models import Message
from django.db import transaction
import json

app_name = "chat_support"
# Create your views here.

message_state = {}

def send_msg(request):

    if request.method == "POST":

        data = request.POST
        user_id = data.get("user_id")
        message_text = data.get("message_text")
        priority = data.get("priority")
        timestamp = timezone.now()

        message = Message.objects.create(user_id=user_id, message_text=message_text,timestamp=timestamp, parent_id=None,priority=priority)
        
        ctx = {
            "msg_id" : message.id
        }
        
        return HttpResponse(json.dumps(ctx), status=201, content_type="application/json")
    
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
    
    return HttpResponse(status=401)


def save_reply(request):

    if request.method == "POST":

        data = request.POST

        user_id = data.get("user_id")
        msg_id = data.get("msg_id")
        reply_text = data.get("message_text")

        if msg_id is None:
            return HttpResponse(status=500)

        timestamp = timezone.now()
        message = Message.objects.filter(id=msg_id, to_be_replied=True).first()
    
        
        if message is not None:

            reply = Message.objects.create(
                user_id=user_id, 
                message_text=reply_text, 
                timestamp=timestamp, 
                parent_id=message, 
            )

            ctx = {
                "msg_id":reply.id
            }

            return HttpResponse(json.dumps(ctx), content_type="application/json", status=201)

        else:

            return HttpResponse(status=501)

    return HttpResponse(status=401)

def get_msg(request):

    if request.method == "GET":

        with transaction.atomic():
            message = Message.objects.select_for_update().filter(parent_id=None, to_be_replied=False).order_by("priority").first() 
    
            if message is None:
                ctx = {
                    "message_text":"No new messages",
                    "msg_id":None
                }
            
            else:
                message.to_be_replied = True
                message.save()
                
                ctx = {
                    "message_text":message.message_text,
                    "msg_id" : message.id
                }


        return HttpResponse(json.dumps(ctx), content_type="application/json", status=200)

    return HttpResponse(status=401)