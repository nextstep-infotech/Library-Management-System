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
