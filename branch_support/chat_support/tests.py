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
 
    # def test_save_reply(self):

    #         data = {"user_id":19, "msg_id":10, "message_text":"The loan has been approved"}

    #         c = Client()
    #         #pdb.set_trace()
    #         response = c.post(path="/save_reply/", data=data)

    #         self.assertEqual(response.status_code, 201)

    #         #pdb.set_trace()
    #         msg_id = response.json()["msg_id"]
    #         self.assertIsNotNone(msg_id)

    #         reply = Message.objects.filter(id=msg_id).first()

    #         self.assertIsNotNone(reply)

    #         self.assertEqual(reply.message_text, data["message_text"])
    

    # def test_get_msg(self):

    #     message = Message.objects.create(user_id=21, message_text="Any response to my above queries please???", priority=13)
    #     reply_message = Message.objects.create(user_id=21, message_text="Any response to my above queries please???", priority=13)
    #     #message_2 = Message.objects.create(user_id=22, message_text="What SMSs should i accumulate on my phone?", priority=12)
    #     #message_3 = Message.objects.create(user_id=23, message_text="Hi, kindly can i have the batch number", priority=11)

    #     c = Client()

    #     response = c.get(path="/receive_reply/{message_1.user_id}/{message_1}")


    def test_receive_reply(self):

        timestamp = timezone.now()
        message = Message.objects.create(user_id=21, message_text="Any response to my above queries please???", priority=13, to_be_replied=True, timestamp=timestamp)
        reply_message = Message.objects.create(user_id=22, message_text="We are working on it", parent_id_id=message.id, timestamp=timestamp)

        c = Client()

        response = c.get(path=f"/receive_reply/{reply_message.user_id}/{message.id}/")

        self.assertEqual(response.status_code, 200)

        reply_message_text = response.json()["reply_message"]
        self.assertEqual(reply_message_text, reply_message.message_text)



