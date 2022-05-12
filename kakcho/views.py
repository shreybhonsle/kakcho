from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
def home(request):
    return render(request, 'home/home.html')

def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return render(request,'home/home.html')

def upload(request):
    if request.method == 'POST':
        uploaded_file  = request.FILES['document']
        print(uploaded_file.name)
        print("\n\n")
        print(uploaded_file.size)
        messages.success(request,"Successfully Uploaded File")

    return render(request,'home/home.html')