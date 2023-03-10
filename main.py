import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QMessageBox, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
from datetime import datetime

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
        self.ui.add_student_btn.clicked.connect(self.add_new_student)
        self.ui.add_book_btn.clicked.connect(self.add_new_book)
        self.ui.add_issue_btn.clicked.connect(self.add_new_issue)
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
        if self.logged_in == True:
            self.ui.LMS_label.setText("Students")
            self.ui.stackedWidget.setCurrentWidget(self.ui.students_page)
            self.get_students_data()
        else:
            self.ui.LMS_label.setText("Login")
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
            QMessageBox.information(self, 'Warning', 'You are not logged in.')

    def on_books_button_clicked(self):
        if self.logged_in == True:
            self.ui.LMS_label.setText("Books")
            self.ui.stackedWidget.setCurrentWidget(self.ui.books_page)
            self.get_books_data()
        else:
            self.ui.LMS_label.setText("Login")
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
            QMessageBox.information(self, 'Warning', 'You are not logged in.')

    def on_issues_button_clicked(self):
        if self.logged_in == True:
            self.ui.LMS_label.setText("Issues")
            self.ui.stackedWidget.setCurrentWidget(self.ui.issues_page)
            self.get_issues_data()
        else:
            self.ui.LMS_label.setText("Login")
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
            QMessageBox.information(self, 'Warning', 'You are not logged in.')

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
                t_joined_date = QTableWidgetItem(str(item['joineddate']))

                self.ui.teacher_table_widget.setItem(row, 0, t_firstname)
                self.ui.teacher_table_widget.setItem(row, 1, t_lastname)
                self.ui.teacher_table_widget.setItem(row, 2, t_subject)
                self.ui.teacher_table_widget.setItem(row, 3, t_contact)
                self.ui.teacher_table_widget.setItem(row, 4, t_email)
                self.ui.teacher_table_widget.setItem(row, 5, t_address)
                self.ui.teacher_table_widget.setItem(row, 6, t_joined_date)

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
        t_joined_date = str(datetime.today().year)

        ConnectToMySQL().add_teacher_data_to_db(t_first, t_last, t_subject, t_contact, t_email, t_address, t_joined_date)
        self.get_teachers_data()


    # Students Page
    @pyqtSlot(bool)
    def get_students_data(self):
        result = ConnectToMySQL().get_students_data_from_db()
        if result:
            self.ui.student_table_widget.setRowCount(len(result))
            for row,item in enumerate(result):
                s_firstname = QTableWidgetItem(str(item['firstname']))
                s_lastname = QTableWidgetItem(str(item['lastname']))
                s_batch = QTableWidgetItem(str(item['batch']))
                s_faculty = QTableWidgetItem(str(item['faculty']))
                s_year = QTableWidgetItem(str(item['year']))
                s_semester = QTableWidgetItem(str(item['semester']))
                s_rollno = QTableWidgetItem(str(item['rollno']))
                s_contact = QTableWidgetItem(str(item['contact']))
                s_address = QTableWidgetItem(str(item['address']))

                self.ui.student_table_widget.setItem(row, 0, s_firstname)
                self.ui.student_table_widget.setItem(row, 1, s_lastname)
                self.ui.student_table_widget.setItem(row, 2, s_batch)
                self.ui.student_table_widget.setItem(row, 3, s_faculty)
                self.ui.student_table_widget.setItem(row, 4, s_year)
                self.ui.student_table_widget.setItem(row, 5, s_semester)
                self.ui.student_table_widget.setItem(row, 6, s_rollno)
                self.ui.student_table_widget.setItem(row, 7, s_contact)
                self.ui.student_table_widget.setItem(row, 8, s_address)

        else:
            QMessageBox.information(self, 'Warning', 'Data could not be loaded. Please try again.')

    def add_new_student(self):
        s_first = self.ui.student_first_name.text()
        if s_first == "":
            QMessageBox.information(self, 'Warning', 'Firstname cannot be empty.')
            return None
        s_last = self.ui.student_last_name.text()
        if s_last == "":
            QMessageBox.information(self, 'Warning', 'Lastname cannot be empty.')
            return None
        s_batch = self.ui.student_batch.text()
        if s_batch == "":
            QMessageBox.information(self, 'Warning', 'Batch cannot be empty.')
            return None
        s_faculty = self.ui.student_faculty.text()
        if s_faculty == "":
            QMessageBox.information(self, 'Warning', 'Faculty cannot be empty.')
            return None
        s_year = self.ui.student_year.text()
        if s_year == "":
            QMessageBox.information(self, 'Warning', 'Year cannot be empty.')
            return None
        s_semester = self.ui.student_semester.text()
        if s_semester == "":
            QMessageBox.information(self, 'Warning', 'Semester cannot be empty.')
            return None
        s_rollno = self.ui.student_roll_no.text()
        if s_rollno == "":
            QMessageBox.information(self, 'Warning', 'Roll No cannot be empty.')
            return None
        s_contact = self.ui.student_contact.text()
        if s_contact == "":
            QMessageBox.information(self, 'Warning', 'Contact cannot be empty.')
            return None        
        s_address = self.ui.student_address.text()
        if s_address == "":
            QMessageBox.information(self, 'Warning', 'Address cannot be empty.')
            return None

        ConnectToMySQL().add_student_data_to_db(s_first, s_last, s_batch, s_faculty, s_year, s_semester, s_rollno, s_contact, s_address)
        self.get_students_data()

    # Books Page
    @pyqtSlot(bool)
    def get_books_data(self):
        result = ConnectToMySQL().get_books_data_from_db()
        if result:
            self.ui.book_table_widget.setRowCount(len(result))
            for row,item in enumerate(result):
                b_isbn = QTableWidgetItem(str(item['isbn']))
                b_title = QTableWidgetItem(str(item['title']))
                b_author = QTableWidgetItem(str(item['author']))
                b_publisher = QTableWidgetItem(str(item['publisher']))
                b_category = QTableWidgetItem(str(item['category']))
                b_quantity = QTableWidgetItem(str(item['quantity']))

                self.ui.book_table_widget.setItem(row, 0, b_isbn)
                self.ui.book_table_widget.setItem(row, 1, b_title)
                self.ui.book_table_widget.setItem(row, 2, b_author)
                self.ui.book_table_widget.setItem(row, 3, b_publisher)
                self.ui.book_table_widget.setItem(row, 4, b_category)
                self.ui.book_table_widget.setItem(row, 5, b_quantity)


        else:
            QMessageBox.information(self, 'Warning', 'Data could not be loaded. Please try again.')

    def add_new_book(self):
        b_isbn = self.ui.book_isbn.text()
        if b_isbn == "":
            QMessageBox.information(self, 'Warning', 'ISBN cannot be empty.')
            return None
        b_title = self.ui.book_title.text()
        if b_title == "":
            QMessageBox.information(self, 'Warning', 'Title cannot be empty.')
            return None
        b_author = self.ui.book_author.text()
        if b_author == "":
            QMessageBox.information(self, 'Warning', 'Author cannot be empty.')
            return None
        b_publisher = self.ui.book_publisher.text()
        if b_publisher == "":
            QMessageBox.information(self, 'Warning', 'Publisher cannot be empty.')
            return None
        b_category = self.ui.book_category.text()
        if b_category == "":
            QMessageBox.information(self, 'Warning', 'Category cannot be empty.')
            return None
        b_quantity = self.ui.book_quantity.text()
        if b_quantity == "":
            QMessageBox.information(self, 'Warning', 'Quantity cannot be empty.')
            return None

        ConnectToMySQL().add_book_data_to_db(b_isbn, b_title, b_author, b_publisher, b_category, b_quantity)
        self.get_books_data()

    # Issues Page
    @pyqtSlot(bool)
    def get_issues_data(self):
        result = ConnectToMySQL().get_issues_data_from_db()
        if result:
            self.ui.issue_table_widget.setRowCount(len(result))
            for row,item in enumerate(result):
                i_book_no = QTableWidgetItem(str(item['book_no']))
                i_student_id = QTableWidgetItem(str(item['student_id']))
                i_issue_date = QTableWidgetItem(str(item['issue_date']))
                i_due_date = QTableWidgetItem(str(item['due_date']))
                i_return_date = QTableWidgetItem(str(item['return_date']))
                i_fine = QTableWidgetItem(str(item['fine']))

                self.ui.issue_table_widget.setItem(row, 0, i_book_no)
                self.ui.issue_table_widget.setItem(row, 1, i_student_id)
                self.ui.issue_table_widget.setItem(row, 2, i_issue_date)
                self.ui.issue_table_widget.setItem(row, 3, i_due_date)
                self.ui.issue_table_widget.setItem(row, 4, i_return_date)
                self.ui.issue_table_widget.setItem(row, 5, i_fine)

        else:
            QMessageBox.information(self, 'Warning', 'Data could not be loaded. Please try again.')

    def add_new_issue(self):
        i_book_no = self.ui.issue_book_no.text()
        if i_book_no == "":
            QMessageBox.information(self, 'Warning', 'Book No cannot be empty.')
            return None
        i_student_id = self.ui.issue_student_id.text()
        if i_student_id == "":
            QMessageBox.information(self, 'Warning', 'Student ID cannot be empty.')
            return None
        i_issue_date = self.ui.issue_date.text()
        if i_issue_date == "":
            QMessageBox.information(self, 'Warning', 'Issue date cannot be empty.')
            return None
        i_due_date = self.ui.issue_due_date.text()
        if i_due_date == "":
            QMessageBox.information(self, 'Warning', 'Due date cannot be empty.')
            return None
        i_return_date = self.ui.issue_return_date.text()
        if i_return_date == "":
            QMessageBox.information(self, 'Warning', 'Return date cannot be empty.')
            return None
        i_fine = self.ui.issue_address.text()

        ConnectToMySQL().add_teacher_data_to_db(i_book_no, i_student_id, i_issue_date, i_due_date, i_return_date, i_fine)
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