import sys
import json
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QStackedWidget)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor


class AnagramGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анаграммы")
        self.setFixedSize(800, 600)

        # Установка цветовой схемы
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

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
            default_words = {
"легкий": [
    "кот", "дом", "лес", "нос", "рот", "сад", "год", "сон", "мир", "бар",
    "век", "дар", "жук", "зло", "ива", "лук", "мех", "пир", "рис", "суп",
    "тир", "хор", "чай", "бег", "вол", "газ", "дуб", "ель", "жар", "зов",
    "кит", "лёд", "мак", "неб", "ода", "пёс", "рак", "сок", "уха",
    "фен", "цех", "шар", "щит", "юла", "яма", "ярд"
  ],    "средний": [
    "банк", "вино", "гора", "диск", "елка", "зима", "игла", "кожа", "луна", "муха",
    "арка", "бокс", "ваза", "вода", "енот", "жара", "зона", "ирис", "йога",
    "каша", "лиса", "нора", "овёс", "пена", "роза", "сова", "туча", "ужин",
    "флаг", "хлеб", "цирк", "чудо", "шарф", "щука", "юбка", "ящик", "аист",
    "блин", "вода", "жара", "иней", "клён", "лото"
  ],
    "сложный": [
    "банан", "ветер", "гроза", "жираф", "книга", "пират", "силач", "абзац", "вагон",
     "жетон", "забор", "инжир", "камин", "лапша", "манго",
    "нитка", "олень", "парик", "редис", "салют", "тайна", "угода", "финик", "хобби",
    "череп", "шалаш", "этнос", "якорь", "азарт", "балет", "ветка", "гараж",
      "искра", "каска", "лазер", "магия", "опера"
  ]
}
            with open('words.json', 'w', encoding='utf-8') as file:
                json.dump(default_words, file, ensure_ascii=False, indent=4)
            return default_words

    def create_main_menu(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        # Заголовок (поле 1 из ТЗ)
        title = QLabel("Анаграммы")
        title.setFont(QFont('Arial', 48, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title, stretch=2)

        # Кнопка "Играть" (поле 2 из ТЗ)
        btn_play = self.create_button("Играть", 200, 60, "background-color: #3498db; color: white;")
        btn_play.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(btn_play, alignment=Qt.AlignCenter)

        # Кнопка "Руководство" (поле 3 из ТЗ)
        btn_help = self.create_button("Руководство", 200, 60, "background-color: #2ecc71; color: white;")
        btn_help.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        layout.addWidget(btn_help, alignment=Qt.AlignCenter)

        # Кнопка "Выход" (поле 4 из ТЗ)
        btn_exit = self.create_button("Выход", 200, 60, "background-color: #e74c3c; color: white;")
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit, alignment=Qt.AlignCenter)

        layout.addStretch(1)
        widget.setLayout(layout)
        self.stack.addWidget(widget)

    def create_level_menu(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Заголовок (поле 1 из ТЗ)
        title = QLabel("Выбор сложности")
        title.setFont(QFont('Arial', 36, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)

        # Кнопки уровней (поля 2,3,4 из ТЗ)
        btn_easy = self.create_button("Легкий", 250, 60, "background-color: #1abc9c; color: white;")
        btn_easy.clicked.connect(lambda: self.start_level("легкий"))
        layout.addWidget(btn_easy, alignment=Qt.AlignCenter)

        btn_medium = self.create_button("Средний", 250, 60, "background-color: #f39c12; color: white;")
        btn_medium.clicked.connect(lambda: self.start_level("средний"))
        layout.addWidget(btn_medium, alignment=Qt.AlignCenter)

        btn_hard = self.create_button("Сложный", 250, 60, "background-color: #e74c3c; color: white;")
        btn_hard.clicked.connect(lambda: self.start_level("сложный"))
        layout.addWidget(btn_hard, alignment=Qt.AlignCenter)

        # Кнопка "Назад" (поле 5 из ТЗ)
        btn_back = self.create_button("Назад", 150, 50, "background-color: #95a5a6; color: white;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back, alignment=Qt.AlignCenter)

        layout.addStretch(1)
        widget.setLayout(layout)
        self.stack.addWidget(widget)

    def create_help_screen(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        # Заголовок
        title = QLabel("Правила игры")
        title.setFont(QFont('Arial', 36, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)

        # Текст правил
        rules = QLabel(
            "Цель игры - составить исходное слово из перемешанных букв.\n\n"
            "1. Выберите уровень сложности (легкий, средний, сложный).\n"
            "2. Вам будет показано слово с перемешанными буквами.\n"
            "3. Нажимайте на буквы в правильном порядке, чтобы составить слово.\n"
            "4. Если ошиблись-нажмите кнопку 'Отмена' для отмены последней буквы.\n"
            "5. Если хотите начать заново - вернитесь в меню выбора уровня.\n\n"
            "Удачи в игре!"
        )
        rules.setFont(QFont('Arial', 15))
        rules.setAlignment(Qt.AlignLeft)
        rules.setStyleSheet("background-color: white; padding: 20px; border-radius: 10px;")
        layout.addWidget(rules)

        # Кнопка назад
        btn_back = self.create_button("Назад", 150, 50, "background-color: #95a5a6; color: white;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back, alignment=Qt.AlignCenter)

        widget.setLayout(layout)
        self.stack.addWidget(widget)

    def create_game_screen(self):
        self.game_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Верхняя панель только с указанием уровня (без кнопки назад)
        top_layout = QHBoxLayout()

        self.level_label = QLabel()
        self.level_label.setFont(QFont('Arial', 16))
        top_layout.addWidget(self.level_label)
        top_layout.addStretch()  # Добавляем растягивающийся элемент для выравнивания

        main_layout.addLayout(top_layout)

        # Поле для ввода слова (поле 1 из ТЗ)
        self.word_display = QLabel()
        self.word_display.setFont(QFont('Arial', 36, QFont.Bold))
        self.word_display.setAlignment(Qt.AlignCenter)
        self.word_display.setStyleSheet("""
            background-color: white;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            padding: 15px;
            min-height: 80px;
        """)
        main_layout.addWidget(self.word_display)

        # Контейнер для виртуальной клавиатуры и кнопки отмены
        keyboard_container = QWidget()
        keyboard_layout = QVBoxLayout()
        keyboard_container.setLayout(keyboard_layout)

        # Виртуальная клавиатура (поле 2 из ТЗ)
        self.keyboard_widget = QWidget()
        self.keyboard_layout = QHBoxLayout()
        self.keyboard_layout.setSpacing(10)
        self.keyboard_widget.setLayout(self.keyboard_layout)
        keyboard_layout.addWidget(self.keyboard_widget, 0, Qt.AlignCenter)

        # Кнопка отмены (кнопка 3 из ТЗ)
        btn_undo = self.create_button("Отмена", 120, 50, "background-color: #e74c3c; color: white;")
        btn_undo.clicked.connect(self.undo_last_letter)
        keyboard_layout.addWidget(btn_undo, 0, Qt.AlignCenter)

        main_layout.addWidget(keyboard_container)

        # Единственная кнопка возврата к выбору уровня (кнопка 4 из ТЗ)
        btn_back_level = self.create_button("Назад к выбору уровня", 200, 50,
                                            "background-color: #95a5a6; color: white;")
        btn_back_level.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        main_layout.addWidget(btn_back_level, 0, Qt.AlignCenter)

        self.game_widget.setLayout(main_layout)
        self.stack.addWidget(self.game_widget)

    def create_result_screen(self):
        self.result_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        # Надпись о результате (поле 1 из ТЗ)
        self.result_label = QLabel()
        self.result_label.setFont(QFont('Arial', 36, QFont.Bold))
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        self.correct_word_label = QLabel()
        self.correct_word_label.setFont(QFont('Arial', 24))
        self.correct_word_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.correct_word_label)

        # Кнопка возврата (поле 2 из ТЗ)
        btn_menu = self.create_button("В меню", 200, 60, "background-color: #3498db; color: white;")
        btn_menu.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_menu, alignment=Qt.AlignCenter)

        layout.addStretch(1)
        self.result_widget.setLayout(layout)
        self.stack.addWidget(self.result_widget)

    def create_button(self, text, width, height, style=""):
        btn = QPushButton(text)
        btn.setFixedSize(width, height)
        btn.setFont(QFont('Arial', 14))
        btn.setStyleSheet(f"""
            QPushButton {{
                {style}
                border-radius: 5px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """)
        return btn

    def start_level(self, level):
        self.current_level = level
        self.current_word = random.choice(self.words[level])
        self.scrambled_word = self.scramble_word(self.current_word)
        self.user_input = []

        # Очищаем клавиатуру
        for i in reversed(range(self.keyboard_layout.count())):
            self.keyboard_layout.itemAt(i).widget().setParent(None)

        # Создаем кнопки с буквами (3-5 кнопок в зависимости от уровня)
        for letter in self.scrambled_word:
            btn = QPushButton(letter.upper())
            btn.setFont(QFont('Arial', 24, QFont.Bold))
            btn.setFixedSize(60, 60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: 2px solid #2980b9;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:disabled {
                    background-color: #bdc3c7;
                    border-color: #95a5a6;
                }
            """)
            btn.clicked.connect(self.letter_clicked)
            self.keyboard_layout.addWidget(btn)

        self.level_label.setText(f"Уровень: {level.capitalize()}")
        self.word_display.setText("")
        self.stack.setCurrentIndex(3)

    def scramble_word(self, word):
        letters = list(word)
        random.shuffle(letters)
        return ''.join(letters)

    def letter_clicked(self):
        sender = self.sender()
        letter = sender.text().lower()

        if self.scrambled_word.lower().count(letter) > self.user_input.count(letter):
            self.user_input.append(letter)
            self.word_display.setText(''.join(self.user_input).upper())

            # Проверяем победу
            if ''.join(self.user_input) == self.current_word:
                self.show_result(True)  

    def undo_last_letter(self):
        if self.user_input:
            self.user_input.pop()
            self.word_display.setText(''.join(self.user_input).upper())

    def show_result(self, win):
        if win:
            self.result_label.setText("Уровень завершен! Победа!")
            self.result_label.setStyleSheet("color: #27ae60;")
        else:
            self.result_label.setText("К сожалению, вы проиграли")
            self.result_label.setStyleSheet("color: #e74c3c;")

        self.correct_word_label.setText(f"Правильное слово: {self.current_word.upper()}")
        self.stack.setCurrentIndex(4)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Установка стиля для всего приложения
    app.setStyleSheet("""
        QWidget {
            font-family: Arial;
        }
    """)

    game = AnagramGame()
    game.show()
    sys.exit(app.exec_())