from datetime import date
import sqlite3
from sqlite3 import Error
import os
from pathlib import Path

class databaseManeger:
    version = "1.0"

    default_classes = ["sallery", "food", "transport", "travel", "rent", "phone"]

    sql_create_accounts_table = """ CREATE TABLE IF NOT EXISTS accounts(
                                            account_id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            begin_day integer,
                                            begin_week integer,
                                            begin_month integer,
                                            begin_year integer, 
                                            balance float,  
                                            comment text                     
                                        ); """

    sql_create_transfer_table = """ CREATE TABLE IF NOT EXISTS transfer (
                                            transfer_id integer PRIMARY KEY,
                                            account_id integer NOT NULL,
                                            sort text NOT NULL,
                                            amount float NOT NULL,
                                            day_id integer NOT NULL,
                                            week_id integer NOT NULL,
                                            month_id integer NOT NULL,
                                            year_id integer NOT NULL,
                                            subsubclass_id integer,
                                            subclass_id integer,
                                            class_id integer, 
                                            comment text,
                                            FOREIGN KEY (account_id)
                                                REFERENCES accounts (account_id)
                                                ON UPDATE CASCADE
                                                ON DELETE RESTRICT,
                                            FOREIGN KEY (year_id)
                                                REFERENCES years (year_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                                            FOREIGN KEY (month_id)
                                                REFERENCES months (month_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                                            FOREIGN KEY (week_id)
                                                REFERENCES weeks (week_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                                            FOREIGN KEY (day_id)
                                                REFERENCES days (day_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                                            FOREIGN KEY (class_id)
                                                REFERENCES class (class_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                                            FOREIGN KEY (subclass_id)
                                                REFERENCES subclass (subclass_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                                            FOREIGN KEY (subsubclass_id)
                                                REFERENCES subsubclass (subsubclass_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE

                                        ); """

    sql_create_class_table = """ CREATE TABLE IF NOT EXISTS class (
                                            class_id integer PRIMARY KEY,
                                            account_id integer NOT NULL,
                                            name text NOT NULL,   
                                            FOREIGN KEY (account_id)
                                                REFERENCES accounts (account_id)
                                                ON UPDATE CASCADE
                                                ON DELETE RESTRICT                 
                                        ); """

    sql_create_subclass_table = """ CREATE TABLE IF NOT EXISTS subclass (
                                            subclass_id integer PRIMARY KEY,
                                            class_id integer NOT NULL, 
                                            account_id integer NOT NULL,
                                            name text NOT NULL,
                                            FOREIGN KEY (account_id)
                                                REFERENCES accounts (account_id)
                                                ON UPDATE CASCADE
                                                ON DELETE RESTRICT,
                                            FOREIGN KEY (class_id)
                                                REFERENCES class (class_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE                   
                                        ); """

    sql_create_subsubclass_table = """ CREATE TABLE IF NOT EXISTS subsubclass (
                                            subsubclass_id integer PRIMARY KEY,
                                            subclass_id integer NOT NULL,
                                            class_id integer NOT NULL,
                                            account_id integer NOT NULL, 
                                            name text NOT NULL,
                                            FOREIGN KEY (account_id)
                                                REFERENCES accounts (account_id)
                                                ON UPDATE CASCADE
                                                ON DELETE RESTRICT,
                                            FOREIGN KEY (class_id)
                                                REFERENCES class (class_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                                            FOREIGN KEY (subclass_id)
                                                REFERENCES subclass (subclass_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE
                                        ); """

    sql_create_year_table = """ CREATE TABLE IF NOT EXISTS years (
                                            year_id integer PRIMARY KEY,
                                            account_id integer NOT NULL,
                                            year text NOT NULL,
                                            begin_balance float NOT NULL,
                                            end_balance float NOT NULL,
                                            FOREIGN KEY (account_id)
                                                REFERENCES accounts (account_id)
                                                ON UPDATE CASCADE
                                                ON DELETE RESTRICT               
                                        ); """

    sql_create_month_table = """ CREATE TABLE IF NOT EXISTS months (
                                            month_id integer PRIMARY KEY,
                                            year_id integer NOT NULL,
                                            account_id integer NOT NULL,
                                            month text NOT NULL,
                                            begin_balance float NOT NULL,
                                            end_balance float NOT NULL,
                                            FOREIGN KEY (account_id)
                                                REFERENCES accounts (account_id)
                                                ON UPDATE CASCADE
                                                ON DELETE RESTRICT,
                                            FOREIGN KEY (year_id)
                                                REFERENCES years (year_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE               
                                        ); """

    sql_create_week_table = """ CREATE TABLE IF NOT EXISTS weeks (
                                            week_id integer PRIMARY KEY,
                                            month_id integer NOT NULL,
                                            year_id integer NOT NULL,
                                            account_id integer NOT NULL,
                                            week text NOT NULL,
                                            begin_balance float NOT NULL,
                                            end_balance float NOT NULL,
                                            FOREIGN KEY (account_id)
                                                REFERENCES accounts (account_id)
                                                ON UPDATE CASCADE
                                                ON DELETE RESTRICT,
                                            FOREIGN KEY (year_id)
                                                REFERENCES years (year_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                                            FOREIGN KEY (month_id)
                                                REFERENCES months (month_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE
                                        ); """

    sql_create_day_table = """ CREATE TABLE IF NOT EXISTS days (
                                            day_id integer PRIMARY KEY,
                                            week_id integer NOT NULL,
                                            month_id integer NOT NULL,
                                            year_id integer NOT NULL,
                                            account_id integer NOT NULL,
                                            day text NOT NULL,
                                            begin_balance float NOT NULL,
                                            end_balance float NOT NULL,
                                            FOREIGN KEY (account_id)
                                                REFERENCES accounts (account_id)
                                                ON UPDATE CASCADE
                                                ON DELETE RESTRICT,
                                            FOREIGN KEY (year_id)
                                                REFERENCES years (year_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                                            FOREIGN KEY (month_id)
                                                REFERENCES months (month_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                                            FOREIGN KEY (week_id)
                                                REFERENCES weeks (week_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE            
                                        ); """

    def __init__(self, account ="default", user = "default"):
        os.chdir(Path(__file__).parent)
        self.user = user
        self.account = str(account)
        self.account_id = None

        self.month = date.today().month
        self.year = date.today().year
        self.week = date(date.today().year, date.today().month, date.today().day).isocalendar()[1]
        self.day = date.today().day

        self.db_directory ="db"
        self.db_file = os.path.join(os.getcwd(), self.db_directory + "/" + user + ".db")
        self.db_connected = False
        self.account_connected = False

        self.create_connection()
        self.insert_account()

        for item in self.default_classes:
            self.insert_class(item)

    def create_dbDirectory(self):
        #doesnt_work
        """checkes if folder for database exist, if it doesn't creates new one"""
        path = os.path.join(os.getcwd(), self.db_directory)
        if not os.path.exists(path):
            os.makedirs(path)
            print("creating directory for local database")
        else:
            print("databse already exists")
        return 1
    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.create_dbDirectory()
        conn = None
        try:
            with sqlite3.connect(self.db_file) as conn:
                print("connected to database")
                self.db_connected = True
        except Error as e:
            print(e)
            print("Error! cannot create the database connection.")
            return "connecting_to_dtatbase error"
        if conn is not None:
            self.create_table(self.sql_create_accounts_table)
            self.create_table(self.sql_create_class_table)
            self.create_table(self.sql_create_subclass_table)
            self.create_table(self.sql_create_subsubclass_table)
            self.create_table(self.sql_create_year_table)
            self.create_table(self.sql_create_month_table)
            self.create_table(self.sql_create_week_table)
            self.create_table(self.sql_create_day_table)
            self.create_table(self.sql_create_transfer_table)
        else:
            print("Error! cannot create the database connection.")
            return "connecting_to_dtatbase error"
        return 1
    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            with sqlite3.connect(self.db_file) as conn:
                c = conn.cursor()
                c.execute(create_table_sql)
                return 1
        except Error as e:
            print(e)
            return "table_creation error"
    def insert_account(self, comment = ""):
        """inserts new accout to account table if it doesn't exist"""
        if self.db_connected:
            entry = None
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM accounts WHERE (name=?)', (self.account,))
                        entry = cur.fetchone()
            except Error as e:
                print(e)
                return "database_error table_accounts"
            if entry == None:
                try:
                    with sqlite3.connect(self.db_file) as conn:
                            sql = ''' INSERT INTO accounts(name,begin_day,begin_week,begin_month,begin_year,balance,comment)
                                      VALUES(?,?,?,?,?,?,?) '''
                            account = (self.account, self.day, self.week, self.month, self.year, 0, comment)
                            cur = conn.cursor()
                            cur.execute(sql, account)
                            print("Inserted account: "+ str(account))
                            self.account_connected = True
                            self.account_id = cur.lastrowid
                            return cur.lastrowid
                except Error as e:
                    print(e)
                    return "database_error table_accounts"
            else:
                try:
                    self.account_connected = True
                    self.account_id = entry[0]
                    return(entry[0])
                except Exception as e:
                    print(e)
                    return "database_error table_accounts"
        else:
            print("can not insert account, db not connected, table_accounts")
            return "db_not_connected_error table_accounts"
    def insert_transfer(self, sort, amount, day_id, week_id, month_id, year_id, class_id = None , subclass_id = None, subsubclass_id = None, comment = ""):
        """inserts new traansfer to transfer table"""
        if self.account_connected:
            if sort == "negative" or sort == "positive":
                try:
                    amount = float(amount)
                except ValueError:
                    return "unexpected amount value, must be convertible to float"
                try:
                    with sqlite3.connect(self.db_file) as conn:
                        sql = ''' INSERT INTO transfer(account_id,sort,amount,day_id,week_id,month_id,year_id,class_id,subclass_id,subsubclass_id,comment)
                                      VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
                        transfer = (self.account_id, sort, amount, day_id, week_id, month_id, year_id, class_id, subclass_id, subsubclass_id, comment)
                        cur = conn.cursor()
                        cur.execute(sql, transfer)
                        print("Inserted transfer: "+ str(transfer))
                        return cur.lastrowid
                except Error as e:
                    print(e)
                    return "database_error table_transfers"
        else:
            print("can not insert transfer, account not connected, table_transfers")
            return "account_not_connected_error table_transfers"
    def insert_class(self, name):
        """inserts new class to class table if it doesn't exist"""
        if self.account_connected:
            entry = None
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM class WHERE (name=?)', (name,))
                        entry = cur.fetchone()
            except Error as e:
                print(e)
                return "database_error table_class"

            try:
                with sqlite3.connect(self.db_file) as conn:
                    if entry == None:
                        sql = ''' INSERT INTO class(account_id, name)
                                  VALUES(?,?) '''
                        class_tuple = (self.account_id, name)
                        cur = conn.cursor()
                        cur.execute(sql, class_tuple)
                        print("Inserted class: "+ str(class_tuple))
                        return cur.lastrowid
            except Error as e:
                print(e)
                return "database_error table_classs"
        else:
            print("can not insert class, account not connected, table_classs")
            return "account_not_connected_error table_classs"
    def insert_subclass(self, name,  class_id):
        """inserts new subclass to subclass table if it doesn't exist"""
        if self.account_connected:
            entry = None
            try:
                class_id = int(class_id)
            except:
                class_id = self.get_classID(class_id)
                if type(class_id) == "str":
                    return "unknown class"
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM subclass WHERE (name=? AND class_id=?)', (name, class_id))
                        entry = cur.fetchone()
            except Error as e:
                print(e)
                return "database_error table_subclass"

            try:
                with sqlite3.connect(self.db_file) as conn:
                    if entry == None:
                        sql = ''' INSERT INTO subclass(account_id,name,class_id)
                                  VALUES(?,?,?) '''
                        subclass_tuple = (self.account_id, name, class_id)
                        cur = conn.cursor()
                        cur.execute(sql, subclass_tuple)
                        print("Inserted subclass: "+ str(subclass_tuple))
                        return cur.lastrowid
            except Error as e:
                print(e)
                return "database_error table_subclass"
        else:
            print("can not insert subclass, account not connected, table_subclass")
            return "account_not_connected_error table_subclass"
    def insert_subsubclass(self, name,  class_id, subclass_id):
        """inserts new subsubclass to subsubclass table if it doesn't exist"""
        if self.account_connected:
            entry = None
            try:
                class_id = int(class_id)
            except:
                class_id = self.get_classID(class_id)
                if type(class_id) == "str":
                    return "unknown class"
            try:
                subclass_id = int(subclass_id)
            except:
                subclass_id = self.get_subclassID(subclass_id)
                if type(subclass_id) == "str":
                    return "unknown subclass"

            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM subsubclass WHERE (name=? AND class_id=? AND subclass_id=?)', (name, class_id, subclass_id))
                        entry = cur.fetchone()
            except Error as e:
                print(e)
                return "database_error table_subsubclass"

            try:
                with sqlite3.connect(self.db_file) as conn:
                    if entry == None:
                        sql = ''' INSERT INTO subsubclass(account_id,name,class_id,subclass_id)
                                  VALUES(?,?,?,?) '''
                        subsubclass_tuple = (self.account_id, name, class_id, subclass_id)
                        cur = conn.cursor()
                        cur.execute(sql, subsubclass_tuple)
                        print("Inserted subsubclass: "+ str(subsubclass_tuple))
                        return cur.lastrowid
            except Error as e:
                print(e)
                return "database_error table_subsubclass"
        else:
            print("can not insert subsubclass, account not connected, table_subsubclass")
            return "account_not_connected_error table_subsubclass"
    def insert_year(self, year,  begin_balance = 0 ):
        """inserts new year to years table if it doesn't exist"""
        if self.account_connected:
            try:
                begin_balance = float(begin_balance)
                year = int(year)
                if year < 1900:
                    return "unexpected input"
                year = str(year)
            except ValueError:
                return "unexpected input"
            entry = None
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM years WHERE (year=?)', (year,))
                        entry = cur.fetchone()
            except Error as e:
                print(e)
                return "database_error table_year"

            try:
                with sqlite3.connect(self.db_file) as conn:
                    if entry == None:
                        sql = ''' INSERT INTO years(account_id,year,begin_balance,end_balance)
                                  VALUES(?,?,?,?) '''
                        year_tuple = (self.account_id, year, begin_balance, begin_balance)
                        cur = conn.cursor()
                        cur.execute(sql, year_tuple)
                        print("Inserted year: "+ str(year_tuple))
                        return cur.lastrowid
            except Error as e:
                print(e)
                return "database_error table_year"
        else:
            print("can not insert year, account not connected, table_year")
            return "account_not_connected_error table_year"
    def insert_month(self, year_id, month,  begin_balance = 0 ):
        """inserts new year to years table if it doesn't exist"""
        if self.account_connected:
            try:
                year_id = int(year_id)
                begin_balance = float(begin_balance)
                month = int(month)
                if 0 > month or month > 13:
                    return "unexpected input"
                month = str(month)
            except ValueError:
                return "unexpected input"
            entry = None
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM months WHERE (month=?)', (month,))
                        entry = cur.fetchone()
            except Error as e:
                print(e)
                return "database_error table_month"

            try:
                with sqlite3.connect(self.db_file) as conn:
                    if entry == None:
                        sql = ''' INSERT INTO months(account_id,year_id,month,begin_balance,end_balance)
                                  VALUES(?,?,?,?,?) '''
                        month_tuple = (self.account_id, year_id, month, begin_balance, begin_balance)
                        cur = conn.cursor()
                        cur.execute(sql, month_tuple)
                        print("Inserted month: "+ str(month_tuple))
                        return cur.lastrowid
            except Error as e:
                print(e)
                return "database_error table_month"
        else:
            print("can not insert month, account not connected, table_month")
            return "account_not_connected_error table_month"
    def insert_week(self, year_id, month_id, week, begin_balance = 0 ):
        """inserts new year to years table if it doesn't exist"""
        if self.account_connected:
            try:
                year_id = int(year_id)
                month_id=int(month_id)
                begin_balance = float(begin_balance)
                week = int(week)
                if 0 > week or week > 53:
                    return "unexpected input"
                week = str(week)
            except ValueError:
                return "unexpected input"
            entry = None
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM weeks WHERE (week=?)', (week,))
                        entry = cur.fetchone()
            except Error as e:
                print(e)
                return "database_error table_week"

            try:
                with sqlite3.connect(self.db_file) as conn:
                    if entry == None:
                        sql = ''' INSERT INTO weeks(account_id,year_id,month_id,week,begin_balance,end_balance)
                                  VALUES(?,?,?,?,?,?) '''
                        week_tuple = (self.account_id, year_id, month_id, week, begin_balance, begin_balance)
                        cur = conn.cursor()
                        cur.execute(sql, week_tuple)
                        print("Inserted week: "+ str(week_tuple))
                        return cur.lastrowid
            except Error as e:
                print(e)
                return "database_error table_week"
        else:
            print("can not insert week, account not connected, table_week")
            return "account_not_connected_error table_week"
    def insert_day(self, year_id, month_id, week_id,  day,  begin_balance = 0 ):
        """inserts new year to years table if it doesn't exist"""
        if self.account_connected:
            try:
                year_id = int(year_id)
                month_id = int(month_id)
                week_id = int(week_id)
                begin_balance = float(begin_balance)
                day = int(day)
                if 0 > day or day > 31:
                    return "unexpected input"
                day = str(day)
            except ValueError:
                return "unexpected input"
            entry = None
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM days WHERE (day=?)', (day,))
                        entry = cur.fetchone()
            except Error as e:
                print(e)
                return "database_error table_day"

            try:
                with sqlite3.connect(self.db_file) as conn:
                    if entry == None:
                        sql = ''' INSERT INTO days(account_id,year_id,month_id,week_id,day,begin_balance,end_balance)
                                  VALUES(?,?,?,?,?,?,?) '''
                        day_tuple = (self.account_id, year_id, month_id, week_id, day, begin_balance, begin_balance)
                        cur = conn.cursor()
                        cur.execute(sql, day_tuple)
                        print("Inserted day: "+ str(day_tuple))
                        return cur.lastrowid
            except Error as e:
                print(e)
                return "database_error table_day"
        else:
            print("can not insert day, account not connected, table_day")
            return "account_not_connected_error table_day"
    def get_classID(self, class_name):
        if self.account_connected:
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM class WHERE (name=? AND account_id)=?', (class_name, self.account_id))
                        entry = cur.fetchone()
                        if entry == None:
                            return "error class_not_saved"
                        return entry[0]
                    else:
                        return"database_error table_class"
            except Error as e:
                print(e)
                return "database_error table_class"
        else:
            print("can not get classID, account not connected, table_class")
            return "account_not_connected_error table_class"
    def get_subclassID(self, subclass_name, class_id):
        """returns classID according name and class_id"""
        if self.account_connected:
            try:
                if type(class_id) is str:
                    class_id = self.get_classID(class_id)
                class_id = int(class_id)
            except ValueError:
                return "unexpected input"
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM subclass WHERE (name=? AND class_id=? AND account_id=?)', (subclass_name,class_id,self.account_id))
                        entry = cur.fetchone()
                        if entry == None:
                            return "error subclass_not_saved"
                        return entry[0]
                    else:
                        return"error invalid_input"
            except Error as e:
                print(e)
                return "database_error table_subclass"
        else:
            print("can not get subclassID, account not connected, table_subclass")
            return "account_not_connected_error table_subclass"
    def get_subsubclassID(self, subsubclass_name, class_id, subclass_id):
        """returns subsubclassID according name, class_id and subclass id """
        if self.account_connected:
            try:
                if type(class_id) is str:
                    class_id = self.get_classID(class_id)
                if type(subclass_id) is str:
                    subclass_id = self.get_classID(subclass_id)
                class_id = int(class_id)
                subclass_id = int(subclass_id)
            except ValueError:
                return "unexpected input"
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM subsubclass WHERE (name=? AND class_id=? AND subclass_id=? AND account_id=?)', (subsubclass_name,class_id,subclass_id,self.account_id))
                        entry = cur.fetchone()
                        if entry == None:
                            return "error subsubclass_not_saved"
                        return entry[0]
                    else:
                        return"error invalid_input"
            except Error as e:
                print(e)
                return "database_error table_subsubclass"
        else:
            print("can not get subsubclassID, account not connected, table_subsubclass")
            return "account_not_connected_error table_subsubclass"
    def get_yearID(self, year_name):
        """returns yearID according name"""
        if self.account_connected:
            try:
                year_name = str(year_name)
            except:
                return "unexcepted input"
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM years WHERE (year=? AND account_id=?)', (year_name,self.account_id))
                        entry = cur.fetchone()
                        if entry == None:
                            return "error year_not_saved"
                        return entry[0]
                    else:
                        return"database_error table_year"
            except Error as e:
                print(e)
                return "database_error table_year"
        else:
            print("can not get yearID, account not connected, table_years")
            return "account_not_connected_error table_year"
    def get_monthID(self, month_name, year_id):
        """returns monthID according name"""
        if self.account_connected:
            try:
                month_name = str(int(month_name))
                if type(year_id) is str:
                    temp = self.get_yearID(year_id)
                    if type(temp) is int:
                        year_id = temp
                year_id = int(year_id)
            except:
                return "unexcepted input"
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM months WHERE (month=? AND year_id=? AND account_id=?)', (month_name, year_id, self.account_id))
                        entry = cur.fetchone()
                        if entry == None:
                            return "error month_not_saved"
                        return entry[0]
                    else:
                        return"database_error table_month"
            except Error as e:
                print(e)
                return "database_error table_month"
        else:
            print("can not get monthID, account not connected, table_months")
            return "account_not_connected_error table_month"
    def get_weekID(self, week_name, year_id, month_id):
        """returns weekID according name"""
        if self.account_connected:
            try:
                week_name = str(int(week_name))
                if type(year_id) is str:
                    temp = self.get_yearID(year_id)
                    if type(temp) is int:
                        year_id = temp
                if type(month_id) is str:
                    temp = self.get_monthID(year_id, month_id)
                    if type(temp) is int:
                        month_id = temp
                year_id = int(year_id)
                month_id = int(month_id)
            except:
                return "unexcepted input"
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM weeks WHERE (week=? AND year_id=? AND month_id=? AND account_id=?)', (week_name, year_id, month_id, self.account_id))
                        entry = cur.fetchone()
                        if entry == None:
                            return "error week_not_saved"
                        return entry[0]
                    else:
                        return"database_error table_week"
            except Error as e:
                print(e)
                return "database_error table_week"
        else:
            print("can not get weekID, account not connected, table_weeks")
            return "account_not_connected_error table_week"
    def get_dayID(self, day_name, year_id, month_id, week_id):
        """returns dayID according name"""
        if self.account_connected:
            try:
                day_name = str(int(day_name))
                if type(year_id) is str:
                    temp = self.get_yearID(year_id)
                    if type(temp) is int:
                        year_id = temp
                if type(month_id) is str:
                    temp = self.get_monthID(year_id,month_id)
                    if type(temp) is int:
                        month_id = temp
                if type(week_id) is str:
                    temp = self.get_monthID(month_id, year_id, week_id)
                    if type(temp) is int:
                        week_id = temp
                year_id = int(year_id)
            except:
                return "unexcepted input"
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM days WHERE (day=? AND year_id=? AND month_id=? AND week_id=? AND account_id=?)', (day_name, year_id,month_id,week_id, self.account_id))
                        entry = cur.fetchone()
                        if entry == None:
                            return "error day_not_saved"
                        return entry[0]
                    else:
                        return"database_error table_day"
            except Error as e:
                print(e)
                return "database_error table_day"
        else:
            print("can not get dayID, account not connected, table_days")
            return "account_not_connected_error table_day"
    def get_balance(self, type, id, time = "end"):
        entry = None
        if type == "year":
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM years WHERE (year_id=?)', (id,))
                        entry = cur.fetchone()
                        if entry == None:
                            return "error year_not_saved"
                        if time == "end":
                            return entry[4]
                        elif time == "begin":
                            return entry[3]
                        else:
                            return "unknown time"
            except Error as e:
                print(e)
                return "database_error table_year"
        elif type == "month":
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM months WHERE (month_id=?)', (id,))
                        entry = cur.fetchone()
                        if entry == None:
                            return "error month_not_saved"
                        if time == "end":
                            return entry[5]
                        elif time == "begin":
                            return entry[4]
                        else:
                            return "unknown time"
            except Error as e:
                print(e)
                return "database_error table_month"
        elif type == "week":
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM weeks WHERE (week_id=?)', (id,))
                        entry = cur.fetchone()
                        if entry == None:
                            return "error week_not_saved"
                        if time == "end":
                            return entry[6]
                        elif time == "begin":
                            return entry[5]
                        else:
                            return "unknown time"
            except Error as e:
                print(e)
                return "database_error table_week"
        elif type == "day":
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM days WHERE (day_id=?)', (id,))
                        entry = cur.fetchone()
                        if entry == None:
                            return "error day_not_saved"
                        if time == "end":
                            return entry[7]
                        elif time == "begin":
                            return entry[6]
                        else:
                            return "unknown time"
            except Error as e:
                print(e)
                return "database_error table_day"
        else:
            return "unknown table name"
    def set_balance(self, type, id, value, time = "end"):
        if type == "year":
            try :
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        if time == "end":
                            sql = ''' UPDATE years
                                SET end_balance = ? 
                                WHERE year_id = ?'''
                        elif time == "begin":
                            sql = ''' UPDATE years
                                SET begin_balance = ? 
                                WHERE year_id = ?'''
                        else:
                            return "unknown time"
                        cur.execute(sql, (value, id))
            except Error as e:
                print(e)
                return "database_error table_year"
        elif type == "month":
            try:
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        if time == "end":
                            sql = ''' UPDATE months
                                SET end_balance = ? 
                                WHERE month_id = ?'''
                        elif time == "begin":
                            sql = ''' UPDATE months
                                SET begin_balance = ? 
                                WHERE month_id = ?'''
                        else:
                            return "unknown time"
                        cur.execute(sql, (value, id))
            except Error as e:
                print(e)
                return "database_error table_month"
        elif type == "week":
            try:
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        if time == "end":
                            sql = ''' UPDATE weeks
                                SET end_balance = ? 
                                WHERE week_id = ?'''
                        elif time == "begin":
                            sql = ''' UPDATE weeks
                                SET begin_balance = ? 
                                WHERE week_id = ?'''
                        else:
                            return "unknown time"
                        cur.execute(sql, (value, id))
            except Error as e:
                print(e)
                return "database_error table_week"
        elif type == "day":
            try:
                with sqlite3.connect(self.db_file) as conn:
                    if conn != None:
                        cur = conn.cursor()
                        if time == "end":
                            sql = ''' UPDATE days
                                SET end_balance = ? 
                                WHERE day_id = ?'''
                        elif time == "begin":
                            sql = ''' UPDATE days
                                SET begin_balance = ? 
                                WHERE day_id = ?'''
                        else:
                            return "unknown time"
                        cur.execute(sql, (value, id))
            except Error as e:
                print(e)
                return "database_error table_day"
        else:
            return "unknown table name"
        return 0
