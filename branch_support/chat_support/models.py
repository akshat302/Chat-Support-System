from django.db import models

# Create your models here.

class Message(models.Model):

    user_id = models.IntegerField(default=0) # Assumed to be unique 
    message_text = models.TextField(max_length=1000)
    timestamp = models.DateTimeField()
    parent_id = models.ForeignKey("Message", on_delete=models.CASCADE, null=True)
    is_reply = models.BooleanField(default=False)
    to_be_replied = models.BooleanField(default=False)