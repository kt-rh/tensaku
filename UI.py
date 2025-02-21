import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QPlainTextEdit
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QColor, QTextFormat, QTextCursor, QPainter

import typo1
import typo2
import re

# 行番号エリアクラス
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

# 行番号付きテキストエディタクラス
class LineNumberTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)
        self.highlightCurrentLine()

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.document().blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        self.lineNumberArea.update(0, 0, self.lineNumberArea.width(), event.size().height())

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = self.palette().alternateBase()
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.document().findBlockByLineNumber(0)
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(QRect(0, int(top), self.lineNumberArea.width(), self.fontMetrics().height()), Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

# メインウィンドウクラス
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    # UIの初期化
    def initUI(self):
        self.setWindowTitle('Text Editor with Line Numbers')
        self.setGeometry(100, 100, 800, 600)

        # テキスト編集ウィジェットの設定
        self.textEditA = LineNumberTextEdit()
        self.textEditB = QTextEdit()
        button = QPushButton('Check Errors')
        button.clicked.connect(self.check_errors)

        # レイアウトの設定
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


    # エラーをチェックする関数
    def check_errors(self):
        text = self.textEditA.toPlainText()
        completed_text, all_errors = typo1.detect_and_correct_errors(text)
        


        list_text = list(text)
        list_tmp = []

        for item in list_text:

            list_tmp.append(item)

            if re.search("。", item):
                list_tmp.append("\n")


        str_edited = "".join(list_tmp)
        self.textEditA.setPlainText(str_edited)
        print(text)
        print(list_tmp) 

        
        cursor = self.textEditA.textCursor()
        for error in all_errors:
            cursor.setPosition(error['position'])
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
            char_format = cursor.charFormat()
            char_format.setForeground(QColor(Qt.red))
            cursor.setCharFormat(char_format)

            # エラーメッセージの設定
            error_message = {
                "kanji-conversion_a": "誤字があります。",
                "kanji-conversion_b": "誤字があります。",
                "substitution": "誤字があります。",
                "transposition": "誤字があります。",
                "others": "誤字があります。",    
                "deketion": "脱字があります。",
                "insertion_a": "衍字があります。",
                "insertion_b": "衍字があります。",
            }
            error_message_text = error_message.get(error['error_type'],"誤字があります。")
            block_number = cursor.blockNumber() + 1
            error_text = f"行: {block_number} エラー: {error_message_text}"
            self.textEditB.append(error_text)

        # typo2のエラーをチェック
        typo2_errors = typo2.check_kanji_and_length(text)
        for error in typo2_errors:
            self.textEditB.append(error)

# メイン関数
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())







