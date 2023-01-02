import logging
import psycopg2
from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from constants.sql_operator import SqlOperator
from db.db_condition import DBCondition
from db.db_connection import ConnectDB


class QueryBuilder:
    def __init__(self, table_name):
        self.db = ConnectDB()
        self.table_name = table_name
        self.logger = logging.getLogger(__name__)
        self.op = SqlOperator()

    # TODO check sql injection
    def insert(self, obj: object):
        cursor = self.db.db_connection.cursor()
        d = vars(obj)
        query = "INSERT INTO {table} ({columns}) VALUES {values};". \
            format(table=self.table_name,
                   columns=",".join(list(d.keys())),
                   values=tuple(d.values()))

        print(query)
        try:
            cursor.execute(query)
            self.logger.info(InfoMessage.DB_QUERY)
            self.logger.info(cursor.query)
            self.db.db_connection.commit()
        except psycopg2.Error as error:
            self.logger.error(ErrorMessage.DB_INSERT)
            self.logger.error(error)
            raise error
        self.db.close_cursor_connection(cursor)
        self.db.return_connection_to_pool(self.db.db_connection)

    # TODO generalize select
    def select(self, column: list = "*", condition: str = None, group: list = None, order: str = None,
               asc_or_desc: str = None, limit: int = None):
        cursor = self.db.db_connection.cursor()
        query = "SELECT {columns} FROM {table} {condition} {group} {order} " \
                "{asc_or_desc} {limit};".format(
            columns=",".join(list(column)) if type(column) == list else "*",
            table=self.table_name,
            condition="WHERE " + condition if condition else "",
            group="GROUP BY " + ",".join(group) if group else "",
            order="ORDER BY " + order if order else "",
            asc_or_desc=asc_or_desc if asc_or_desc else "",
            limit="LIMIT " + str(limit) if limit else "")

        try:
            cursor.execute(query)
            self.logger.info(InfoMessage.DB_QUERY)
            self.logger.info(cursor.query)
            result = cursor.fetchall()
        except psycopg2.Error as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise error
        self.db.close_cursor_connection(cursor)

        return result

    def update(self, update: list, condition: DBCondition):
        cursor = self.db.db_connection.cursor()
        query = "UPDATE {table} SET {update} WHERE {condition};". \
            format(table=self.table_name,
                   update=",".join(update),
                   condition=condition)
        try:
            cursor.execute(query)
            self.logger.info(InfoMessage.DB_QUERY)
            self.logger.info(cursor.query)
            self.db.db_connection.commit()
        except psycopg2.Error as error:
            self.logger.error(ErrorMessage.DB_INSERT)
            self.logger.error(error)
            raise error
        self.db.close_cursor_connection(cursor)
        # self.db.return_connection_to_pool(self.db.db_connection)
