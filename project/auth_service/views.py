from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from .forms import UserRegister
from django.contrib.auth.hashers import make_password, check_password


def home_page(request):
    return render(request, "auth_service/home_page.html")


def registration(request):
    info = {}
    form = UserRegister(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        repeat_password = form.cleaned_data["repeat_password"]
        email = form.cleaned_data["email"]

        if password != repeat_password:
            info["error"] = "Пароли не совпадают"
        elif User.objects.filter(username=username).exists():
            info["error"] = "Пользователь с таким логином уже существует"
        elif User.objects.filter(email=email).exists():
            info["error"] = "Эл. почта уже используется другим пользователем"
        else:
            hashed_password = make_password(password)
            new_user = User(username=username, email=email, password=hashed_password)
            new_user.save()
            return render(request, "auth_service/success_page.html", {
                "message": f"Приветствуем, {username}!"
            })

    info["form"] = form
    return render(request, "auth_service/registration_page.html", info)


def login_page(request):
    info = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username).first()

        if user and check_password(password, user.password):
            return render(request, "auth_service/success_page.html", {
                "message": f"Добро пожаловать, {username}!"
            })
        else:
            info["error"] = "Неверное имя пользователя или пароль"

    return render(request, "auth_service/login_page.html", info)
