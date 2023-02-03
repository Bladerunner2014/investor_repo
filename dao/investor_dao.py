from db.query_builder import QueryBuilder
from models.investors import InvestorsDB
from db.db_condition import DBCondition
from constants.sql_operator import SqlOperator


class InvestorDao:
    def __init__(self):
        self.db = QueryBuilder("test_inv")
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
        try:
            self.db.update(update=ls, condition=condi.condition)
        except Exception as error:
            raise error
        # updating the last update date
        try:
            self.db.update_date(user_id=data['user_id'])
        except Exception as error:
            raise error
