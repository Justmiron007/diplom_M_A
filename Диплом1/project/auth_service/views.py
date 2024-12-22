from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from .forms import UserRegister
from django.contrib.auth.hashers import make_password, check_password


# Главная страница
def home_page(request):
    return render(request, "auth_service/home_page.html")


# Страница регистрации
def registration(request):
    # Словарь для хранения информации об ошибках
    info = {}

    # Создание формы регистрации
    form = UserRegister(request.POST or None)

    # Если метод запроса POST и форма прошла валидацию
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        repeat_password = form.cleaned_data["repeat_password"]
        email = form.cleaned_data["email"]

        # Проверка на совпадение паролей
        if password != repeat_password:
            info["error"] = "Пароли не совпадают"
        # Проверка, существует ли пользователь с таким логином
        elif User.objects.filter(username=username).exists():
            info["error"] = "Пользователь с таким логином уже существует"
        # Проверка, используется ли уже этот email
        elif User.objects.filter(email=email).exists():
            info["error"] = "Эл. почта уже используется другим пользователем"
        else:
            # Хеширование пароля перед сохранением в базу данных
            hashed_password = make_password(password)
            # Создание нового пользователя и сохранение его в базе данных
            new_user = User(username=username, email=email, password=hashed_password)
            new_user.save()

            # Переадресация на страницу с успешной регистрацией
            return render(request, "auth_service/success_page.html", {
                "message": f"Приветствуем, {username}!"
            })

    # Добавление формы в контекст для отображения на странице
    info["form"] = form
    return render(request, "auth_service/registration_page.html", info)


# Страница логина
def login_page(request):
    # Словарь для хранения информации об ошибках
    info = {}

    # Если метод запроса POST
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Поиск пользователя по имени
        user = User.objects.filter(username=username).first()

        # Проверка, совпадает ли введенный пароль с хешированным паролем в базе данных
        if user and check_password(password, user.password):
            # Переадресация на страницу с успешным входом
            return render(request, "auth_service/success_page.html", {
                "message": f"Добро пожаловать, {username}!"
            })
        else:
            # Если логин или пароль неверны, отображаем ошибку
            info["error"] = "Неверное имя пользователя или пароль"

    return render(request, "auth_service/login_page.html", info)
