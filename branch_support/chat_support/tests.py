from django.test import TestCase, Client
from chat_support.models import Message
from chat_support.views import send_msg, receive_reply, get_msg, save_reply
from django.test import TestCase
import pdb
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

        data = {"user_id":13, "msg_id":9, "message_text":"The loan has been approved"}

        c = Client()
        response = c.post(path="/save_reply/", data=data)

        self.assertEqual(response.status_code, 201)

        #pdb.set_trace()
        msg_id = response.json()["msg_id"]
        self.assertIsNotNone(msg_id)

        reply = Message.objects.filter(id=msg_id).first()

        self.assertIsNotNone(reply)

        self.assertEqual(reply.message_text, data["message_text"])
