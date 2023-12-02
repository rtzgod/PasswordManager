import tkinter as tk
import tkinter.simpledialog
import tkinter.messagebox
import sqlite3
import random
import string


def create_table():
    # Создаем таблицу, если она не существует
    connection = sqlite3.connect("passwords.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT,
            username TEXT,
            password TEXT,
            master_key TEXT
        )
    ''')
    connection.commit()
    connection.close()


def is_secure_password(password):
    # Проверяем, соответствует ли пароль условиям безопасности
    return len(password) >= 8 and any(char.isupper() for char in password) and any(char in "!@#$%^&*()-_=+" for char in password)


def generate_secure_password():
    # Генерируем новый пароль, удовлетворяющий условиям безопасности
    length = 8
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    password = ''.join(random.choice(chars) for _ in range(length))
    return password


def save_password():
    site = site_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # Проверяем условия безопасности пароля
    if not is_secure_password(password):
        # Выводим окно с рекомендациями
        error_message = "Пароль не соответствует условиям безопасности.\n\n"
        if len(password) < 8:
            error_message += "- Пароль должен содержать не менее 8 символов.\n"
        if not any(char.isupper() for char in password):
            error_message += "- Пароль должен содержать хотя бы одну заглавную букву.\n"
        if not any(char in "!@#$%^&*()-_=+" for char in password):
            error_message += "- Пароль должен содержать хотя бы один специальный символ: !@#$%^&*()-_=+\n"

        # Предлагаем сгенерировать новый пароль
        result = tkinter.messagebox.askyesno(
            "Ошибка", error_message + "\nХотите сгенерировать новый пароль?")
        if result:
            new_password = generate_secure_password()
            password_entry.delete(0, tk.END)
            password_entry.insert(0, new_password)
        return

    # Открываем диалоговое окно для ввода мастер-ключа
    master_key = get_master_key()

    if master_key:
        # Сохраняем пароль в базе данных
        connection = sqlite3.connect("passwords.db")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO passwords (site, username, password, master_key) VALUES (?, ?, ?, ?)',
                       (site, username, password, master_key))
        connection.commit()
        connection.close()

        # Очищаем поля ввода после сохранения
        site_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        # Обновляем отображение
        update_display()


def get_master_key():
    # Открываем диалоговое окно для ввода мастер-ключа
    master_key = tkinter.simpledialog.askstring(
        "Мастер-ключ", "Введите мастер-ключ:", show='*')
    return master_key


def get_password():
    site = search_site_entry.get()
    master_key = search_master_key_entry.get()

    # Получаем пароль из базы данных
    connection = sqlite3.connect("passwords.db")
    cursor = connection.cursor()
    cursor.execute(
        'SELECT password FROM passwords WHERE site=? AND master_key=?', (site, master_key))
    result = cursor.fetchone()
    connection.close()

    if result:
        password_var.set(result[0])
    else:
        password_var.set("Пароль не найден")


def update_display():
    # Очищаем поле Text и заполняем его сохраненными данными
    display_text.config(state=tk.NORMAL)
    display_text.delete(1.0, tk.END)

    # Получаем данные из базы данных
    connection = sqlite3.connect("passwords.db")
    cursor = connection.cursor()
    cursor.execute('SELECT site, username FROM passwords')
    rows = cursor.fetchall()
    connection.close()

    # Вставляем данные в поле Text
    for row in rows:
        display_text.insert(tk.END, f"Сайт: {row[0]}, Логин: {row[1]}\n")

    display_text.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Менеджер паролей")

# Создаем таблицу, если она не существует
create_table()

# Левая часть окна
tk.Label(root, text="Сайт:").grid(row=0, column=0, padx=10, pady=10)
site_entry = tk.Entry(root)
site_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Логин:").grid(row=1, column=0, padx=10, pady=10)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Пароль:").grid(row=2, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Сохранить пароль", command=save_password).grid(
    row=3, columnspan=2, pady=10)

# Правая часть окна
search_frame = tk.LabelFrame(root, text="Получить пароль")
search_frame.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="nsew")

tk.Label(search_frame, text="Сайт:").grid(row=0, column=0, padx=10, pady=10)
search_site_entry = tk.Entry(search_frame)
search_site_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(search_frame, text="Мастер-ключ:").grid(row=1,
                                                 column=0, padx=10, pady=10)
search_master_key_entry = tk.Entry(search_frame, show="*")
search_master_key_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Button(search_frame, text="Получить пароль",
          command=get_password).grid(row=2, columnspan=2, pady=10)

password_var = tk.StringVar()
tk.Label(search_frame, textvariable=password_var).grid(
    row=3, columnspan=2, pady=10)

# Поле Text для отображения сохраненных данных с возможностью прокрутки
display_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
display_text.grid(row=4, columnspan=2, pady=10)

# Кнопка для обновления отображения
tk.Button(root, text="Обновить", command=update_display).grid(
    row=5, columnspan=2, pady=10)

# Запускаем функцию update_display сразу при запуске приложения
update_display()

root.mainloop()
