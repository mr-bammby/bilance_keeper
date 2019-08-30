
from typing import NamedTuple
from datetime import date
import os
from pathlib import Path



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
    def __init__(self, user = "default", account ="default"):
        os.chdir(Path(__file__).parent)
        self.account = str(account)
        self.account_id = None
        self.user = str(user)

        self.month = date.today().month
        self.month_bilance = 0
        self.year = date.today().year
        self.year_bilance = 0
        self.current_bilance = 0

        self.week = date(date.today().year, date.today().month, date.today().day).isocalendar()[1]
        self.day = date.today().day

        print("init_end")









