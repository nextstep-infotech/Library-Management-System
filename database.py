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

    #Login Details
    def get_data_for_login(self):
        try:
            result = []
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM admin')
            data = cursor.fetchall()
            for d in list(data[0][1:]):
                result.append(d)
            return result
        
        except Exception as e:
            print("Failed to get data.")
            print(e)
        finally:
            if self.conn:
                self.conn.close() 

    # Update login status
    def update_login_status(self):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute('UPDATE admin SET status = 1 WHERE status = 0;')
            self.conn.commit()
        except Exception as e:
            print("Failed to udpate status.")
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    # Update password
    def update_password(self, new):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(f"UPDATE admin SET password = '{new}', status = '0';")
            self.conn.commit()
        except Exception as e:
            print("Failed to reset password.")
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    # log out
    def logout(self):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute('UPDATE admin SET status = 0 WHERE status = 1;')
            self.conn.commit()
        except Exception as e:
            print("Failed to logout.")
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    #Dashboard Page
    def get_all_data_counts_from_db(self):
        try:
            count = []
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            cursor.execute('SELECT COUNT(*) FROM teachers')
            row_count = cursor.fetchone()
            count.append(list(row_count.values())[0])

            cursor.execute('SELECT COUNT(*) FROM students')
            row_count = cursor.fetchone()
            count.append(list(row_count.values())[0])

            cursor.execute('SELECT COUNT(*) FROM books')
            row_count = cursor.fetchone()
            count.append(list(row_count.values())[0])

            cursor.execute('SELECT COUNT(*) FROM issues')
            row_count = cursor.fetchone()
            count.append(list(row_count.values())[0])
            return count
        
        except Exception as e:
            print("Failed to get data.")
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def get_data_for_graph(self):
        try:
            result = []
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute('SELECT batch, count(*) FROM students GROUP BY batch order by batch;')
            data = cursor.fetchall()
            batch = [i[0] for i in data]
            stu = [i[1] for i in data]
            result.append(batch)
            result.append(stu)
            return result
        
        except Exception as e:
            print("Failed to get data.")
            print(e)
        finally:
            if self.conn:
                self.conn.close()
                
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

    def add_teacher_data_to_db(self,first,last,subject,contact,email,address, joined):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"INSERT INTO teachers (firstname, lastname, subject, contact, email, address, joineddate) VALUES ('{first}', '{last}', '{subject}', '{contact}', '{email}', '{address}', '{joined}')"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to insert data.")
            print(e)
        finally:
            if self.conn:
                self.conn.commit()
                self.conn.close()

    def edit_teacher_data_to_db(self,id, first,last,subject,contact,email,address, joined):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"UPDATE teachers SET firstname='{first}', lastname='{last}', subject='{subject}', contact='{contact}', email='{email}', address='{address}', joineddate='{joined}' WHERE idteachers={int(id)}"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to edit data.")
            print(e)
        finally:
            if self.conn:
                self.conn.commit()
                self.conn.close()

    def delete_teacher_data_to_db(self,id):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"DELETE FROM teachers WHERE idteachers={int(id)}"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to delete data.")
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

    def edit_student_data_to_db(self, id, first,last,batch,faculty,year,semester,rollno,contact,address):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"UPDATE students SET firstname='{first}', lastname='{last}', batch='{batch}', faculty='{faculty}', year='{year}', semester='{semester}', rollno='{rollno}', contact='{contact}', address='{address}' WHERE idstudent={int(id)}"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to insert data.")
            print(e)
        finally:
            if self.conn:
                self.conn.commit()
                self.conn.close()

    def delete_student_data_to_db(self,id):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"DELETE FROM students WHERE idstudent={int(id)}"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to delete data.")
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

    def edit_book_data_to_db(self, id, isbn, title, author,publisher,category,quantity):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"UPDATE books SET isbn='{isbn}', title='{title}', author='{author}', publisher='{publisher}', category='{category}', quantity='{quantity}' WHERE idbooks={int(id)}"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to insert data.")
            print(e)
        finally:
            if self.conn:
                self.conn.commit()
                self.conn.close()

    def delete_book_data_to_db(self,id):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"DELETE FROM books WHERE idbooks={int(id)}"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to delete data.")
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

    def edit_issue_data_to_db(self, id, book_no, student_id, issue_date, due_date, return_date, fine):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"UPDATE issues SET book_no='{book_no}', student_id='{student_id}', issue_date='{issue_date}', due_date='{due_date}', return_date='{return_date}', fine='{fine}' WHERE idissue={int(id)}"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to insert data.")
            print(e)
        finally:
            if self.conn:
                self.conn.commit()
                self.conn.close()

    def delete_issue_data_to_db(self,id):
        try:
            self.connect()
            cursor = self.conn.cursor(dictionary = True)
            sql = f"DELETE FROM issues WHERE idissue={int(id)}"
            cursor.execute(sql)
        except Exception as e:
            print("Failed to delete data.")
            print(e)
        finally:
            if self.conn:
                self.conn.commit()
                self.conn.close()


#Special function to get book name and student name in issue page.
    def get_book_data_from_db(self, id):
        try:
            self.connect()
            cursor = self.conn.cursor()
            sql = f"SELECT title FROM books WHERE idbooks='{id}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        except Exception as e:
            print("Failed to get data.")
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def get_student_data_from_db(self, id):
        try:
            self.connect()
            cursor = self.conn.cursor()
            sql = f"SELECT CONCAT(firstname, ' ', lastname) FROM students WHERE idstudent='{id}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        except Exception as e:
            print("Failed to get data.")
            print(e)
        finally:
            if self.conn:
                self.conn.close()