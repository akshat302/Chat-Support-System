# Chat Support
### Requirements

- Python 3.6.8
- Django==3.2.11
- django-extensions==3.1.0
- djangorestframework==3.13.1
- ipython==7.13.0
- requests==2.27.1
- pytest==7.0.1


### Steps to run

1. clone the github repo - git clone https://github.com/akshat302/Branch-International.git
2. cd into the Branch-International folder - cd Branch-International/branch_support
3. run python manage.py migrate in the terminal.
4. run python manage.py runserver in the terminal to run the server.
5. To run test corresponding to the API's run `python manage.py test` in the terminal.



## Overview 

Detailed Explanation - https://docs.google.com/document/d/1P0ClLLYY8fbKF373hqhndRWflH8-zNby_FZNPMoMTLk/edit?usp=sharing

### Entities 

1. Message

### Database Models

Message:
	
	user_id : id of the user (Assumed to be unique)
	message_text : content of the message
	timestamp : time and date of the message
	parent_id : id of the message to which reply has to be generated
	to_be_replied - it indicates whether the message is ready to be replied
	priority - determines the priority(importance) of the message, lesser the number more is the priority of the message 
	


### API Details 

send_msg -

    URL - "http://127.0.0.1:8000/send_msg/"
    Type - POST
    Request Body - {"user_id":1, "message_text": "When is the due date", "priority":2}
    Description - Allows the users to send messages(Queries).
    Response - {"msg_id": message.id, "status": 201}




receive_reply - 
    
    URL - "http://127.0.0.1:8000/receive_reply/<user_id>/<msg_id>/"
    Type - GET
    Description - Allows the users to see the reply they get against thier message
    Response - ctx = {
                "user_id": user_id,
                "reply_message":"We are working on it",
                "timestamp": "11/28/22, 17:18:45",
                "reply_ready": True }


get_msg - 

    URL - "http://127.0.0.1:8000/get_msg/"
    Type - GET
    Description - Allows the customer support people to retrieve the messages send by the users.
    Response - ctx = {
                    "message_text":"What SMSs should i accumulate on my phone?",
                    "msg_id" : 2}


save_reply - 

    URL - "http://127.0.0.1:8000/save_reply/"
    Type - POST
    Request Body - {"user_id":1, "msg_id": 4, "message_text": "We are working on it"}
    Description - ALlows the customer support people to send replies against the user's messages
    Response - {"msg_id": message.id, "status": 201}
   
