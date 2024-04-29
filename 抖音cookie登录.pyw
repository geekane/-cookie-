from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("抖音登录")

        # 布局
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        layout = QVBoxLayout()
        self.main_widget.setLayout(layout)

        # Cookie输入框
        self.cookie_edit = QLineEdit()
        self.cookie_edit.setPlaceholderText("请输入抖音Cookie字符串")
        layout.addWidget(self.cookie_edit)

        # 登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.on_login_clicked)
        layout.addWidget(self.login_button)

        # 信息标签
        self.info_label = QLabel()
        layout.addWidget(self.info_label)

    def on_login_clicked(self):
        # 获取Cookie字符串
        cookie_string = self.cookie_edit.text()

        # 创建WebDriver服务
        s = Service(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe')
        options = webdriver.EdgeOptions()
        options.add_argument("start-maximized")# 可选，最大化窗口

        # 启动Edge浏览器
        driver = webdriver.Edge(service=s, options=options)

        # 访问抖音网页
        driver.get('https://www.douyin.com')

        # 解析Cookie字符串并设置Cookie
        self.parse_and_set_cookies(driver, cookie_string)

        # 再次访问网页以应用Cookie
        driver.get('https://www.douyin.com')

        # 等待页面加载完成
        wait = WebDriverWait(driver, 10)
        # 请替换下面的 "some_unique_element_id" 为页面上一个确实存在的元素ID
        wait.until(EC.presence_of_element_located((By.ID, "login-pannel")))

        # 显示登录状态
        if driver.find_element(By.ID, "login-pannel").is_displayed():
            self.info_label.setText("登录失败")
        else:
            self.info_label.setText("登录成功")

        # 关闭浏览器
        driver.quit()

    def parse_and_set_cookies(self, driver, cookie_string):
        # 移除开头和结尾的空白字符，确保处理准确性
        cookie_string = cookie_string.strip()

        # 按照分号分割成Cookie项列表
        cookie_items = cookie_string.split(';')

        # 创建一个空字典用于存储键值对
        cookies_dict = {}

        # 解析Cookie字符串并填充到字典
        for item in cookie_items:
            if '=' in item:
                name, value = item.split('=', 1)
                cookies_dict[name.strip()] = value.strip()

        # 设置Cookie
        for name, value in cookies_dict.items():
            driver.add_cookie({'name': name, 'value': value})


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
