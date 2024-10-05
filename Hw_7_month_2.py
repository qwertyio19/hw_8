" Домашнее задание "



import sqlite3


connect = sqlite3.connect("bank_system.db")
cursor = connect.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    age INTEGER NOT NULL,
    address TEXT NOT NULL,
    email TEXT NOT NULL,
    balance REAL DEFAULT 0
)
""")
connect.commit()


def open_account():
    name = input("Введите имя: ")
    surname = input("Введите фамилию: ")
    age = int(input("Введите возраст: "))
    address = input("Введите адрес: ")
    email = input("Введите email: ")
    
    cursor.execute("""
    INSERT INTO accounts (name, surname, age, address, email) 
    VALUES (?, ?, ?, ?, ?)
    """, (name, surname, age, address, email))
    
    connect.commit()
    print("Счет успешно открыт!")


def deposit(account_id, amount):
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    result = cursor.fetchone()
    
    if result:
        new_balance = result[0] + amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
        connect.commit()
        print(f"Счет пополнен на {amount}. Текущий баланс: {new_balance}")
    else:
        print("Счет не найден.")


def withdraw(account_id, amount):
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    result = cursor.fetchone()
    
    if result and result[0] >= amount:
        new_balance = result[0] - amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
        connect.commit()
        print(f"Со счета снято {amount}. Текущий баланс: {new_balance}")
    elif result:
        print("Недостаточно средств на счете.")
    else:
        print("Счет не найден.")


def check_balance(account_id):
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    result = cursor.fetchone()
    
    if result:
        print(f"Текущий баланс счета: {result[0]}")
    else:
        print("Счет не найден.")


while True:
    print("\n1. Открыть счет\n2. Пополнить счет\n3. Снять средства\n4. Проверить баланс\n5. Выйти")
    choice = input("Выберите действие: ")

    if choice == "1":
        open_account()
    elif choice == "2":
        account_id = int(input("Введите ID счета: "))
        amount = float(input("Введите сумму для пополнения: "))
        deposit(account_id, amount)
    elif choice == "3":
        account_id = int(input("Введите ID счета: "))
        amount = float(input("Введите сумму для снятия: "))
        withdraw(account_id, amount)
    elif choice == "4":
        account_id = int(input("Введите ID счета: "))
        check_balance(account_id)
    elif choice == "5":
        break
    else:
        print("Неверный выбор.")