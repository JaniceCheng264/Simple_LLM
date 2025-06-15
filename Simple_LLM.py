import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QListWidget, QTextEdit,
    QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
#載入LLM.py
from LLM import LLMClient
            
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主視窗")
        self.llm = None

        self.create()

    def create(self):
        #左邊
        self.nav_frame = QWidget()
        nav_layout = QVBoxLayout()
        self.nav_frame.setLayout(nav_layout)

        #API key
        nav_layout.addWidget(QLabel("API Key："))
        self.api_input = QLineEdit()
        nav_layout.addWidget(self.api_input)

        #System Prompt
        nav_layout.addWidget(QLabel("System Prompt："))
        self.system_text = QTextEdit()
        self.system_text.setPlainText("你是一名風趣幽默的助理,使用中文回覆.")
        nav_layout.addWidget(self.system_text)

        #System送出按鈕
        self.system_btn = QPushButton("更新System Prompt與API key")
        self.system_btn.clicked.connect(self.submit)
        nav_layout.addWidget(self.system_btn)


        #右邊
        self.edit_frame= QWidget()
        edit_layout = QVBoxLayout()
        self.edit_frame.setLayout(edit_layout)

        #user input
        edit_layout.addWidget(QLabel("使用者輸入："))
        #self.user_label = QLabel("使用者輸入：")
        self.comment_input = QTextEdit()
        edit_layout.addWidget(self.comment_input)

        #按鈕送出使用者輸入
        self.submit_btn = QPushButton("送出")
        self.submit_btn.clicked.connect(self.user_submit)
        edit_layout.addWidget(self.submit_btn)
        
        edit_layout.addWidget(QLabel("聊天紀錄："))
        #self.chat_label = QLabel("聊天紀錄：")
        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)
        edit_layout.addWidget(self.chat_output)

        #排版
        main_layout= QHBoxLayout()
        main_layout.addWidget(self.nav_frame, 2)
        main_layout.addWidget(self.edit_frame, 3)
        self.setLayout(main_layout)


    def submit(self):
        #初始時沒有API key -> 觸發此並送出API key
        #缺點:無法重設API key, 可以透過製造重設按鈕/建立送出API key的按鈕
        key = self.api_input.text().strip()
        if not key:
                self.chat_output.append("System: 請輸入 API 金鑰。")
                return
            
        system_input = self.system_text.toPlainText().strip()
        if not system_input:
            self.chat_output.append("System: 請輸入System Prompt")
            return
        
        self.llm = LLMClient(api_key=key,prompt=system_input)
        self.chat_output.append("System: System prompt與API key已更新")
        
    def user_submit(self):
        user_text = self.comment_input.toPlainText().strip()
        if not user_text:
            self.chat_output.append("System: 請輸入訊息")
            return
        
        self.chat_output.append(f"User: {user_text}")
        self.comment_input.clear() #清空user的輸入

        try:
            reply=self.llm.send(user_text)
            self.chat_output.append(f"AI回覆: {reply}")
        except Exception as e:
            self.chat_output.append(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# if __name__ == "__main__" 是標準啟動方式（代表直接執行）
# root = tk.Tk()：創建 GUI 視窗
# root.mainloop()：進入 GUI 主迴圈，讓畫面持續運作
    