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
        if type(year_id) == str:
            if year_id == "error year_not_saved":
                self.database.insert_year(year)
            else:
                return year_id

        month_id = self.database.get_monthID(month, year_id)
        if type(month_id) == str:
            if month_id == "error month_not_saved":
                self.database.insert_month(year_id, month)
            else:
                return month_id

        week_id = self.database.get_weekID(week, year_id, month_id)
        if type(week_id) == str:
            if week_id == "error week_not_saved":
                self.database.insert_week(year_id, month_id, week)
            else:
                return week_id

        day_id = self.database.get_dayID(day, year_id, month_id, week_id)
        if type(day_id) == str:
            if day_id == "error day_not_saved":
                self.database.insert_day(year_id, month_id, week_id, day)
            else:
                return day_id

        if class_ != "None":
            print(class_)
            class_id = self.database.get_classID(class_)
            if type(class_id) == str:
                return class_id

            if subclass_ != None:
                subclass_id = self.database.get_subclassID(subclass_, class_id)
                if type(subclass_id) == str:
                    return subclass_id

                if subsubclass_ != None:
                    subsubclass_id = self.database.get_subsubclassID(subsubclass_, class_id, subclass_id)
                    if type(subsubclass_id) == str:
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

    def delete_transfer(self, type, transfer_id=None, day=None, week=None, month=None, year=None, class_=None,
                        subclass_=None, subsubclass_=None, including=False):
        if type == "transfer":
            return self.database.delete(type, transfer_id)
        elif type == "year" or type == "month" or type == "week" or type == "day":
            year_id = self.database.get_yearID(str(year))
            if type(year_id) == str:
                return year_id
            if type == "year":
                return self.database.delete(type, year_id)
            month_id = self.database.get_monthID(str(month), year_id)
            if type(month_id) == str:
                return month_id
            if type == "month":
                return self.database.delete(type, month_id)
            week_id = self.database.get_weekID(str(week), year_id, month_id)
            if type(week_id) == str:
                return week_id
            if type == "week":
                return self.database.delete(type, week_id)
            day_id = self.database.get_dayID(str(day), year_id, month_id, week_id)
            if type(day_id) == str:
                return day_id
            return self.database.delete(type, day_id)
        elif type == "class" or type == "subclass" or type == "subsubclass":
            class_id = self.database.get_classID(class_)
            if type(class_id) == str:
                return class_id
            if type == "class":
                return self.database.delete(type, class_id)
            subclass_id = self.database.get_subclassID(subclass_)
            if type(subclass_id) == str:
                return class_id
            if type == "subclass":
                return self.database.delete(type, subclass_id)
            subsubclass_id = self.database.get_subsubclassID(subsubclass_)
            if type(subsubclass_id) == str:
                return class_id
            return self.database.delete(type, subsubclass_id)
        else:
            return "error unknnown_type"
    """in progress"""
    # def change_transfer(self, transfer_id, new_transfer_line):
    #     old_transfer_line = self.database.get_transaction_list("transfer", transfer_id)
    #     if type(old_transfer_line) == str:
    #         return old_transfer_line
    #     diff = []
    #     for el1, el2, num in zip(old_transfer_line, new_transfer_line, range(len(old_transfer_line))):
    #         if el1 != el2:
    #             diff.append(num, el2)
    #     for items


    def get_transfer_list(self, type, day=None, week=None, month=None, year=None, class_=None, subclass_=None,
                          subsubclass_=None):
        if type == "year" or type == "month" or type == "week" or type == "day":
            year_id = self.database.get_yearID(str(year))
            if type(year_id) == str:
                return year_id
            if type == "year":
                list_ = self.database.get_transaction_list(type, year_id)
                return list_
        if type == "month" or type == "week" or type == "day":
            month_id = self.database.get_monthID(str(month), year_id)
            if type(month_id) == str:
                return month_id
            if type == "month":
                list_ = self.database.get_transaction_list(type, month_id)
                return list_
        if type == "week" or type == "day":
            week_id = self.database.get_weekID(str(week), year_id, month_id)
            if type(week_id) == str:
                return week_id
            if type == "week":
                list_ = self.database.get_transaction_list(type, week_id)
                return list_
        if type == "day":
            day_id = self.database.get_dayID(str(day), year_id, month_id, week_id)
            if type(day_id) == str:
                return day_id
            list_ = self.database.get_transaction_list(type, day_id)
            return list_
        if type == "class" or type == "subclass" or type == "subsubclass":
            class_id = self.database.get_classID(str(class_))
            if type(class_id) == str:
                return class_id
            if type == "class":
                list_ = self.database.get_transaction_list(type, class_id)
                return list_
        if type == "subclass" or type == "subsubclass":
            subclass_id = self.database.get_classID(str(class_))
            if type(subclass_id) == str:
                return subclass_id
            if type == "class":
                list_ = self.database.get_transaction_list(type, class_id)
                return list_
        if type == "subclass" or type == "subsubclass":
            subclass_id = self.database.get_subclassID(str(subclass_), class_id)
            if type(subclass_id) == str:
                return subclass_id
            if type == "subclass":
                list_ = self.database.get_transaction_list(type, subclass_id)
                return list_
        if type == "subsubclass":
            subsubclass_id = self.database.get_subsubclassID(str(subsubclass_), class_id, subclass_id)
            if type(subsubclass_id) == str:
                return subsubclass_id
            if type == "subsubclass":
                list_ = self.database.get_transaction_list(type, subsubclass_id)
                return list_

    def calculate_endBalance(self, list, startBalance = 0):
        try:
            endBalance = float(startBalance)
        except:
            return "error startBalance_type"
        for transfer in list:
            if transfer[2] == "positive":
                endBalance = endBalance + transfer[3]
            elif transfer[2] == "negative":
                endBalance = endBalance + transfer[3]
            else:
                return "error sort_of_transaction"
        return endBalance

    def set_endBalance(self, list, year, month = None, week = None, day = None):
        year_id = self.database.get_yearID(year)
        if month == None:
            beginBalance = self.database.get_balance("year", year_id, time= "begin")
            endBalance = self.calculate_endBalance(list, startBalance=beginBalance)
            temp = self.database.set_balance("year", year_id, endBalance)
            if type(temp) == str:
                return temp
            else:
                return 0
        monh_id = self.database.get_yearID(month, year_id)
        if week == None:
            beginBalance = self.database.get_balance("month", monh_id, time="begin")
            endBalance = self.calculate_endBalance(list, startBalance=beginBalance)
            temp = self.database.set_balance("month", monh_id, endBalance)
            if type(temp) == str:
                return temp
            else:
                return 0
        week_id = self.database.get_yearID(week, year_id, monh_id)
        if day == None:
            beginBalance = self.database.get_balance("week", week_id, time="begin")
            endBalance = self.calculate_endBalance(list, startBalance=beginBalance)
            temp = self.database.set_balance("week", week_id, endBalance)
            if type(temp) == str:
                return temp
            else:
                return 0
        day_id = self.database.get_yearID(day, year_id, monh_id, week_id)
        beginBalance = self.database.get_balance("day", day_id, time="begin")
        endBalance = self.calculate_endBalance(list, startBalance=beginBalance)
        temp = self.database.set_balance("day", day_id, endBalance)
        if type(temp) == str:
            return temp
        else:
            return 0
        return"error"

    def set_beginBalance(self, type, value, id):
        self.database.set_balance(type, id, value, time = "begin")