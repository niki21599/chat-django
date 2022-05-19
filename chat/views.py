from cgitb import text
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.core import serializers

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    """
    This is the endpoint to load the Chat html and the endpoint to post a Message to the databas    
    
    """

    if request.method == "POST":
        request.POST["textmessage"]
        myChat = Chat.objects.get(id=1)
        new_Message = Message.objects.create(text=request.POST["textmessage"], chat=myChat, author=request.user, receiver=request.user)
        new_Message_Json = serializers.serialize("json", [new_Message])
        return JsonResponse(new_Message_Json[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id = 1)

    return render(request, "chat/index.html", {"messages": chatMessages})

def login_view(request):
    """
    This is the endpoint to login. 
    It requires a username and a password
    It returns a json with either {login: true} or {login: false}. If the login is sucessful it authenticates the user    
    
    """
    if request.method == "POST":
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user: 
            login(request, user)
            return JsonResponse({"login": True}, safe=False)
        else:
            return JsonResponse({"login": False}, safe=False)
    
    return render(request, "auth/login.html")

def register(request):
    """
    This is the endpoint to create a new user. 
    It requires following data: 
    1. username
    2. first_name
    3. last_name
    4. email
    5. password
    6. password_repeat
    It return one of the following options: 
    1. {"success": True} if the data is correct. It creates the new User
    2. {"success": False, "errorMessage": "Username already exists" } if the username already exists.
    3. {"success": False, "errorMessage": "Passwords don't match" } if password and password_repeat are not the same. 
    
    """
    if request.method == "POST":
        username=request.POST["username"]
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        email=request.POST["email"]
        password=request.POST["password"]
        password_repeat=request.POST["password_repeat"]
        
        if password == password_repeat:
            print("create user")
            try:
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return JsonResponse({"success": True}, safe=False)
            except IntegrityError:
                return JsonResponse({"success": False, "errorMessage": "Username already exists" }, safe=False) 
        else:
            return JsonResponse({"success": False, "errorMessage": "Passwords don't match" }, safe=False)
         
        
    return render(request, "auth/register.html") 

def logout_view(request):

    """
    This endpoint logs the user out and returns to the login Page. 
    """

    logout(request)
    return render(request, "auth/login.html")
    
    
