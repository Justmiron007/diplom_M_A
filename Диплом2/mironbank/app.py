from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import Config

# Инициализация приложения Flask
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация расширений для приложения
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


# Определение модели User для базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Главная страница
@app.route('/')
def home():
    return render_template('home_page.html')


# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    info = {}  # Словарь для хранения ошибок при регистрации
    if request.method == 'POST':
        # Получение данных из формы
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repeat_password = request.form['repeat_password']

        if password != repeat_password:
            info['error'] = 'Пароли не совпадают!'
        elif User.query.filter_by(username=username).first():
            info['error'] = 'Пользователь с таким логином уже существует!'
        elif User.query.filter_by(email=email).first():
            info['error'] = 'Эл. почта уже используется другим пользователем'
        else:
            # Хеширование пароля перед сохранением в базе данных
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)  # Добавление нового пользователя в сессию базы данных
            db.session.commit()  # Применение изменений в базе данных
            return render_template('success_page.html', message=f'Приветствуем, {username}!')

    return render_template('registration_page.html', info=info)


# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Получение данных из формы
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()  # Поиск пользователя по логину

        # Проверка, если пользователь существует и пароль правильный
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return render_template('success_page.html', message=f'Добро пожаловать, {username}!')
        else:
            return render_template('login_page.html', error='Неверное имя пользователя или пароль')
    return render_template('login_page.html')


# Страница успешного входа
@app.route('/success')
def success():
    if 'user_id' in session:  # Проверка, если пользователь авторизован
        user = User.query.get(session['user_id'])  # Получение текущего пользователя по ID из сессии
        return render_template('success_page.html', message=f'Приветствуем, {user.username}!')
    # Если пользователь не авторизован, перенаправление на главную страницу
    return redirect(url_for('home'))


# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
