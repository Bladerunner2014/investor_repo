from constants.status_code import StatusCode
from dao.investor_dao import InvestorDao
from http_handler.response_handler import ResponseHandler
from models.investors import InvestorsDB
from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
import logging

from dotenv import dotenv_values
from constants.enums import SubLevel


# to handle the routes
class InvestorManager:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)
        self.dao = InvestorDao()

    # insert new investor to the database
    def handle_investor(self, dt: dict, user_id):
        sub_level = dt.get('sub_level')
        investor = InvestorsDB()
        investor.user_id = user_id
        investor.is_subscribe = dt.get('is_subscribe', True)
        investor.expire_date = dt.get('expire_date')
        investor.api_key = dt.get('api_key')
        investor.secret_key = dt['secret_key']
        investor.exchange = dt.get('exchange')

        if not all([sub_level, investor.expire_date, investor.api_key, investor.secret_key, investor.exchange]):
            self.logger.error(ErrorMessage.BAD_REQUEST)
            return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST

        investor.sub_level = SubLevel(sub_level).name

        try:
            self.dao.insert_new_investor(investor)
        except Exception as error:
            self.logger.error(ErrorMessage.INV_INSERT)
            self.logger.error(error)
            raise Exception
        res = ResponseHandler()
        res.set_status_code(StatusCode.SUCCESS)
        res.set_response({"message": InfoMessage.INV_SUCCESS})
        return res

    # return the information of an investor
    def investor_detail(self, user_id):
        try:
            result = self.dao.select_investor(user_id)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise Exception
        res = ResponseHandler()
        if not result:
            self.logger.error(ErrorMessage.DB_SELECT)
            result = ErrorMessage.DB_SELECT
            res.set_status_code(StatusCode.NOT_FOUND)
        else:
            res.set_status_code(StatusCode.SUCCESS)
        dictionary_result = self.create_dict_from_postgres(result)

        res.set_response(dictionary_result)
        return res

    def investor_by_id(self, investor_id):
        try:
            result = self.dao.select_investor_by_id(investor_id)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise Exception
        res = ResponseHandler()
        if not result:
            self.logger.error(ErrorMessage.DB_SELECT)
            result = ErrorMessage.DB_SELECT
            res.set_status_code(StatusCode.NOT_FOUND)
        else:
            res.set_status_code(StatusCode.SUCCESS)
        dictionary_result = self.create_dict_from_postgres(result)

        res.set_response(dictionary_result)
        return res

    # update the information of an investor
    def investor_update(self, data: dict, user_id):
        try:
            result = self.dao.select_investor(user_id)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise Exception
        res = ResponseHandler()

        if not result:
            self.logger.error(ErrorMessage.DB_SELECT)
            res.set_status_code(StatusCode.NOT_FOUND)
            res.set_response({"message": ErrorMessage.DB_SELECT})
            return res
        else:

            try:
                self.dao.update_investor(data)
            except Exception as error:
                self.logger.error(ErrorMessage.DB_SELECT)
                self.logger.error(error)
                raise Exception
            res.set_status_code(StatusCode.SUCCESS)
            res.set_response({"message": InfoMessage.INV_UPDATE})

            return res

    @staticmethod
    def create_dict_from_postgres(res):
        columns = ['id',
                   'user_id',
                   'api_key',
                   'secret_key',
                   'is_subscribe',
                   'exchange',
                   'expire_date',
                   'sub_level',
                   'created_at',
                   'updated_at']

        results_list = []
        for ls in res:
            results_list.append({columns[i]: ls[i] for i in range(len(columns))})

        return results_list[0]
