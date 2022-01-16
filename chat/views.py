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

#originURL = 'http://127.0.0.1:3000'
originURL = 'https://fb-chat00.herokuapp.com'

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
    
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Access-Control-Allow-Origin'] = originURL
    return response

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
            response = JsonResponse({"message": "User logged in"}, status=201)
            response['Access-Control-Allow-Origin'] = 'https://fb-chat00.herokuapp.com'
            response['Access-Control-Allow-Credentials'] = 'true'
            #response.set_cookie('userId', user.id, { sameSite: 'none', secure: true })
            #response.set_cookie('username', username)
            response.set_cookie(key='userId', value=user.id, samesite='None', secure=True, httponly=False)
            #response.set_cookie(key='username', value=username, samesite='None', secure=True)
            return response
        else:
            response = JsonResponse({"message": "User not logged in"}, status=201)
            response['Access-Control-Allow-Origin'] = originURL
            response['Access-Control-Allow-Credentials'] = 'true'
            return response
    else:
        response = JsonResponse({"message": "Invalid opperation"}, status=201)
        response['Access-Control-Allow-Origin'] = originURL
        response['Access-Control-Allow-Credentials'] = 'true'
        return response

@csrf_exempt
def messages_api(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        userId = data['userId']
        username = data['username']
        text = data['text']
        date = datetime.datetime.now()        
        Message(userId=userId, username=username, text=text, datetime=str(date)).save()
        response = JsonResponse({"message": "Message added."}, status=201)
        response['Access-Control-Allow-Origin'] = 'https://fb-chat00.herokuapp.com'
        return response


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        email = ''
        password = data['password']
        confirmation = password

        if password != confirmation:
            response = JsonResponse({"message": "Password doesn't match"}, status=201)
            response['Access-Control-Allow-Origin'] = originURL
            return response

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            response = JsonResponse({"message": "User already taken"}, status=201)
            response['Access-Control-Allow-Origin'] = originURL
            response['Access-Control-Allow-Credentials'] = 'true'
            return response

        response = JsonResponse({"message": "User added"}, status=201)
        response['Access-Control-Allow-Origin'] = originURL
        response['Access-Control-Allow-Credentials'] = 'true'
        response.set_cookie('userId', user.id)
        response.set_cookie('username', username)
        return response
    else:
        response = JsonResponse({"message": "Invalid opperation"}, status=201)
        response['Access-Control-Allow-Origin'] = originURL
        response['Access-Control-Allow-Credentials'] = 'true'
        return response