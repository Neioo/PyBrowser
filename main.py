import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super(BrowserTab, self).__init__(parent)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)


    def back(self):
        self.browser.back()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowIcon(QIcon('Logo.png'))


        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_navbar)

        self.setCentralWidget(self.tabs)

        self.create_tab()

        # navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Back button
        back_btn = QAction(QIcon('back-arrow.png'), 'Back', self)
        back_btn.triggered.connect(self.current_browser().back)
        navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction(QIcon('front-arrow.png'),'Forward', self)
        forward_btn.triggered.connect(self.current_browser().forward)
        navbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction(QIcon('reload.png'),'Reload', self)
        reload_btn.triggered.connect(self.current_browser().reload)
        navbar.addAction(reload_btn)

        # Home button
        home_btn = QAction(QIcon('home.png'),'Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # New Tab button
        new_tab_btn = QAction(QIcon('new-tab.png'),'New Tab', self)
        new_tab_btn.triggered.connect(self.create_tab)
        navbar.addAction(new_tab_btn)

        # search bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # navbar aesthetic
        navbar.setStyleSheet("QToolBar {background-color: #333; }")
        navbar.setIconSize(QSize(30, 30))
        self.url_bar.setStyleSheet("QLineEdit { border-radius: 5px; padding: 2px; margin-right:5px; background: #FFF; }")
        self.showMaximized()
        self.setStyleSheet("QMainWindow {background-color: #333;}")

    def update_navbar(self, index):
        current_browser = self.current_browser()
        current_browser.urlChanged.connect(self.update_url)

    def navigate_home(self):
        self.current_browser().setUrl(QUrl('http://google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def create_tab(self):
        browser_tab = BrowserTab(self)
        self.tabs.addTab(browser_tab, "New Tab")
        self.tabs.setCurrentWidget(browser_tab)

    def current_browser(self):
        return self.tabs.currentWidget().browser

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

app = QApplication(sys.argv)
QApplication.setApplicationName('Iris')
window = MainWindow()
window.show()
sys.exit(app.exec_())
