import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,QPlainTextEdit

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat

from sudachipy import tokenizer, dictionary


def check_kanji_and_length(text):

    tokenizer_obj = dictionary.Dictionary().create()

    mode = tokenizer.Tokenizer.SplitMode.C

    tokens = tokenizer_obj.tokenize(text, mode)

 

    problematic_tokens = ["頂き", "下さい", "所謂", "概ね"]

    errors = []

 

    for token in tokens:

        if token.surface() in problematic_tokens:

            errors.append(f"開いたほうが良い漢字があります: {token.surface()}")

 

    sentences = text.split('。')

    for i, sentence in enumerate(sentences):

        if len(sentence) > 40:

            errors.append(f"行: {i + 1} - 1文が40文字を超えています。")

 

    return errors

 

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.initUI()

 

    def initUI(self):

        self.setWindowTitle('Text Editor with SudachiPy')

        self.setGeometry(100, 100, 800, 600)

 

        self.textEditA = QTextEdit()

        self.textEditB = QTextEdit()

        button = QPushButton('Check Kanji')

        button.clicked.connect(self.check_kanji)

 

        layoutA = QVBoxLayout()

        layoutA.addWidget(self.textEditA)

        layoutB = QVBoxLayout()

        layoutB.addWidget(self.textEditB)

        buttonLayout = QHBoxLayout()

        buttonLayout.addWidget(button)

 

        mainLayout = QVBoxLayout()

        mainLayout.addLayout(layoutA)

        mainLayout.addLayout(buttonLayout)

        mainLayout.addLayout(layoutB)

 

        container = QWidget()

        container.setLayout(mainLayout)

        self.setCentralWidget(container)

 

    def check_kanji(self):

        text = self.textEditA.toPlainText()

        errors = check_kanji_and_length(text)

        for error in errors:

            self.textEditB.append(error)

 

if __name__ == '__main__':

    app = QApplication(sys.argv)

    mainWin = MainWindow()

    mainWin.show()

    sys.exit(app.exec_())