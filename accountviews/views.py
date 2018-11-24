from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


# Create your views here.
def signup(request):
    if request.method == "POST":
        new_user = UserCreationForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            username = new_user.cleaned_data.get('username')
            raw_password = new_user.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    elif request.method == "GET":
        return redirect('/')