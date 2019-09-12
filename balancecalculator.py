from typing import NamedTuple
from datetime import date
import os
from pathlib import Path
from databaseManeger import databaseManeger


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

    def __init__(self, user="default", account="default"):
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

        self.database = databaseManeger()
        print(self.database.get_yearID(2025))
        self.database.insert_year(2025, 0)
        year_id = self.database.get_yearID(2025)
        self.database.insert_month(year_id, 1)
        month_id = self.database.get_monthID(1, year_id)
        print(month_id)
        self.database.insert_week(year_id, month_id, 1)
        week_id = self.database.get_weekID(1, year_id, month_id)

        self.database.insert_day(year_id, month_id, week_id, 4)

        day_id = self.database.get_dayID(4, year_id, month_id, week_id)
        print(day_id)
        self.database.insert_transfer("positive", 555, day_id, week_id, month_id, year_id)
        self.database.insert_transfer("negative", 55, day_id, week_id, month_id, year_id)
        self.database.insert_transfer("negative", 11, day_id, week_id, month_id, year_id)
        self.database.insert_transfer("negative", 22, day_id, week_id, month_id, year_id)
        self.database.insert_transfer("positive", 333, day_id, week_id, month_id, year_id)
        print(self.database.get_transaction_list("year", year_id)[-1])

    def add_transfer(self, value, day, week, month, year, sort="positive", class_=None, subclass_=None,
                     subsubclass_=None, comment=""):

        if sort != "positive" and sort != "negative":
            return "invalid input"

        try:
            value = float(value)
            day = int(day)
            week = int(week)
            month = int(month)
            year = int(year)
            class_ = str(class_)
            subclass_ = str(subclass_)
            subsubclass_ = str(subsubclass_)
        except:
            return "invalid input"

        if value < 0:
            sort = "negative"
        elif value == 0:
            return "invalid value"
        year_id = self.database.get_yearID(year)
        if type(year_id) == "str":
            if year_id == "error year_not_saved":
                self.database.insert_year(year)
            else:
                return year_id

        month_id = self.database.get_monthID(month, year_id)
        if type(month_id) == "str":
            if month_id == "error month_not_saved":
                self.database.insert_month(year_id, month)
            else:
                return month_id

        week_id = self.database.get_weekID(week, year_id, month_id)
        if type(week_id) == "str":
            if week_id == "error week_not_saved":
                self.database.insert_week(year_id, month_id, week)
            else:
                return week_id

        day_id = self.database.get_dayID(day, year_id, month_id, week_id)
        if type(day_id) == "str":
            if day_id == "error day_not_saved":
                self.database.insert_day(year_id, month_id, week_id, day)
            else:
                return day_id

        if class_ != "None":
            print(class_)
            class_id = self.database.get_classID(class_)
            if type(class_id) == "str":
                return class_id

            if subclass_ != None:
                subclass_id = self.database.get_subclassID(subclass_, class_id)
                if type(subclass_id) == "str":
                    return subclass_id

                if subsubclass_ != None:
                    subsubclass_id = self.database.get_subsubclassID(subsubclass_, class_id, subclass_id)
                    if type(subsubclass_id) == "str":
                        return subsubclass_id
                    self.database.insert_transfer(sort, value, day_id, week_id, month_id, year_id, class_id=class_id,
                                                  subclass_id=subclass_id, subsubclass_id=subsubclass_id,
                                                  comment=comment)
                else:
                    self.database.insert_transfer(sort, value, day_id, week_id, month_id, year_id, class_id=class_id,
                                                  subclass_id=subclass_id, comment=comment)
            else:
                self.database.insert_transfer(sort, value, day_id, week_id, month_id, year_id, class_id=class_id,
                                              comment=comment)
        else:
            self.database.insert_transfer(sort, value, day_id, week_id, month_id, year_id, comment=comment)

