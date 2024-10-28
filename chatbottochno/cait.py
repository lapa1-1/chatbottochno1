# Импортируем необходимые модули из Flask и SQLAlchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Создаем приложение Flask
app = Flask(__name__)

# Указываем настройки базы данных: используем SQLite и файл базы данных users.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем отслеживание изменений для оптимизации
db = SQLAlchemy(app)  # Инициализируем объект SQLAlchemy для взаимодействия с базой данных

# Определяем модель User для таблицы в базе данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор пользователя
    user_id = db.Column(db.String(50), unique=True, nullable=False)  # ID пользователя, должен быть уникальным
    phone_number = db.Column(db.String(20), nullable=False)  # Телефонный номер пользователя

# Создаем маршрут для добавления нового пользователя через POST-запрос
@app.route('/api/submit', methods=['POST'])
def submit_phone():
    # Получаем данные из тела запроса в формате JSON
    data = request.json
    user_id = data.get('user_id')
    phone_number = data.get('phone_number')

    # Проверяем, переданы ли все необходимые данные
    if not user_id or not phone_number:
        return jsonify({'error': 'user_id and phone_number are required'}), 400

    # Проверяем, существует ли пользователь с указанным user_id в базе данных
    existing_user = User.query.filter_by(user_id=user_id).first()
    if existing_user:
        # Если пользователь существует, возвращаем сообщение
        return jsonify({'message': 'User already exists'}), 200

    # Если пользователя нет, создаем нового и сохраняем его в базе данных
    new_user = User(user_id=user_id, phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()  # Подтверждаем изменения

    return jsonify({'message': 'User created'}), 201  # Возвращаем сообщение о создании пользователя

# Создаем маршрут для получения списка всех пользователей через GET-запрос
@app.route('/api/users', methods=['GET'])
def get_users():
    # Извлекаем всех пользователей из базы данных
    users = User.query.all()
    # Формируем список словарей с данными пользователей
    users_list = [{"user_id": user.user_id, "phone_number": user.phone_number} for user in users]
    return jsonify(users_list), 200  # Возвращаем список пользователей

# Проверяем, если модуль запущен как главный, создаем таблицы в базе данных
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаем таблицы (если они не существуют)
    app.run(debug=True)  # Запускаем сервер с отладочным режимом
