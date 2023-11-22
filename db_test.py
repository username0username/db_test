import sqlite3
import re
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QCheckBox, QLabel, QMessageBox, QTextEdit

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setFixedSize(600,700)

        self.connection = sqlite3.connect("database.db")
        self.create_table_if_not_exists()
        self.update_output()


    def create_table_if_not_exists(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                surname TEXT,
                name TEXT,
                email TEXT,
                password TEXT,
                day TEXT,
                month TEXT,
                year TEXT,
                gender TEXT
            )
        ''')
        self.connection.commit()

    def initUI(self):
        layout = QVBoxLayout()

        Label1 = QLabel("Создание аккаунта", self)
        layout.addWidget(Label1)  

        self.surnameLE = QLineEdit(self)
        self.surnameLE.setPlaceholderText("Фамилия")
        layout.addWidget(self.surnameLE)

        self.nameLE = QLineEdit(self)
        self.nameLE.setPlaceholderText("Имя")
        layout.addWidget(self.nameLE)

        self.emailLE = QLineEdit(self)
        self.emailLE.setPlaceholderText("E-Mail")
        layout.addWidget(self.emailLE)

        self.passLE = QLineEdit(self)
        self.passLE.setPlaceholderText("Пароль")
        self.passLE.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passLE)

        Label2 = QLabel("Дата рождения", self)
        layout.addWidget(Label2)  

        self.dayCB = QComboBox(self)
        self.dayCB.addItems([str(i) for i in range(1, 32)])
        layout.addWidget(self.dayCB)

        self.monthCB = QComboBox(self)
        self.monthCB.addItems(["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"])
        layout.addWidget(self.monthCB)

        self.yearCB = QComboBox(self)
        self.yearCB.setPlaceholderText("2000")
        self.yearCB.addItems([str(i) for i in range(1900, 2023)])
        layout.addWidget(self.yearCB)
 
        Label3 = QLabel("Пол", self)
        layout.addWidget(Label3)  

        self.maleChB = QCheckBox("Мужской", self)
        self.maleChB.setChecked(True)
        layout.addWidget(self.maleChB)

        self.femaleChB = QCheckBox("Женский", self)
        layout.addWidget(self.femaleChB)

        self.maleChB.clicked.connect(self.onMaleCheckboxClicked)
        self.femaleChB.clicked.connect(self.onFemaleCheckboxClicked)

        button = QPushButton('Регистрация', self)
        button.clicked.connect(self.onButtonClick)
        layout.addWidget(button)

        self.outputTextEdit = QTextEdit(self)
        self.outputTextEdit.setReadOnly(True)
        layout.addWidget(self.outputTextEdit)

        self.setLayout(layout)

    def onMaleCheckboxClicked(self):
        if self.maleChB.isChecked():
            self.femaleChB.setChecked(False)

    def onFemaleCheckboxClicked(self):
        if self.femaleChB.isChecked():
            self.maleChB.setChecked(False)

    def validateEmail(self, email):
        email_format = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_format, email) is not None

    def validateName(self, name):
        return name.isalpha() or name.isspace()

    def onButtonClick(self):
        sur = self.surnameLE.text()
        name = self.nameLE.text()
        email = self.emailLE.text()

        if not self.validateName(sur) or not self.validateName(name):
            QMessageBox.warning(self, "Ошибка", "Имя и фамилия могут содержать только буквы и пробелы.")
            return
        if not self.validateEmail(email):
            QMessageBox.warning(self, "Ошибка", "Неверный формат электронной почты.")
            return

        passwrd = self.passLE.text()
        day = self.dayCB.currentText()
        month = self.monthCB.currentText()
        year = self.yearCB.currentText()
        gender = ""
        if self.maleChB.isChecked():
            gender = "Мужской"
        elif self.femaleChB.isChecked():
            gender = "Женский"

        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_account = cursor.fetchone()

        if existing_account:
            QMessageBox.warning(self, "Ошибка", "Аккаунт с таким email уже существует.")
        else:
            cursor.execute('''
                INSERT INTO users (surname, name, email, password, day, month, year, gender)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (sur, name, email, passwrd, day, month, year, gender))
            self.connection.commit()

            #print("Имя:", name, "\nФамилия:", sur, "\nEmail:", email, "\nПароль:", passwrd)
            #print("Дата рождения: ", f"{day} {month} {year}")
            #print("Пол:", gender)

            QMessageBox.information(self, "Готово", "Аккаунт зарегестрирован.")
            self.update_output()

    def update_output(self):
        self.outputTextEdit.clear()

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()

        for row in data:
            self.outputTextEdit.append(str(row))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())