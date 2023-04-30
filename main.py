import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QMessageBox, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from datetime import datetime
import re
from library_management import Ui_MainWindow
from database import ConnectToMySQL

class MainWindow(QMainWindow):
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
        #Adding
        self.ui.add_teacher_btn.clicked.connect(self.add_new_teacher)
        self.ui.add_student_btn.clicked.connect(self.add_new_student)
        self.ui.add_book_btn.clicked.connect(self.add_new_book)
        self.ui.add_issue_btn.clicked.connect(self.add_new_issue)
        #Editing
        self.ui.edit_teacher_btn.clicked.connect(self.edit_selected_teacher)
        self.ui.edit_student_btn.clicked.connect(self.edit_selected_student)
        self.ui.edit_book_btn.clicked.connect(self.edit_selected_book)
        self.ui.edit_issue_btn.clicked.connect(self.edit_selected_issue)
        #Deleting
        self.ui.delete_teacher_btn.clicked.connect(self.delete_selected_teacher)
        self.ui.delete_student_btn.clicked.connect(self.delete_selected_student)
        self.ui.delete_book_btn.clicked.connect(self.delete_selected_book)
        self.ui.delete_issue_btn.clicked.connect(self.delete_selected_issue)


        self.ui.login_btn.clicked.connect(self.login_method)
        self.ui.show_hide_current_password.clicked.connect(self.show_hide_current_password_method)
        self.ui.show_hide_new_password.clicked.connect(self.show_hide_new_password_method)
        self.ui.show_hide_confirm_password.clicked.connect(self.show_hide_confirm_password_method)
        self.ui.reset_password_btn.clicked.connect(self.reset_password_method)
        self.ui.show_login_password_btn.clicked.connect(self.show_login_password_method)

        #Get data to top
        self.ui.teacher_table_widget.clicked.connect(self.get_teacher_data_to_top)
        self.ui.student_table_widget.clicked.connect(self.get_student_data_to_top)
        self.ui.book_table_widget.clicked.connect(self.get_book_data_to_top)
        self.ui.issue_table_widget.clicked.connect(self.get_issue_data_to_top)

        #Clear data on top
        self.ui.clear_teacher_selection_btn.clicked.connect(self.clear_teacher_data_on_top)
        self.ui.clear_student_selection_btn.clicked.connect(self.clear_student_data_on_top)
        self.ui.clear_book_selection_btn.clicked.connect(self.clear_book_data_on_top)
        self.ui.clear_issue_selection_btn.clicked.connect(self.clear_issue_data_on_top)

        self.show_current_password = False
        self.show_new_password = False
        self.show_confirm_password = False
        self.show_login_password = False

        self.update_cards_and_graph()
        self.get_admin_details()

    def on_login_button_clicked(self):
        if self.status == '0':
            self.ui.LMS_label.setText("Login")
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
        else:
            #log out page
            self.reply = QMessageBox.question(self, 'Log Out', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if self.reply == QMessageBox.Yes:
                ConnectToMySQL().logout()
                self.status = '0'
                self.ui.username.setText('')
                self.ui.password.setText('')
                self.on_dashboard_button_clicked()

    def login_method(self):
        user = self.ui.username.text()
        protector = self.ui.password.text()
        if user.lower() != self.username:
            QMessageBox.information(self, 'Username does not match.')
            return None
        if protector != self.password:
            QMessageBox.information(self, 'Password does not match.')
            return None
        else:
            self.status = '1'
            ConnectToMySQL().update_login_status()
            self.ui.LMS_label.setText("Library Management System")
            self.ui.stackedWidget.setCurrentWidget(self.ui.dashboard_page)
            self.ui.username.setText('')
            self.ui.password.setText('')

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
        self.update_cards_and_graph()

    def on_teachers_button_clicked(self):
        if self.status == '1':
            self.ui.LMS_label.setText("Teachers")
            self.ui.stackedWidget.setCurrentWidget(self.ui.teachers_page)

            # Resize Teacher Table
            # Divide the total width equally to all columns
            teacher_total_width = self.ui.teacher_table_widget.width()        
            teacher_column_width = int(teacher_total_width / self.ui.teacher_table_widget.columnCount())
            # Set the column width of each column
            for i in range(self.ui.teacher_table_widget.columnCount()):
                self.ui.teacher_table_widget.setColumnWidth(i, teacher_column_width)
            
            #Clear all teacher line edits
            self.clear_teacher_data_on_top()

            self.get_teachers_data()
        else:
            self.ui.LMS_label.setText("Login")
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
            QMessageBox.information(self, 'Warning', 'You are not logged in.')

    def on_students_button_clicked(self):
        if self.status == '1':
            self.ui.LMS_label.setText("Students")
            self.ui.stackedWidget.setCurrentWidget(self.ui.students_page)
            # Resize Student Table
            # Divide the total width equally to all columns
            student_total_width = self.ui.student_table_widget.width()
            student_column_width = int(student_total_width / self.ui.student_table_widget.columnCount())
            # Set the column width of each column
            for i in range(self.ui.student_table_widget.columnCount()):
                self.ui.student_table_widget.setColumnWidth(i, student_column_width)

            #Clear all student line edits
            self.clear_student_data_on_top()

            self.get_students_data()
        else:
            self.ui.LMS_label.setText("Login")
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
            QMessageBox.information(self, 'Warning', 'You are not logged in.')

    def on_books_button_clicked(self):
        if self.status == '1':
            self.ui.LMS_label.setText("Books")
            self.ui.stackedWidget.setCurrentWidget(self.ui.books_page)
            # Resize Book Table
            # Divide the total width equally to all columns
            book_total_width = self.ui.book_table_widget.width()
            book_column_width = int(book_total_width / self.ui.book_table_widget.columnCount())
            # Set the column width of each column
            for i in range(self.ui.book_table_widget.columnCount()):
                self.ui.book_table_widget.setColumnWidth(i, book_column_width)

            #Clear all book line edits
            self.clear_book_data_on_top()

            self.get_books_data()
        else:
            self.ui.LMS_label.setText("Login")
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
            QMessageBox.information(self, 'Warning', 'You are not logged in.')

    def on_issues_button_clicked(self):
        if self.status == '1':
            self.ui.LMS_label.setText("Issues")
            self.ui.stackedWidget.setCurrentWidget(self.ui.issues_page)
            # Resize Issue Table
            # Divide the total width equally to all columns
            issue_total_width = self.ui.issue_table_widget.width()
            issue_column_width = int(issue_total_width / self.ui.issue_table_widget.columnCount())
            # Set the column width of each column
            for i in range(self.ui.issue_table_widget.columnCount()):
                self.ui.issue_table_widget.setColumnWidth(i, issue_column_width)

            #Clear all issue line edits
            self.clear_issue_data_on_top()

            self.get_issues_data()
        else:
            self.ui.LMS_label.setText("Login")
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
            QMessageBox.information(self, 'Warning', 'You are not logged in.')

    def on_settings_button_clicked(self):
        self.ui.LMS_label.setText("Settings")
        self.ui.stackedWidget.setCurrentWidget(self.ui.settings_page)


    # Get admin username and password
    def get_admin_details(self):
        result = ConnectToMySQL().get_data_for_login()
        self.username = result[0]
        self.password = result[1]
        self.status = result[2]

    # Dashboard Page
    def update_cards_and_graph(self):
        #Dashboard Card
        result = ConnectToMySQL().get_all_data_counts_from_db()
        self.ui.teachers_count_label.setText(str(result[0]))
        self.ui.students_count_label.setText(str(result[1]))
        self.ui.books_count_label.setText(str(result[2]))
        self.ui.issues_count_label.setText(str(result[3]))


        #Plotting current data in dashboard
        self.figure = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax1 = self.figure.add_subplot(111)
        result = ConnectToMySQL().get_data_for_graph()
        x = result[0]
        y = result[1]
        self.ax1.bar(x, y)

        # # Create a second set of axes and plot the line graph
        # self.ax2 = self.ax1.twinx()
        # y2 = [2, 5, 6, 4, 8]
        # self.ax2.plot(x, y2, 'r')

        self.graph_layout = QVBoxLayout()
        self.graph_layout.addWidget(self.canvas)
        self.ui.graph_widget.setLayout(self.graph_layout)

    # Teachers Page
    @pyqtSlot(bool)
    def get_teachers_data(self):
        result = ConnectToMySQL().get_teachers_data_from_db()
        if result:
            self.ui.teacher_table_widget.setRowCount(len(result))
            for row,item in enumerate(result):
                t_id = QTableWidgetItem(str(item['idteachers']))
                t_firstname = QTableWidgetItem(str(item['firstname']))
                t_lastname = QTableWidgetItem(str(item['lastname']))
                t_subject = QTableWidgetItem(str(item['subject']))
                t_contact = QTableWidgetItem(str(item['contact']))
                t_email = QTableWidgetItem(str(item['email']))
                t_address = QTableWidgetItem(str(item['address']))
                t_joined_date = QTableWidgetItem(str(item['joineddate']))

                self.ui.teacher_table_widget.setItem(row, 0, t_id)
                self.ui.teacher_table_widget.setItem(row, 1, t_firstname)
                self.ui.teacher_table_widget.setItem(row, 2, t_lastname)
                self.ui.teacher_table_widget.setItem(row, 3, t_subject)
                self.ui.teacher_table_widget.setItem(row, 4, t_contact)
                self.ui.teacher_table_widget.setItem(row, 5, t_email)
                self.ui.teacher_table_widget.setItem(row, 6, t_address)
                self.ui.teacher_table_widget.setItem(row, 7, t_joined_date)

        else:
            QMessageBox.information(self, 'Warning', 'Data could not be loaded. Please try again.')

    def get_teacher_data_to_top(self):
        teacher_row = self.ui.teacher_table_widget.currentRow()
        self.ui.teacher_first_name.setText(self.ui.teacher_table_widget.item(teacher_row,1).text())
        self.ui.teacher_last_name.setText(self.ui.teacher_table_widget.item(teacher_row,2).text())
        self.ui.teacher_subject.setText(self.ui.teacher_table_widget.item(teacher_row,3).text())
        self.ui.teacher_contact.setText(self.ui.teacher_table_widget.item(teacher_row,4).text())
        self.ui.teacher_email.setText(self.ui.teacher_table_widget.item(teacher_row,5).text())
        self.ui.teacher_address.setText(self.ui.teacher_table_widget.item(teacher_row,6).text())
    
    def clear_teacher_data_on_top(self):
        #Clear all teacher line edits
        self.ui.teacher_first_name.clear()
        self.ui.teacher_last_name.clear()
        self.ui.teacher_subject.clear()
        self.ui.teacher_contact.clear()
        self.ui.teacher_email.clear()
        self.ui.teacher_address.clear()

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

    def edit_selected_teacher(self):
        teacher_row = self.ui.teacher_table_widget.currentRow()
        id = self.ui.teacher_table_widget.item(teacher_row,0).text()
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

        ConnectToMySQL().edit_teacher_data_to_db(id, t_first, t_last, t_subject, t_contact, t_email, t_address, t_joined_date)
        self.get_teachers_data()

    def delete_selected_teacher(self):
        teacher_row = self.ui.teacher_table_widget.currentRow()
        id = self.ui.teacher_table_widget.item(teacher_row,0).text()
        self.reply = QMessageBox.question(self, 'Delete Teacher', 'Are you sure you want to delete this teacher?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if self.reply == QMessageBox.Yes:
            ConnectToMySQL().delete_teacher_data_to_db(id)
            self.get_teachers_data()
        else:
            pass


    # Students Page
    @pyqtSlot(bool)
    def get_students_data(self):
        result = ConnectToMySQL().get_students_data_from_db()
        if result:
            self.ui.student_table_widget.setRowCount(len(result))
            for row,item in enumerate(result):
                s_id = QTableWidgetItem(str(item['idstudent']))
                s_firstname = QTableWidgetItem(str(item['firstname']))
                s_lastname = QTableWidgetItem(str(item['lastname']))
                s_batch = QTableWidgetItem(str(item['batch']))
                s_faculty = QTableWidgetItem(str(item['faculty']))
                s_year = QTableWidgetItem(str(item['year']))
                s_semester = QTableWidgetItem(str(item['semester']))
                s_rollno = QTableWidgetItem(str(item['rollno']))
                s_contact = QTableWidgetItem(str(item['contact']))
                s_address = QTableWidgetItem(str(item['address']))

                self.ui.student_table_widget.setItem(row, 0, s_id)
                self.ui.student_table_widget.setItem(row, 1, s_firstname)
                self.ui.student_table_widget.setItem(row, 2, s_lastname)
                self.ui.student_table_widget.setItem(row, 3, s_batch)
                self.ui.student_table_widget.setItem(row, 4, s_faculty)
                self.ui.student_table_widget.setItem(row, 5, s_year)
                self.ui.student_table_widget.setItem(row, 6, s_semester)
                self.ui.student_table_widget.setItem(row, 7, s_rollno)
                self.ui.student_table_widget.setItem(row, 8, s_contact)
                self.ui.student_table_widget.setItem(row, 9, s_address)

        else:
            QMessageBox.information(self, 'Warning', 'Data could not be loaded. Please try again.')

    def get_student_data_to_top(self):
        student_row = self.ui.student_table_widget.currentRow()
        self.ui.student_first_name.setText(self.ui.student_table_widget.item(student_row,1).text())
        self.ui.student_last_name.setText(self.ui.student_table_widget.item(student_row,2).text())
        self.ui.student_batch.setText(self.ui.student_table_widget.item(student_row,3).text())
        self.ui.student_faculty.setText(self.ui.student_table_widget.item(student_row,4).text())
        self.ui.student_year.setText(self.ui.student_table_widget.item(student_row,5).text())
        self.ui.student_semester.setText(self.ui.student_table_widget.item(student_row,6).text())
        self.ui.student_roll_no.setText(self.ui.student_table_widget.item(student_row,7).text())
        self.ui.student_contact.setText(self.ui.student_table_widget.item(student_row,8).text())
        self.ui.student_address.setText(self.ui.student_table_widget.item(student_row,9).text())

    def clear_student_data_on_top(self):
        #Clear all student line edits
        self.ui.student_first_name.clear()
        self.ui.student_last_name.clear()
        self.ui.student_batch.clear()
        self.ui.student_faculty.clear()
        self.ui.student_year.clear()
        self.ui.student_semester.clear()
        self.ui.student_roll_no.clear()
        self.ui.student_contact.clear()
        self.ui.student_address.clear()

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

    def edit_selected_student(self):
        student_row = self.ui.student_table_widget.currentRow()
        id = self.ui.student_table_widget.item(student_row,0).text()

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

        ConnectToMySQL().edit_student_data_to_db(id, s_first, s_last, s_batch, s_faculty, s_year, s_semester, s_rollno, s_contact, s_address)
        self.get_students_data()

    def delete_selected_student(self):
        student_row = self.ui.student_table_widget.currentRow()
        id = self.ui.student_table_widget.item(student_row,0).text()
        self.reply = QMessageBox.question(self, 'Delete Student', 'Are you sure you want to delete this student?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if self.reply == QMessageBox.Yes:
            ConnectToMySQL().delete_student_data_to_db(id)
            self.get_students_data()
        else:
            pass

    # Books Page
    @pyqtSlot(bool)
    def get_books_data(self):
        result = ConnectToMySQL().get_books_data_from_db()
        if result:
            self.ui.book_table_widget.setRowCount(len(result))
            for row,item in enumerate(result):
                b_id = QTableWidgetItem(str(item['idbooks']))
                b_isbn = QTableWidgetItem(str(item['isbn']))
                b_title = QTableWidgetItem(str(item['title']))
                b_author = QTableWidgetItem(str(item['author']))
                b_publisher = QTableWidgetItem(str(item['publisher']))
                b_category = QTableWidgetItem(str(item['category']))
                b_quantity = QTableWidgetItem(str(item['quantity']))

                self.ui.book_table_widget.setItem(row, 0, b_id)
                self.ui.book_table_widget.setItem(row, 1, b_isbn)
                self.ui.book_table_widget.setItem(row, 2, b_title)
                self.ui.book_table_widget.setItem(row, 3, b_author)
                self.ui.book_table_widget.setItem(row, 4, b_publisher)
                self.ui.book_table_widget.setItem(row, 5, b_category)
                self.ui.book_table_widget.setItem(row, 6, b_quantity)

        else:
            QMessageBox.information(self, 'Warning', 'Data could not be loaded. Please try again.')

    def get_book_data_to_top(self):
        book_row = self.ui.book_table_widget.currentRow()
        self.ui.book_isbn.setText(self.ui.book_table_widget.item(book_row,1).text())
        self.ui.book_title.setText(self.ui.book_table_widget.item(book_row,2).text())
        self.ui.book_author.setText(self.ui.book_table_widget.item(book_row,3).text())
        self.ui.book_publisher.setText(self.ui.book_table_widget.item(book_row,4).text())
        self.ui.book_category.setText(self.ui.book_table_widget.item(book_row,5).text())
        self.ui.book_quantity.setText(self.ui.book_table_widget.item(book_row,6).text())

    def clear_book_data_on_top(self):
        self.ui.book_isbn.clear()
        self.ui.book_title.clear()
        self.ui.book_author.clear()
        self.ui.book_publisher.clear()
        self.ui.book_category.clear()
        self.ui.book_quantity.clear()

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

    def edit_selected_book(self):
        book_row = self.ui.book_table_widget.currentRow()
        id = self.ui.book_table_widget.item(book_row,0).text()

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

        ConnectToMySQL().edit_book_data_to_db(id, b_isbn, b_title, b_author, b_publisher, b_category, b_quantity)
        self.get_books_data()

    def delete_selected_book(self):
        book_row = self.ui.book_table_widget.currentRow()
        id = self.ui.book_table_widget.item(book_row,0).text()
        self.reply = QMessageBox.question(self, 'Delete Book', 'Are you sure you want to delete this book?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if self.reply == QMessageBox.Yes:
            ConnectToMySQL().delete_book_data_to_db(id)
            self.get_books_data()
        else:
            pass

    # Issues Page
    @pyqtSlot(bool)
    def get_issues_data(self):
        result = ConnectToMySQL().get_issues_data_from_db()
        if result:
            self.ui.issue_table_widget.setRowCount(len(result))
            for row,item in enumerate(result):
                i_id = QTableWidgetItem(str(item['idissue']))
                i_book_no = QTableWidgetItem(str(item['book_no']))
                i_student_id = QTableWidgetItem(str(item['student_id']))
                i_issue_date = QTableWidgetItem(str(item['issue_date']))
                i_due_date = QTableWidgetItem(str(item['due_date']))
                i_return_date = QTableWidgetItem(str(item['return_date']))
                i_fine = QTableWidgetItem(str(item['fine']))

                self.ui.issue_table_widget.setItem(row, 0, i_id)    
                self.ui.issue_table_widget.setItem(row, 1, i_book_no)
                self.book_name = QTableWidgetItem("Get Book name from sql")
                self.ui.issue_table_widget.setItem(row, 2, self.book_name)
                self.ui.issue_table_widget.setItem(row, 3, i_student_id)
                self.student_name = QTableWidgetItem("Get student name from sql")
                self.ui.issue_table_widget.setItem(row, 4, self.student_name)
                self.ui.issue_table_widget.setItem(row, 5, i_issue_date)
                self.ui.issue_table_widget.setItem(row, 6, i_due_date)
                self.ui.issue_table_widget.setItem(row, 7, i_return_date)
                self.ui.issue_table_widget.setItem(row, 8, i_fine)

        else:
            QMessageBox.information(self, 'Warning', 'Data could not be loaded. Please try again.')

    def get_issue_data_to_top(self):
        issue_row = self.ui.issue_table_widget.currentRow()
        self.ui.issue_book_no.setText(self.ui.issue_table_widget.item(issue_row,1).text())
        self.ui.issue_student_id.setText(self.ui.issue_table_widget.item(issue_row,3).text())
        self.ui.issue_date.setText(self.ui.issue_table_widget.item(issue_row,5).text())
        self.ui.issue_due_date.setText(self.ui.issue_table_widget.item(issue_row,6).text())
        self.ui.issue_return_date.setText(self.ui.issue_table_widget.item(issue_row,7).text())
        self.ui.issue_fine.setText(self.ui.issue_table_widget.item(issue_row,8).text())

    def clear_issue_data_on_top(self):
        self.ui.issue_book_no.clear()
        self.ui.issue_student_id.clear()
        self.ui.issue_date.clear()
        self.ui.issue_due_date.clear()
        self.ui.issue_return_date.clear()
        self.ui.issue_fine.clear()

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
        i_fine = self.ui.issue_fine.text()

        ConnectToMySQL().add_issue_data_to_db(i_book_no, i_student_id, i_issue_date, i_due_date, i_return_date, i_fine)
        self.get_issues_data()

    def edit_selected_issue(self):
        issue_row = self.ui.issue_table_widget.currentRow()
        id = self.ui.issue_table_widget.item(issue_row,0).text()
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
        i_fine = self.ui.issue_fine.text()

        ConnectToMySQL().edit_issue_data_to_db(id, i_book_no, i_student_id, i_issue_date, i_due_date, i_return_date, i_fine)
        self.get_issues_data()

    def delete_selected_issue(self):
        issue_row = self.ui.issue_table_widget.currentRow()
        id = self.ui.issue_table_widget.item(issue_row,0).text()
        self.reply = QMessageBox.question(self, 'Delete Issue', 'Are you sure you want to delete this issue?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if self.reply == QMessageBox.Yes:
            ConnectToMySQL().delete_issue_data_to_db(id)
            self.get_issues_data()
        else:
            pass

    # Settings Page
    def show_hide_current_password_method(self):
        if self.show_current_password == False:
            self.ui.current_password.setEchoMode(QLineEdit.Normal)
            self.ui.show_hide_current_password.setIcon(QIcon('icon/show.png'))
            self.show_current_password = True
        else:
            self.ui.current_password.setEchoMode(QLineEdit.Password)
            self.ui.show_hide_current_password.setIcon(QIcon('icon/hide.png'))
            self.show_current_password = False

    def show_hide_new_password_method(self):
        if self.show_new_password == False:
            self.ui.new_password.setEchoMode(QLineEdit.Normal)
            self.ui.show_hide_new_password.setIcon(QIcon('icon/show.png'))
            self.show_new_password = True
        else:
            self.ui.new_password.setEchoMode(QLineEdit.Password)
            self.ui.show_hide_new_password.setIcon(QIcon('icon/hide.png'))
            self.show_new_password = False

    def show_hide_confirm_password_method(self):
        if self.show_confirm_password == False:
            self.ui.confirm_password.setEchoMode(QLineEdit.Normal)
            self.ui.show_hide_confirm_password.setIcon(QIcon('icon/show.png'))
            self.show_confirm_password = True
        else:
            self.ui.confirm_password.setEchoMode(QLineEdit.Password)
            self.ui.show_hide_confirm_password.setIcon(QIcon('icon/hide.png'))
            self.show_confirm_password = False

    def show_login_password_method(self):
        if self.show_login_password == False:
            self.ui.password.setEchoMode(QLineEdit.Normal)
            self.ui.show_login_password_btn.setIcon(QIcon('icon/show.png'))
            self.show_login_password = True
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)
            self.ui.show_login_password_btn.setIcon(QIcon('icon/hide.png'))
            self.show_login_password = False

    def reset_password_method(self):
        current_pass = self.ui.current_password.text()
        new_pass = self.ui.new_password.text()
        confirm_pass = self.ui.confirm_password.text()
        if current_pass != self.password:
            QMessageBox.information(self, 'Warning', 'Current Password is incorrent.')
            return
        if new_pass != confirm_pass:
            QMessageBox.information(self, 'Warning', 'New Password and Confirm Password does not match.')
            return
        if new_pass == "" or confirm_pass == "":
            QMessageBox.information(self, 'Warning', 'Enter your new password and confirm password.')
            return
        if current_pass == new_pass:
            QMessageBox.information(self, 'Warning', 'You have entered old password as new password. Try again.')
            return
        if self.validate_password(new_pass):
            ConnectToMySQL().update_password(new_pass)
            self.password = new_pass
            QMessageBox.information(self, 'Information', 'Password Changed Successfully')
            self.ui.current_password.setText('')
            self.ui.new_password.setText('')
            self.ui.confirm_password.setText('')
            self.ui.LMS_label.setText("Login")
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
            QMessageBox.information(self, 'Information', 'Login with your new password.')

        else:
            QMessageBox.information(self, 'Warning', 'Pasword should contains at least 1 uppercase, 1 lowercase, 1 digit, 1 special symbol and mimimum password length should 8.')
            return
        
    def validate_password(self, password):  
        if len(password) < 8:  
            return False  
        if not re.search("[a-z]", password):  
            return False  
        if not re.search("[A-Z]", password):  
            return False  
        if not re.search("[0-9]", password):  
            return False  
        return True  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ## Loading style file
    with open("style.qss", "r") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())