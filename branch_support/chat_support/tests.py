from django.test import TestCase, Client
from chat_support.models import Message
from chat_support.views import send_msg, receive_reply, get_msg, save_reply
from django.test import TestCase
import pdb
from django.utils import timezone
# Create your tests here.
class TestChatSupport(TestCase):

    def test_send_msg(self):

        data = {"user_id":2, "message_text": "When is the due date", "priority":2}

        c = Client()
        response = c.post(path="/send_msg/", data=data)

        self.assertEqual(response.status_code, 201) 
        
    
        msg_id = response.json()["msg_id"]

        self.assertIsNotNone(msg_id)

        message = Message.objects.filter(id=msg_id).first()
        self.assertIsNotNone(message)

        self.assertEqual(message.message_text, data["message_text"])
 
    def test_save_reply(self):

            timestamp = timezone.now()
            message = Message.objects.create(user_id=21, message_text="Any response to my above queries please???", priority=13, to_be_replied=True, timestamp=timestamp)
            
            data = {"user_id":message.user_id, "msg_id":message.id, "message_text":"Sure we'll look into it"}

            c = Client()
        
            response = c.post(path="/save_reply/", data=data)

            self.assertEqual(response.status_code, 201)

            msg_id = response.json()["msg_id"]
            self.assertIsNotNone(msg_id)

            reply = Message.objects.filter(id=msg_id).first()

            self.assertIsNotNone(reply)

            self.assertEqual(reply.message_text, data["message_text"])
    

    def test_receive_reply(self):

        timestamp = timezone.now()
        message = Message.objects.create(user_id=21, message_text="Any response to my above queries please???", priority=13, to_be_replied=True, timestamp=timestamp)
        reply_message = Message.objects.create(user_id=22, message_text="We are working on it", parent_id_id=message.id, timestamp=timestamp)

        c = Client()

        response = c.get(path=f"/receive_reply/{reply_message.user_id}/{message.id}/")

        self.assertEqual(response.status_code, 200)

        reply_message_text = response.json()["reply_message"]
        self.assertEqual(reply_message_text, reply_message.message_text)


    def test_get_msg(self):
        
        timestamp = timezone.now()
        message_1 = Message.objects.create(user_id=21, message_text="Any response to my above queries please???", priority=13, timestamp=timestamp)
        message_2 = Message.objects.create(user_id=22, message_text="What SMSs should i accumulate on my phone?", priority=12, timestamp=timestamp)
    
        c = Client()

        response_1 = c.get(path="/get_msg/")

        self.assertEqual(response_1.status_code, 200)

        message_text = response_1.json()["message_text"]
        msg_id = response_1.json()["msg_id"]

        self.assertIsNotNone(msg_id)
        self.assertEqual(message_text, message_2.message_text) # because message 2 priority is higher

        response_2 = c.get(path="/get_msg/")

        self.assertEqual(response_2.status_code, 200)

        message_text = response_2.json()["message_text"]
        msg_id = response_2.json()["msg_id"]

        self.assertIsNotNone(msg_id)
        self.assertEqual(message_text, message_1.message_text)

    
