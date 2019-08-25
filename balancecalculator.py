
from typing import NamedTuple
from datetime import date
import sqlite3
from sqlite3 import Error
import os


class transfer(NamedTuple):
    SORT: str = "negative"
    AMOUNT: float = 0.0
    DAY: int = date.today().day
    WEEK: int = date(date.today().year, date.today().month, date.today().day).isocalendar()[1]
    MONTH: int = date.today().month
    YEAR: int = date.today().year
    CLASS: str = ""
    SUBCLASS: str = ""
    SUBSUBCLASS: str = ""
    ACCOUNT: str = "default"
    

class BalanceCalculator:
    version = "1.0"

    sql_create_accounts_table = """ CREATE TABLE IF NOT EXISTS accounts(
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            hash text,
                                            begin_day integer,
                                            begin_week integer,
                                            begin_month integer,
                                            begin_year integer, 
                                            begin_balance float,  
                                            comment text                     
                                        ); """

    sql_create_transfer_table = """ CREATE TABLE IF NOT EXISTS transfer (
                                            id integer PRIMARY KEY,
                                            hash text,
                                            sort text,
                                            amount float,
                                            balance float,
                                            day integer,
                                            week integer,
                                            month integer,
                                            year integer,
                                            class_id integer,
                                            subclass_id integer,
                                            subsubclass_id integer,
                                            comment text                                                                        
                                        ); """

    sql_create_class_table = """ CREATE TABLE IF NOT EXISTS class (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            hash text                       
                                        ); """

    sql_create_subclass_table = """ CREATE TABLE IF NOT EXISTS subclass (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            hash text,
                                            class_id integer                      
                                        ); """

    sql_create_subsubclass_table = """ CREATE TABLE IF NOT EXISTS subsubclass (
                                            id integer PRIMARY KEY,i
                                            name text NOT NULL,
                                            hash text,
                                            class_id integer,
                                            subclass_id integer                 
                                        ); """

    sql_create_year_table = """ CREATE TABLE IF NOT EXISTS years (
                                            year integer PRIMARY KEY,
                                            hash text,
                                            begin_balance float,
                                            end_balance float               
                                        ); """

    sql_create_month_table = """ CREATE TABLE IF NOT EXISTS months (
                                            yearmonth integer PRIMARY KEY,
                                            hash text,
                                            begin_balance float,
                                            end_balance float               
                                        ); """

    sql_create_week_table = """ CREATE TABLE IF NOT EXISTS weeks (
                                            yearmonthweek integer PRIMARY KEY,
                                            hash text,
                                            begin_balance float,
                                            end_balance float               
                                        ); """

    sql_create_day_table = """ CREATE TABLE IF NOT EXISTS days (
                                            yearmonthday integer PRIMARY KEY,
                                            hash text,
                                            begin_balance float,
                                            end_balance float               
                                        ); """

    def __init__(self, user = "default", account ="default"):
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        self.account = str(account)
        self.user = str(user)
        self.month = date.today().month
        self.month_bilance = 0
        self.year = date.today().year
        self.year_bilance = 0
        self.current_bilance = 0
        self.week = date(date.today().year, date.today().month, date.today().day).isocalendar()[1]
        self.day = date.today().day
        self.logged_in = 0
        self.db_file = "db/" + user + ".db"
        self.db_directory ='/db'
        self.conn = None
        self.create_connection()
       # self.pull_history()
       # self.read_history()
        print("init_end")

    def create_dbDirectory(self):
        """checkes if folder for database exist, if it doesn't creates new one"""
        if not os.path.exists(self.db_directory):
            os.makedirs(self.db_directory)
            print("creating directory for local database")

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.create_dbDirectory()
        try:
            self.conn = sqlite3.connect(self.db_file)
            print("connected to database")
        except Error as e:
            print(e)
        if self.conn is not None:
            self.create_table(self.sql_create_accounts_table)
            self.create_table(self.sql_create_transfer_table)
            self.create_table(self.sql_create_class_table)
            self.create_table(self.sql_create_subclass_table)
            self.create_table(self.sql_create_subsubclass_table)
            self.create_table(self.sql_create_year_table)
            self.create_table(self.sql_create_month_table)
            self.create_table(self.sql_create_week_table)
            self.create_table(self.sql_create_day_table)
        else:
            print("Error! cannot create the database connection.")


    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
    # def read_from_history(self, ):

    #def write_to_history(self):




    # def pull_histroy(self):
    #
    # def push_history(self):