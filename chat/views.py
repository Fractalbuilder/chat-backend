from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import time
from django.http import StreamingHttpResponse
from .models import User, Message
import datetime

def index(request):
    return render(request, "general/index.html")

@csrf_exempt
def chat_messages(request):
    def event_stream():
        while True:
            messages = list(Message.objects.values())
            yield 'data:' + json.dumps(messages) + '\n\n'
            print("Info sent")
            time.sleep(1)
    
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

@csrf_exempt
def login(request):
    if request.method == "POST":
        # Attempt to sign user in
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            return JsonResponse({"message": "User logged in", "userId": user.id, "username": username}, status=201)
        else:
            return JsonResponse({"message": "User not logged in"}, status=201)
    else:
        return JsonResponse({"message": "Invalid opperation"}, status=201)

@csrf_exempt
def messages_api(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        userId = data['userId']
        username = data['username']
        text = data['text']
        date = datetime.datetime.now()        
        Message(userId=userId, username=username, text=text, datetime=str(date)).save()
        return JsonResponse({"message": "Message added."}, status=201)

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        email = ''
        password = data['password']
        confirmation = password

        if password != confirmation:
            return JsonResponse({"message": "Password doesn't match"}, status=201)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return JsonResponse({"message": "User already taken"}, status=201)

        return JsonResponse({"message": "User added", "userId": user.id, "username": username}, status=201)
    else:
        return JsonResponse({"message": "Invalid opperation"}, status=201)