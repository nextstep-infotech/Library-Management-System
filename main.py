import sys
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QMessageBox, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
import pandas as pd
import numpy as np

from library_management import Ui_MainWindow
from database import ConnectToMySQL

class MainWindow(QMainWindow):
    username = "nextstep815"
    password = None
    logged_in = True
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.icon_menu.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.dashboard_btn_2.setChecked(True)
        self.ui.user_btn.clicked.connect(self.on_login_button_clicked)
        self.ui.dashboard_btn_1.clicked.connect(self.on_dashboard_button_clicked)
        self.ui.dashboard_btn_2.clicked.connect(self.on_dashboard_button_clicked)
        self.ui.teachers_btn_1.clicked.connect(self.on_teachers_button_clicked)
        self.ui.teachers_btn_2.clicked.connect(self.on_teachers_button_clicked)
        self.ui.students_btn_1.clicked.connect(self.on_students_button_clicked)
        self.ui.students_btn_2.clicked.connect(self.on_students_button_clicked)
        self.ui.books_btn_1.clicked.connect(self.on_books_button_clicked)
        self.ui.books_btn_2.clicked.connect(self.on_books_button_clicked)
        self.ui.issues_btn_1.clicked.connect(self.on_issues_button_clicked)
        self.ui.issues_btn_2.clicked.connect(self.on_issues_button_clicked)
        self.ui.settings_btn_1.clicked.connect(self.on_settings_button_clicked)
        self.ui.settings_btn_2.clicked.connect(self.on_settings_button_clicked)
        self.ui.add_teacher_btn.clicked.connect(self.add_new_teacher)
        self.ui.login_btn.clicked.connect(self.login_method)

        #Plotting current data in dashboard
        self.figure = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax1 = self.figure.add_subplot(111)
        x = ['A', 'B', 'C', 'D', 'E']
        y = [10, 7, 4, 9, 3]
        self.ax1.bar(x, y)

        # Create a second set of axes and plot the line graph
        self.ax2 = self.ax1.twinx()
        y2 = [2, 5, 6, 4, 8]
        self.ax2.plot(x, y2, 'r')

        self.graph_layout = QVBoxLayout()
        self.graph_layout.addWidget(self.canvas)
        self.ui.graph_widget.setLayout(self.graph_layout)

    def on_login_button_clicked(self):
        self.ui.LMS_label.setText("Login")
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)

    def login_method(self):
        user = self.ui.username.text()
        protector = self.ui.password.text()
        if user.lower() != "nextstep815" and protector != "Next$tep815":
            QMessageBox.information(self, 'Username or password does not match.')
            return None
        else:
            self.logged_in = True
            self.ui.LMS_label.setText("Library Management System")
            self.ui.stackedWidget.setCurrentWidget(self.ui.dashboard_page)

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_menu.findChildren(QPushButton) \
                    + self.ui.full_name_menu.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    ## Functions to change menu pages
    def on_dashboard_button_clicked(self):
        self.ui.LMS_label.setText("Library Management System")
        self.ui.stackedWidget.setCurrentWidget(self.ui.dashboard_page)

    def on_teachers_button_clicked(self):
        if self.logged_in == True:
            self.ui.LMS_label.setText("Teachers")
            self.ui.stackedWidget.setCurrentWidget(self.ui.teachers_page)
            self.get_teachers_data()
        else:
            self.ui.LMS_label.setText("Login")
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
            QMessageBox.information(self, 'Warning', 'You are not logged in.')

    def on_students_button_clicked(self):
        self.ui.LMS_label.setText("Students")
        self.ui.stackedWidget.setCurrentWidget(self.ui.students_page)

    def on_books_button_clicked(self):
        self.ui.LMS_label.setText("Books")
        self.ui.stackedWidget.setCurrentWidget(self.ui.books_page)

    def on_issues_button_clicked(self):
        self.ui.LMS_label.setText("Isssues")
        self.ui.stackedWidget.setCurrentWidget(self.ui.issues_page)

    def on_settings_button_clicked(self):
        self.ui.LMS_label.setText("Settings")
        self.ui.stackedWidget.setCurrentWidget(self.ui.settings_page)

    # Dashboard Page
    

    # Teachers Page
    @pyqtSlot(bool)
    def get_teachers_data(self):
        result = ConnectToMySQL().get_teachers_data_from_db()
        if result:
            self.ui.teacher_table_widget.setRowCount(len(result))
            for row,item in enumerate(result):
                t_firstname = QTableWidgetItem(str(item['firstname']))
                t_lastname = QTableWidgetItem(str(item['lastname']))
                t_subject = QTableWidgetItem(str(item['subject']))
                t_contact = QTableWidgetItem(str(item['contact']))
                t_email = QTableWidgetItem(str(item['email']))
                t_address = QTableWidgetItem(str(item['address']))

                self.ui.teacher_table_widget.setItem(row, 0, t_firstname)
                self.ui.teacher_table_widget.setItem(row, 1, t_lastname)
                self.ui.teacher_table_widget.setItem(row, 2, t_subject)
                self.ui.teacher_table_widget.setItem(row, 3, t_contact)
                self.ui.teacher_table_widget.setItem(row, 4, t_email)
                self.ui.teacher_table_widget.setItem(row, 5, t_address)

        else:
            QMessageBox.information(self, 'Warning', 'Data could not be loaded. Please try again.')

    def add_new_teacher(self):
        t_first = self.ui.teacher_first_name.text()
        if t_first == "":
            QMessageBox.information(self, 'Warning', 'Your teacher does not have first name? That\'s amazing. :)')
            return None
        t_last = self.ui.teacher_last_name.text()
        if t_last == "":
            QMessageBox.information(self, 'Warning', 'Do I have to ask for last name also?')
            return None
        t_subject = self.ui.teacher_subject.text()
        if t_subject == "":
            QMessageBox.information(self, 'Warning', 'If he/she is teacher, what does he/she teaches?')
            return None
        t_contact = self.ui.teacher_contact.text()
        if t_contact == "":
            QMessageBox.information(self, 'Warning', 'Hello.. Can I have your number please.')
            return None
        t_email = self.ui.teacher_email.text()
        if t_email == "":
            QMessageBox.information(self, 'Warning', 'How do wasps send messages? By bee-mail.')
            return None
        t_address = self.ui.teacher_address.text()
        if t_address == "":
            QMessageBox.information(self, 'Warning', 'Does this teacher lives in space?')
            return None

        ConnectToMySQL().add_teacher_data_to_db(t_first,t_last,t_subject,t_contact,t_email,t_address)
        self.get_teachers_data()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ## Loading style file
    with open("style.qss", "r") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())