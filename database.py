import mysql.connector

class ConnectToMySQL():
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = '12345'
        self.port = '3306'
        self.database = 'nextstepinfotech'
        self.conn = None

    def connect(self):
        """
        Create connection with database
        """
        self.conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.password,
            port = self.port,
            database = self.database
        )

    #Teachers Page
    def get_teachers_data_from_db(self):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = "SELECT * FROM teachers"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Failed to get data.")
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def add_teacher_data_to_db(self,first,last,subject,contact,email,address):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"INSERT INTO teachers (firstname, lastname, subject, contact, email, address) VALUES ('{first}', '{last}', '{subject}', '{contact}', '{email}', '{address}')"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to insert data.")
            print(e)
        finally:
            if self.conn:
                self.conn.commit()
                self.conn.close()

    #Students Page
    def get_students_data_from_db(self):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = "SELECT * FROM students"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Failed to get data.")
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def add_student_data_to_db(self,first,last,batch,faculty,year,semester,rollno,contact,address):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"INSERT INTO students (firstname, lastname, batch, faculty, year, semester, rollno, contact, address) VALUES ('{first}', '{last}', '{batch}', '{faculty}', '{year}', '{semester}', '{rollno}', '{contact}', '{address}')"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to insert data.")
            print(e)
        finally:
            if self.conn:
                self.conn.commit()
                self.conn.close()

   #Books Page
    def get_books_data_from_db(self):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = "SELECT * FROM books"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Failed to get data.")
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def add_book_data_to_db(self,isbn,title,author,publisher,category,quantity):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"INSERT INTO books (isbn, title, author, publisher, category, quantity) VALUES ('{isbn}', '{title}', '{author}', '{publisher}', '{category}', '{quantity}')"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to insert data.")
            print(e)
        finally:
            if self.conn:
                self.conn.commit()
                self.conn.close()

   #Issues Page
    def get_issues_data_from_db(self):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = "SELECT * FROM issues"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Failed to get data.")
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def add_issue_data_to_db(self,book_no, student_id, issue_date, due_date, return_date, fine):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"INSERT INTO issues (book_no, student_id, issue_date, due_date, return_date, fine) VALUES ('{book_no}', '{student_id}', '{issue_date}', '{due_date}', '{return_date}', '{fine}')"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to insert data.")
            print(e)
        finally:
            if self.conn:
                self.conn.commit()
                self.conn.close()

