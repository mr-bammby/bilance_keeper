
from typing import NamedTuple
from datetime import date
import pickle

class transfer(NamedTuple):
    SORT: str = "negative"
    AMOUNT: float = 0.0
    DAY: int = date.today().day
    WEEK: int = datetime.date(date.today().year, date.today().month, date.today().day).isocalendar()[1]
    MONTH: int = date.today().month
    YEAR: int = date.today().year
    CLASS: str = ""
    SUBCLASS: str = ""
    SUBSUBCLASS: str = ""
    ACCOUNT: str = "default"
    

class balance_calculator():
    version = "1.0"
    def __init__(self):
        self.history = []
        self.month = date.today().month
        self.month_bilance = 0
        self.year = date.today().year
        self.year_bilance = 0
        self.current_bilance = 0
        self.week = datetime.date(date.today().year, date.today().month, date.today().day).isocalendar()[1]
        self.day = date.today().day
        self.logged_in = 0
#        self.pull_history()
#        self.read_history()
        
    def read_history():
        