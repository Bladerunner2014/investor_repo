from db.query_builder import QueryBuilder
from models.investors import InvestorsDB
from db.db_condition import DBCondition
from constants.sql_operator import SqlOperator
import datetime
from datetime import timezone


class InvestorDao:
    def __init__(self):
        self.db = QueryBuilder("investors_table")
        self.op = SqlOperator()

    def insert_new_investor(self, invedb: InvestorsDB):
        try:
            self.db.insert(invedb)
        except Exception as error:
            raise error

    def select_investor(self, user_id):
        try:
            cond = DBCondition(term='user_id', operator=self.op.EQL, const=user_id)
            cond.build_condition()
            result = self.db.select(condition=cond.condition)
        except Exception as error:
            raise error
        return result

    def update_investor(self, data: dict):
        # create a list of conditions for update the information
        ls = []
        for x, y in data.items():
            cond = DBCondition(term=x, operator=self.op.EQL, const=y)
            cond.build_condition()
            ls.append(cond.condition)
        condi = DBCondition(term='user_id', operator=self.op.EQL, const=data['user_id'])
        condi.build_condition()
        value = datetime.datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
        cond_for_date = DBCondition(term='updated_at', operator=self.op.EQL, const=value)
        cond_for_date.build_condition()
        ls.append(cond_for_date.condition)
        try:
            self.db.update(update=ls, condition=condi.condition)
        except Exception as error:
            raise error

