import sys
import json
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QMessageBox, QStackedWidget)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont


class AnagramGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анаграммы")
        self.setFixedSize(800, 600)

        # Загрузка слов
        self.words = self.load_words()

        # Основной стек виджетов для переключения между экранами
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Создаем все экраны
        self.create_main_menu()
        self.create_level_menu()
        self.create_help_screen()
        self.create_game_screen()
        self.create_result_screen()

        # Показываем главное меню
        self.stack.setCurrentIndex(0)

    def load_words(self):
        try:
            with open('words.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            # Если файл не найден, создаем пример словаря
            default_words = {
                "легкий": ["кот", "дом", "лес", "нос", "рот", "сад", "год", "сон"],
                "средний": ["книга", "стол", "окно", "дверь", "ручка", "лист", "вода", "ночь"],
                "сложный": ["компьютер", "программа", "клавиатура", "монитор", "мышка", "кресло", "стол", "лампа"]
            }
            with open('words.json', 'w', encoding='utf-8') as file:
                json.dump(default_words, file, ensure_ascii=False, indent=4)
            return default_words

    def create_main_menu(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Анаграммы")
        title.setFont(QFont('Arial', 36))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title, stretch=2)

        # Кнопки
        btn_play = QPushButton("Играть")
        btn_play.setFont(QFont('Arial', 18))
        btn_play.clicked.connect(lambda: self.stack.setCurrentIndex(1))  # Переход к выбору уровня
        layout.addWidget(btn_play, stretch=1)

        btn_help = QPushButton("Руководство")
        btn_help.setFont(QFont('Arial', 18))
        btn_help.clicked.connect(lambda: self.stack.setCurrentIndex(2))  # Переход к руководству
        layout.addWidget(btn_help, stretch=1)

        btn_exit = QPushButton("Выход")
        btn_exit.setFont(QFont('Arial', 18))
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit, stretch=1)

        # Добавляем отступы
        layout.addStretch(2)
        widget.setLayout(layout)
        self.stack.addWidget(widget)

    def create_level_menu(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Выбор сложности")
        title.setFont(QFont('Arial', 36))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title, stretch=1)

        # Кнопки уровней
        btn_easy = QPushButton("Легкий")
        btn_easy.setFont(QFont('Arial', 18))
        btn_easy.clicked.connect(lambda: self.start_level("легкий"))
        layout.addWidget(btn_easy, stretch=1)

        btn_medium = QPushButton("Средний")
        btn_medium.setFont(QFont('Arial', 18))
        btn_medium.clicked.connect(lambda: self.start_level("средний"))
        layout.addWidget(btn_medium, stretch=1)

        btn_hard = QPushButton("Сложный")
        btn_hard.setFont(QFont('Arial', 18))
        btn_hard.clicked.connect(lambda: self.start_level("сложный"))
        layout.addWidget(btn_hard, stretch=1)

        btn_back = QPushButton("Назад")
        btn_back.setFont(QFont('Arial', 18))
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))  # Возврат в главное меню
        layout.addWidget(btn_back, stretch=1)

        # Добавляем отступы
        layout.addStretch(2)
        widget.setLayout(layout)
        self.stack.addWidget(widget)

    def create_help_screen(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Правила игры")
        title.setFont(QFont('Arial', 36))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Текст правил
        rules = QLabel(
            "Цель игры - составить исходное слово из перемешанных букв.\n\n"
            "1. Выберите уровень сложности (легкий, средний, сложный).\n"
            "2. Вам будет показано слово с перемешанными буквами.\n"
            "3. Нажимайте на буквы в правильном порядке, чтобы составить слово.\n"
            "4. Если ошиблись - нажмите кнопку 'Отмена' для отмены последней буквы.\n"
            "5. Если хотите начать заново - вернитесь в меню выбора уровня.\n\n"
            "Удачи в игре!"
        )
        rules.setFont(QFont('Arial', 14))
        rules.setAlignment(Qt.AlignLeft)
        layout.addWidget(rules)

        # Кнопка назад
        btn_back = QPushButton("Назад")
        btn_back.setFont(QFont('Arial', 18))
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))  # Возврат в главное меню
        layout.addWidget(btn_back)

        widget.setLayout(layout)
        self.stack.addWidget(widget)

    def create_game_screen(self):
        self.game_widget = QWidget()
        layout = QVBoxLayout()

        # Верхняя панель с уровнем и кнопкой назад
        top_layout = QHBoxLayout()

        self.level_label = QLabel()
        self.level_label.setFont(QFont('Arial', 14))
        top_layout.addWidget(self.level_label)

        top_layout.addStretch()

        btn_back = QPushButton("Назад")
        btn_back.setFont(QFont('Arial', 14))
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(1))  # Возврат к выбору уровня
        top_layout.addWidget(btn_back)

        layout.addLayout(top_layout)

        # Поле для ввода слова
        self.word_display = QLabel()
        self.word_display.setFont(QFont('Arial', 24))
        self.word_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.word_display)

        # Виртуальная клавиатура
        self.keyboard_widget = QWidget()
        self.keyboard_layout = QHBoxLayout()
        self.keyboard_widget.setLayout(self.keyboard_layout)
        layout.addWidget(self.keyboard_widget)

        # Кнопка отмены
        btn_undo = QPushButton("Отмена")
        btn_undo.setFont(QFont('Arial', 14))
        btn_undo.clicked.connect(self.undo_last_letter)
        layout.addWidget(btn_undo)

        self.game_widget.setLayout(layout)
        self.stack.addWidget(self.game_widget)

    def create_result_screen(self):
        self.result_widget = QWidget()
        layout = QVBoxLayout()

        self.result_label = QLabel()
        self.result_label.setFont(QFont('Arial', 24))
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        self.correct_word_label = QLabel()
        self.correct_word_label.setFont(QFont('Arial', 18))
        self.correct_word_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.correct_word_label)

        btn_menu = QPushButton("В меню")
        btn_menu.setFont(QFont('Arial', 18))
        btn_menu.clicked.connect(lambda: self.stack.setCurrentIndex(0))  # Возврат в главное меню
        layout.addWidget(btn_menu)

        self.result_widget.setLayout(layout)
        self.stack.addWidget(self.result_widget)

    def start_level(self, level):
        self.current_level = level
        self.current_word = random.choice(self.words[level])
        self.scrambled_word = self.scramble_word(self.current_word)
        self.user_input = []

        # Обновляем интерфейс игры
        self.level_label.setText(f"Уровень: {level}")
        self.word_display.setText("")

        # Очищаем клавиатуру
        for i in reversed(range(self.keyboard_layout.count())):
            self.keyboard_layout.itemAt(i).widget().setParent(None)

        # Создаем кнопки с буквами
        for letter in self.scrambled_word:
            btn = QPushButton(letter)
            btn.setFont(QFont('Arial', 18))
            btn.setFixedSize(QSize(60, 60))
            btn.clicked.connect(self.letter_clicked)
            self.keyboard_layout.addWidget(btn)

        self.stack.setCurrentIndex(3)  # Переключаемся на экран игры

    def scramble_word(self, word):
        letters = list(word)
        random.shuffle(letters)
        return ''.join(letters)

    def letter_clicked(self):
        sender = self.sender()
        letter = sender.text()

        # Проверяем, что буква еще не была использована
        if self.scrambled_word.count(letter) > self.user_input.count(letter):
            self.user_input.append(letter)
            self.word_display.setText(''.join(self.user_input))

            # Проверяем победу
            if ''.join(self.user_input) == self.current_word:
                self.show_result(True)

    def undo_last_letter(self):
        if self.user_input:
            self.user_input.pop()
            self.word_display.setText(''.join(self.user_input))

    def show_result(self, win):
        if win:
            self.result_label.setText("Уровень завершен! Победа!")
            self.result_label.setStyleSheet("color: green;")
        else:
            self.result_label.setText("К сожалению, вы проиграли")
            self.result_label.setStyleSheet("color: red;")

        self.correct_word_label.setText(f"Правильное слово: {self.current_word}")
        self.stack.setCurrentIndex(4)  # Переключаемся на экран результата


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = AnagramGame()
    game.show()
    sys.exit(app.exec_())
